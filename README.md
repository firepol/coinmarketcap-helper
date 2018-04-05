# Coinmarketcap scraper

A little script to get all the crypto currencies listed on [coinmarketcap.com](https://coinmarketcap.com), by symbol.

I needed this, because the coinmarketcap API inconveniently wants you to pass as parameter the cryptocurrency name, instead of (more practical) the symbol.

Here the result, feel free to download or link to this file: [coinmarketcap_symbols.json](https://raw.githubusercontent.com/firepol/coinmarketcap-scraper/master/data/coinmarketcap_symbols.json)

To get the cryptocurrency name to be passed to the coinmarketcap API, first get the crypto currency name by symbol, then lower case the result and replace the spaces with a dash, like this (see `get_url_friendly_text` method in the `main.py` file):

```
>>> 'Coin Name'.lower().replace(' ', '-')
'coin-name'
```

Thanks to [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for making the scraping of the website a piece of cake ;)