# ml-group35

## Contents
1. Generating dataset  
  1.1 [Binance Trade Data](#binance-trade-data)  
2. 

## Generating dataset

### Binance Trade Data
Binance provides past history data and repository to download them. Link to report [Binance Public Data Git](https://github.com/binance/binance-public-data)
```
$ cd binance/python && python download-trade.py -s ETHUSDT
```

The trade data consists records of every trade for ETHUSDT, [preprocess_binance.py](binance/preprocess_binance.py) groups trade by hours output mean price, std price and qty sum.
```
$ cd binance && python preprocess_binance.py --data ../data/binance/raw/monthly/ETHUSDT-trades-2021-06.csv --output ../data/binance/processed/ETHUSDT-trades-2021-06-processed.csv
```