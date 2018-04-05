import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

COINMARKETCAP_ALL_URL = 'https://coinmarketcap.com/all/views/all/'

EXAMPLE_TD = '<td class="no-wrap currency-name" data-sort="Bitcoin Gold">' \
             '<div class="s-s-2083 currency-logo-sprite"></div>' \
             '<span class="currency-symbol"><a href="/currencies/bitcoin-gold/">BTG</a></span>' \
             '<a class="currency-name-container" href="/currencies/bitcoin-gold/">Bitcoin Gold</a>' \
             '</td>'


def main():
    page = urlopen(COINMARKETCAP_ALL_URL).read()
    soup = BeautifulSoup(page, 'html.parser')

    result = {}
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        td = row.findAll('td')[1]
        symbol_info = get_symbol_info(td)
        result[symbol_info[0]] = symbol_info[1]

    with open('data/coinmarketcap_symbols.json', 'w') as f:
        f.write(json.dumps(result, indent=2))


def get_symbol_info(td):
    """
    Array containing
    0:
    - symbol: e.g. BTG

    1: dictionary containing:
    - name (official name): e.g. Bitcoin Gold
    - api_name (to query the coinmarketcap API): e.g. bitcoin-gold

    >>> get_symbol_info(BeautifulSoup(EXAMPLE_TD, "html.parser").td)
    ['BTG', {'name': 'Bitcoin Gold', 'api_name': 'bitcoin-gold'}]
    """
    name = td['data-sort']
    symbol = td.span.get_text()
    api_name = get_url_friendly_text(name)
    result = [symbol, {'name': name, 'api_name': api_name}]
    return result


def get_url_friendly_text(text):
    """
    >>> get_url_friendly_text('Test Coin')
    'test-coin'
    """
    return text.lower().replace(' ', '-')


if __name__ == '__main__':
    main()
