#!/usr/bin/env python3.6
import time
import json
import os
from collections import OrderedDict
from coinmarketcap import Market


class CoinmarketcapHelper:

    __DATA_FOLDER = './data'

    def __init__(self, convert_currency='usd', data_folder=__DATA_FOLDER):
        self.tickers = {}
        self.symbols = {}
        self.convert_currency = convert_currency
        self.tickers_path = f'{data_folder}/tickers/coinmarketcap_tickers_{convert_currency.upper()}.json'
        self.symbols_aliases_path = f'{data_folder}/symbols_aliases.json'
        self.symbols_path = f'{data_folder}/coinmarketcap_symbols.json'
        self.aliases = json.load(open(self.symbols_aliases_path))
        self.coinmarketcap = Market()
        self._initialize()

    def _initialize(self):
        download_tickers = True
        if os.path.exists(self.tickers_path):
            date_now = time.time()
            file_date = os.path.getmtime(self.tickers_path)
            file_seconds_old = date_now - file_date
            # This will make sure that the file will be loaded if it was saved within 1 hour
            if file_seconds_old < 60 * 60:
                self.tickers = json.load(open(self.tickers_path))
                download_tickers = False

        if download_tickers:
            tickers = self.coinmarketcap.ticker(start=0, limit=10000, convert=self.convert_currency)
            self._process_tickers(tickers)
            with open(self.tickers_path, 'w') as f:
                f.write(json.dumps(self.tickers, indent=2))

        if self.symbols == {}:
            self.symbols = json.load(open(self.symbols_path))

    def _process_tickers(self, tickers):
        errors = []
        symbols_ranked = {}
        for ticker in tickers:
            # Add to tickers dictionary (key = coinmarketcap id = crypo lower case in most cases)
            id = ticker['id']
            self.tickers[id] = ticker

            # Add symbol_info (name + id) to symbols dictionary
            symbol = ticker['symbol']
            name = ticker['name']
            symbol_info = self._get_symbol_info(ticker)
            symbol_value = symbols_ranked.get(symbol)
            if symbol_value is not None:
                errors.append(f"{symbol}: {self._get_previous_id(symbol_value)} / {name}")
                if not isinstance(symbol_value, list):
                    symbol_value = [symbol_value]
                symbol_value.append(symbol_info[1])
                symbols_ranked[symbol] = symbol_value
            else:
                symbols_ranked[symbol] = symbol_info[1]

        # Save symbols sorted alphabetically
        self.symbols = OrderedDict(sorted(symbols_ranked.items(), key=lambda t: t[0]))
        with open(self.symbols_path, 'w') as f:
            f.write(json.dumps(self.symbols, indent=2))

        if len(errors) > 0:
            print('The following symbols were conflicting: \n' + '\n'.join(sorted(errors)))

    def _get_symbol_info(self, ticker):
        id = ticker['id']
        name = ticker['name']
        symbol = ticker['symbol']
        result = [symbol, {'name': name, 'id': id}]
        return result

    def _get_previous_id(self, symbol_value):
        if isinstance(symbol_value, list):
            return symbol_value[-1]['name']
        else:
            return symbol_value['name']

    def _get_price(self, currency_symbol, convert_currency):
        currency_id = self.get_currency_id(currency_symbol)
        if currency_id is None:
            return None

        ticker = self.tickers[currency_id]
        return float(ticker[f'price_{convert_currency.lower()}'])

    def get_price(self, currency_symbol):
        return self._get_price(currency_symbol, self.convert_currency)

    def get_price_usd(self, currency_symbol):
        return self._get_price(currency_symbol, 'usd')

    def get_price_btc(self, currency_symbol):
        return self._get_price(currency_symbol, 'btc')

    def get_currency_id(self, currency_symbol):
        currency_symbol = currency_symbol.upper()
        alias = self.aliases.get(currency_symbol)
        currency_info = self.symbols.get(alias or currency_symbol)
        if currency_info is None:
            print(f'Currency {currency_symbol} not found in our coinmarketcap list.')
            return None

        if isinstance(currency_info, list):
            # TODO: improve logic here, use an override list or so
            currency_id = currency_info[0]['id']
        else:
            currency_id = currency_info['id']

        return currency_id


if __name__ == '__main__':
    CoinmarketcapHelper()
