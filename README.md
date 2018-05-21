# coinmarketcap-helper

This is a helper to get a cryptocurrency price on [coinmarketcap.com](https://coinmarketcap.com) by its symbol.

In fact the [python coinmarketcap API](https://github.com/barnumbirr/coinmarketcap) based on the [official coinmarketcap API](https://coinmarketcap.com/api/) inconveniently wants you to pass as parameter the coinmarketcap cryptocurrency id (which in v1, in most cases it was the cryptocurrency name, lowercase, with spaces converted to dashes, e.g. `bitcoin-gold` for _Bitcoin Gold_; in the actual v2 it's a numerical id).
 
Most exchanges provide their cryptocurrencies pairs with a symbol. So, I think it's more practical to query coinmarketcap by symbol, e.g. `BTG` for _Bitcoin Gold_.

This library saves the following files in the `data` folder (situated in your working directory):

- [coinmarketcap_symbols.json](https://raw.githubusercontent.com/firepol/coinmarketcap-helper/master/data/coinmarketcap_symbols.json): this is the file containing a dictionary (key: `symbol`, value: a dictionary containing `id` and `name`) of all the cryptocurrencies available on coinmarketcap.com
- [coinmarketcap_symbols_aliases.json](https://raw.githubusercontent.com/firepol/coinmarketcap-helper/master/data/coinmarketcap_symbols_aliases.json): some symbols weren't found, e.g. _IOTA_, _YOYO_. If you try to get a price by an alias, you will get a result if the alias is in this file.
- [coinmarketcap_coins_aliases.json](https://raw.githubusercontent.com/firepol/coinmarketcap-helper/master/data/coinmarketcap_coins_aliases.json): some coins are known with different names, e.g. _Stellar Lumen_ simply as _Steller_. If you try to get a symbol by the coin name (e.g. as fallback if the symbol is not found), you will get a result if the alias is in this file.
- [coinmarketcap_symbols_conflicting.json](https://raw.githubusercontent.com/firepol/coinmarketcap-helper/master/data/coinmarketcap_symbols_conflicting.json): cryptocurrencies using the same symbol used by another cryptocurrency.
## Testing

To test this library, you can use **pytest**:

```
pip install pytest
cd coinmarketcap_helper
pytest
```

## Known issues

### Cryptocurrencies using the same symbol

Several coins share the same symbol e.g. CAT (BitClave, BlockCAT, Catcoin), BTG (Bitcoin Gold, Bitgem) etc.

Now, if you query the price for such a symbol, by default you get a list, sorted by ranking. This can lead to wrong results, especially if you own bad ranked altcoins. You must implement your own logic to deal with such cases, as every user must know which coins he is handling.

### Symbols aliases

The `symbols_aliases.json` file is incomplete: I will try to update it in a semi-automatic way...
