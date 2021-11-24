# ml-group35

## Contents
1. Generating dataset  
  1.1 [Binance Trade Data](#binance-trade-data)  
  1.2 [Reddit comment data](#reddit-comment-data)
  1.3 [Twitter tweet data](#twitter-tweet-data)
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


### Reddit comment data

Poetry is used for package management. To initialize the dependencies and the venv, run `poetry install`.

```
$ cd reddit
$ poetry run python reddit.py
```

The boolean `GROUP_BY_HOUR` in the source code can be adjusted to `True` or `False`. If `True`, the output JSON will be in the format

```json
[
	{
		"date": "1900-01-01",
		"hour": "1900-01-01T00",
		"comments": [
			{
				"user": "reddit_userna,e",
				"subreddit": "Ethereum",
				"timestamp": 1515709116,
				"karma": 4,
				"body": "comment text here"
			},
			...
		]
	},
	...
]
```

If it is `False`, the "hour" field will be omitted and there will be only one entry per day.

### Twitter tweet data

Install with Poetry as with the Reddit scraper.

```
$ cd twitter
$ poetry run python twitter.py
```

The data is in the format

```json
[
	{
		"date": "1900-01-01",
		"tweets": [
			{
				"timestamp": 1514937599,
				"id": 948343144575270913,
				"content": "tweet text here",
				"user": "twitter_handle",
				"retweetCount": 0,
				"likeCount": 0,
				"replyCount": 0
			},
			...
		]
	},
	...
]
```
