import datetime
import time
import json
import os
from collections import OrderedDict
import urllib.request
from bs4 import BeautifulSoup

COINMARKETCAP_ALL_URL = 'https://coinmarketcap.com/all/views/all/'

EXAMPLE_TD = '<td class="no-wrap currency-name" data-sort="Bitcoin Gold">' \
             '<div class="s-s-2083 currency-logo-sprite"></div>' \
             '<span class="currency-symbol"><a href="/currencies/bitcoin-gold/">BTG</a></span>' \
             '<a class="currency-name-container" href="/currencies/bitcoin-gold/">Bitcoin Gold</a>' \
             '</td>'


def main():
    html_temp_file = 'temp/coinmarketcap_all.html'
    if os.path.exists(html_temp_file):
        date_now = time.time()
        html_temp_file_date = os.path.getmtime(html_temp_file)
        html_temp_file_seconds_old = date_now - html_temp_file_date
        # This will make sure that the file won't be re-downloaded if it's not older than 1 hour
        if html_temp_file_seconds_old > 60*60:
            urllib.request.urlretrieve(COINMARKETCAP_ALL_URL, html_temp_file)
    else:
        urllib.request.urlretrieve(COINMARKETCAP_ALL_URL, html_temp_file)

    with open(html_temp_file, 'r') as f:
        page = f.read()

    soup = BeautifulSoup(page, 'html.parser')

    result = {}
    errors = []
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        td = row.findAll('td')[1]
        symbol_info = get_symbol_info(td)
        symbol = symbol_info[0]
        symbol_value = result.get(symbol)
        if symbol_value is not None:
            errors.append(f"{symbol}: {symbol_value} / {symbol_info[1]}")
            if not isinstance(symbol_value, list):
                symbol_value = [symbol_value]
            symbol_value.append(symbol_info[1])
            result[symbol_info[0]] = symbol_value
        else:
            result[symbol_info[0]] = symbol_info[1]

    ordered_result = OrderedDict(sorted(result.items(), key=lambda t: t[0]))

    with open('data/coinmarketcap_symbols.json', 'w') as f:
        f.write(json.dumps(ordered_result, indent=2))

    if len(errors) > 0:
        raise Exception('The following symbols were conflicting: \n' + '\n'.join(errors))


def get_symbol_info(td):
    """
    Get an array containing
    0:
    - symbol: e.g. BTG

    1: dictionary containing:
    - name (official name): e.g. Bitcoin Gold
    - api_name (to query the coinmarketcap API): e.g. bitcoin-gold

    >>> get_symbol_info(BeautifulSoup(EXAMPLE_TD, 'html.parser').td)
    ['BTG', {'name': 'Bitcoin Gold', 'api_name': 'bitcoin-gold'}]
    """
    name = td['data-sort']
    symbol = td.span.get_text()
    api_name = td.a['href'].replace('/currencies/', '')[:-1]
    result = [symbol, {'name': name, 'api_name': api_name}]
    return result


if __name__ == '__main__':
    main()
