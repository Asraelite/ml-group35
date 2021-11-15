import json
import time
from collections import defaultdict

from psaw import PushshiftAPI

SUBREDDITS = [
    "EtherMining",
    "Cryptocurrency",
    "Cryptocurrencies",
    "CryptoMarkets",
    "EthTrader",
    "Ethereum",
    "Bitcoin"
]

# This file does not get overwritten; results are appended to it
OUTPUT_FILE = "reddit.json"
SUBREDDIT_COMMENT_LIMIT = 30_000

api = PushshiftAPI()

total_fetched_counts = defaultdict(int)

for subreddit in SUBREDDITS:
	with open(OUTPUT_FILE, "a") as file:
		last_timestamp = None
		comments = []
		while True:
			# We are limited to fetching 500 comments at a time, so after
			# each request, check the timestamp of the last comment, and only
			# fetch comments from before that timestamp in the next request
			print(f"{last_timestamp} {subreddit}")
			results = list(
			    api.search_comments(limit=500,
			                        subreddit=subreddit,
			                        before=last_timestamp))
			comments.extend(results)
			if len(results) == 0 or len(comments) >= SUBREDDIT_COMMENT_LIMIT:
				break
			last_timestamp = comments[-1].created_utc
		
		total_fetched_counts[subreddit] += len(comments)

		comment_json_data = [{
		    "subreddit": subreddit,
		    "timestamp": comment.created_utc,
		    "karma": comment.score,
		    "body": comment.body,
		} for comment in comments if comment.author != "[deleted]"]

		file.write(json.dumps(comment_json_data) + "\n")

print("Total comments fetched:")
for subreddit, count in total_fetched_counts.items():
	print("  {}: {}".format(subreddit, count))
