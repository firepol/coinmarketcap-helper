# coinmarketcap-helper

This is a helper to get a cryptocurrency price on [coinmarketcap.com](https://coinmarketcap.com) by its symbol.

In fact the official [coinmarketcap API](https://github.com/barnumbirr/coinmarketcap) inconveniently wants you to pass as parameter the coinmarketcap cryptocurrency id (which in most cases is the cryptocurrency name, lowercase, with spaces converted to dashes, but in some cases it isn't), e.g. `bitcoin-gold` for _Bitcoin Gold_.
 
Most exchanges provide their cryptocurrencies pairs with a symbol. So, I think it's more practical to query coinmarketcap by symbol, e.g. `BTG` for _Bitcoin Gold_.

This library saves the following files in the `data` folder (situated in your working directory):

- [coinmarketcap_symbols.json](https://raw.githubusercontent.com/firepol/coinmarketcap-helper/master/data/coinmarketcap_symbols.json): this is the file containing a dictionary (key: `symbol`, value: a dictionary containing `id` and `name`) of all the cryptocurrencies available on coinmarketcap.com
- [symbols_aliases.json](https://raw.githubusercontent.com/firepol/coinmarketcap-helper/master/data/symbols_aliases.json):  some symbols weren't found, e.g. _IOTA_, _YOYO_. I added them here.

## Known issues

Several symbols used by different cryptocurrencies. E.g. CAT (BitClave and BlockCAT), BTG (Bitgem, Bitcoin Gold) etc. now, by default you will get the first one in the list, sorted by ranking. This can lead to wrong results, especially if you own bad ranked altcoins.


The `symbols_aliases.json` file is incomplete: I will try to update it in a semi-automatic way...