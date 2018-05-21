import logging

from coinmarketcap_helper.coinmarketcap_helper import CoinmarketcapHelper

FORMAT = "[%(asctime)s, %(levelname)s] %(message)s"
logging.basicConfig(filename='test.log', level=logging.DEBUG, format=FORMAT)


def test_btc_price():
    helper = CoinmarketcapHelper()
    symbol = 'BTC'
    price = helper.get_price(symbol)
    logging.info(f'{symbol} price: {price} {helper.convert_currency}')


def test_btg_price():
    helper = CoinmarketcapHelper()
    symbol = 'BTG'
    price = helper.get_price(symbol)
    logging.info(f'{symbol} price: {price} {helper.convert_currency}')


def test_btg_price_first():
    helper = CoinmarketcapHelper()
    symbol = 'BTG'
    price = helper.get_price(symbol, True)
    logging.info(f'{symbol} price: {price} {helper.convert_currency}')


def test_first_price_config_true():
    helper = CoinmarketcapHelper(first_price=True)
    symbol = 'BTG'
    price = helper.get_price(symbol)
    logging.info(f'{symbol} price: {price} {helper.convert_currency}')


def test_btc_price_eur():
    helper = CoinmarketcapHelper(convert_currency='EUR')
    symbol = 'BTC'
    price = helper.get_price(symbol)
    logging.info(f'{symbol} price: {price} {helper.convert_currency}')


def test_get_symbol_by_name():
    helper = CoinmarketcapHelper()
    name = 'Stellar Lumen'
    symbol = helper.get_symbol_by_name(name)
    assert symbol == 'XLM'


if __name__ == '__main__':
    test_btc_price()
    test_btg_price()
    test_btg_price_first()
    test_first_price_config_true()
    test_btc_price_eur()
    test_get_symbol_by_name()
