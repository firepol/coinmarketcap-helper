#!/usr/bin/env python3.6
import logging
import time
import json
import os
from collections import OrderedDict
from math import ceil

from coinmarketcap import Market


class CoinmarketcapHelper:

    __DATA_FOLDER = './data'
    __CACHE_MINUTES = 30
    __FIRST_PRICE = False

    def __init__(self, convert_currency='USD', data_folder=__DATA_FOLDER, cache_minutes=__CACHE_MINUTES,
                 first_price=__FIRST_PRICE):
        self.first_price = first_price
        self.tickers = OrderedDict()
        self.symbols = OrderedDict()
        self.convert_currency = convert_currency.upper()
        self.tickers_path = f'{data_folder}/tickers/coinmarketcap_tickers_{self.convert_currency}.json'
        self.symbols_aliases_path = f'{data_folder}/coinmarketcap_symbols_aliases.json'
        self.coins_aliases_path = f'{data_folder}/coinmarketcap_coins_aliases.json'
        self.symbols_path = f'{data_folder}/coinmarketcap_symbols.json'
        self.symbols_conflicting_path = f'{data_folder}/coinmarketcap_symbols_conflicting.json'
        os.makedirs(os.path.dirname(self.tickers_path), exist_ok=True)
        self.coinmarketcap = Market()
        self._initialize(cache_minutes)

        self.symbols_aliases = self._load_dict_from_json(self.symbols_aliases_path)
        self.coins_aliases = self._load_dict_from_json(self.coins_aliases_path)

    def _initialize(self, cache_minutes=__CACHE_MINUTES):
        """Load tickers json or if it's missing or older than `cache_minutes`, re-download it"""
        download_tickers = True
        if os.path.exists(self.tickers_path):
            logging.debug(f'File {self.tickers_path} exists')
            date_now = time.time()
            file_date = os.path.getmtime(self.tickers_path)
            file_seconds_old = date_now - file_date
            # This will make sure that the file will be loaded if it was saved within 1 hour
            if file_seconds_old < cache_minutes * 60:
                logging.debug(f'File {self.tickers_path} is cached already.')
                self.tickers = json.load(open(self.tickers_path))
                download_tickers = False

        if download_tickers:
            listings = self.coinmarketcap.listings()
            total_listings = listings['metadata']['num_cryptocurrencies']
            hundreds = ceil(total_listings / 100)
            logging.debug(f'Downloading {total_listings} tickers with {hundreds} API calls...')
            tickers = OrderedDict()
            for i in range(hundreds):
                start_rank = i * 100 + 1
                logging.debug(f'Downloading from rank {start_rank} to {start_rank + 99}...')
                partial_tickers = self.coinmarketcap.ticker(start=start_rank, limit=100, convert=self.convert_currency)
                tickers.update(partial_tickers['data'])

            self._process_tickers(tickers)
            with open(self.tickers_path, 'w') as f:
                f.write(json.dumps(self.tickers, indent=2))
            logging.debug(f'Downloading tickers: done.')
            self.tickers = tickers

        if self.symbols == {}:
            self.symbols = json.load(open(self.symbols_path))

    def _process_tickers(self, tickers):
        """
        Create a dictionary of info (name + id) by symbol, save it as json (for caching purposes, to be loaded at each
        initialization) and save also conflicting symbols (used by several cyptocurrencies)
        """
        non_unique_symbols = OrderedDict()
        symbols_ranked = OrderedDict()
        for ticker in tickers.values():
            # Add to tickers dictionary (key = coinmarketcap id)
            id = ticker['id']
            self.tickers[id] = ticker

            # Add symbol_info (name + id) to symbols dictionary
            symbol = ticker['symbol']
            symbol_info = self._convert_to_symbol_info(ticker)
            symbol_ranked = symbols_ranked.get(symbol)
            # If the symbol is found, it means that this is a non unique symbol
            if symbol_ranked is not None:
                # If it's not found this dict, then we add a list of 2 elements (first crypto and this crypto)
                if non_unique_symbols.get(symbol) is None:
                    non_unique_symbols[symbol] = [symbol_ranked, symbol_info[1]]
                else:
                    non_unique_symbols[symbol].append(symbol_info[1])

                if not isinstance(symbol_ranked, list):
                    symbol_ranked = [symbol_ranked]
                symbol_ranked.append(symbol_info[1])
                symbols_ranked[symbol] = symbol_ranked
            else:
                symbols_ranked[symbol] = symbol_info[1]

        # Save symbols sorted alphabetically
        self.symbols = OrderedDict(sorted(symbols_ranked.items(), key=lambda t: t[0]))
        with open(self.symbols_path, 'w') as f:
            f.write(json.dumps(self.symbols, indent=2))

        # Save non unique symbols sorted alphabetically
        non_unique_symbols_sorted = OrderedDict(sorted(non_unique_symbols.items(), key=lambda t: t[0]))
        if len(non_unique_symbols) > 0:
            with open(self.symbols_conflicting_path, 'w') as f:
                f.write(json.dumps(non_unique_symbols_sorted, indent=2))
            logging.debug('The following symbols are not unique: ' + ','.join(sorted(non_unique_symbols_sorted)))

    @staticmethod
    def _load_dict_from_json(json_path):
        if os.path.exists(json_path):
            return json.load(open(json_path))
        else:
            return {}

    @staticmethod
    def _convert_to_symbol_info(ticker):
        """Convert a ticker to symbol_info by extracting symbol, name and id"""
        id = ticker['id']
        name = ticker['name']
        symbol = ticker['symbol']
        result = [symbol, {'name': name, 'id': id}]
        return result

    def _get_symbol_info(self, symbol):
        """Get symbol info, `None` if the symbol is not found, or a list if many coins use the same symbol"""
        symbol = symbol.upper()
        alias = self.symbols_aliases.get(symbol)
        symbol_info = self.symbols.get(alias or symbol)
        if symbol_info is None:
            logging.error(f'Currency {symbol} not found in our coinmarketcap list.')
            return None
        return symbol_info

    def _get_ticker_price(self, ticker):
        return float(ticker['quotes'][self.convert_currency]['price'])

    def get_coin_id(self, symbol):
        """Get symbol id, `None` is the symbol is not found, or a list if many coins use the same symbol"""
        currency_info = self._get_symbol_info(symbol)
        if currency_info is None:
            return None

        if isinstance(currency_info, list):
            return currency_info

        return currency_info['id']

    def get_price(self, symbol, get_first=None):
        """
        Get price by symbol

        :param symbol: coin symbol, e.g. BTC, ETH, LTC
        :param get_first: if true, if a symbol is used by several coins, it will return the price of the first coin,
        else it will return a list of symbol_info (coin id and name) including also the price
        :return: None, a price or a list of symbol_info with price
        """
        get_first = get_first or self.first_price

        currency_id = self.get_coin_id(symbol)
        if currency_id is None:
            return None

        if not isinstance(currency_id, list):
            ticker = self.tickers[str(currency_id)]
            return self._get_ticker_price(ticker)
        else:
            if get_first:
                ticker = self.tickers[str(currency_id[0]['id'])]
                return self._get_ticker_price(ticker)
            else:
                for currency_info in currency_id:
                    currency_info_id = currency_info['id']
                    ticker = self.tickers[str(currency_info_id)]
                    price = self._get_ticker_price(ticker)
                    currency_info.update({'price': price})
                return currency_id

    def get_symbol_by_name(self, name):
        """Get symbol by coin name"""
        alias = self.coins_aliases.get(name.lower())
        search_name = (alias or name).lower()
        result = None
        for symbol, symbol_info in self.symbols.items():
            if not isinstance(symbol_info, list):
                symbol_info = [symbol_info]

            for info in symbol_info:
                if info['name'].lower() == search_name:
                    result = symbol
                    break
        return result
