# Coinmarketcap scraper

A little script to get all the crypto currencies listed on [coinmarketcap.com](https://coinmarketcap.com), by symbol.

I needed this, because the coinmarketcap API inconveniently wants you to pass as parameter the cryptocurrency name, instead of (more practical) the symbol.

Here the result, feel free to download or link to this file: [coinmarketcap_symbols.json](https://raw.githubusercontent.com/firepol/coinmarketcap-scraper/master/data/coinmarketcap_symbols.json)

Example:

```
{
  ...
  "SBTC": {
    "name": "Super Bitcoin",
    "api_name": "super-bitcoin"
  },
  ...
}
```

TODO: there are symbols used by different cryptocurrencies. E.g. CAT (BitClave and BlockCAT), BTG (Bitgem, Bitcoin Gold)

Thanks to [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for making the scraping of the website a piece of cake ;)