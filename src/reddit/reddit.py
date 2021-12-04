import json
import datetime
from collections import defaultdict
import os

from psaw import PushshiftAPI

from typing import List, Tuple

# This file does not get overwritten; results are appended to it
OUTPUT_FILE = "reddit.json"

SUBREDDITS = [
    "EtherMining", "Cryptocurrency", "Cryptocurrencies", "CryptoMarkets",
    "EthTrader", "Ethereum", "Bitcoin"
]

# If set to `True`, each day's JSON output will be divded into a separate
# list for each hour of time. Otherwise, there will only be a single list per
# day. See the README for more.
GROUP_BY_HOUR = False

COMMENTS_PER_SUBREDDIT_PER_HOUR_LIMIT = 10
START_YEAR = 2018
END_YEAR = 2021

api = PushshiftAPI()


def main():
	is_first_entry = False

	# If the output file is empty or doesn't exist, start the JSON list
	if not os.path.isfile(OUTPUT_FILE) or os.stat(OUTPUT_FILE).st_size == 0:
		with open(OUTPUT_FILE, "w") as file:
			file.write("[\n")
			is_first_entry = True

	limit = COMMENTS_PER_SUBREDDIT_PER_HOUR_LIMIT
	if GROUP_BY_HOUR == False:
		limit *= 24

	total_fetched_counts = defaultdict(int)

	for date in all_dates_in_year_range(START_YEAR, END_YEAR):
		for (start_time, end_time) in get_time_ranges_for_day(date):
			comments = []

			for subreddit in SUBREDDITS:

				results = get_comments(subreddit, start_time, end_time, limit)
				print(
				    f"{len(results)} from {subreddit} {start_time.strftime('%Y-%m-%dT%H')} to {end_time.strftime('%Y-%m-%dT%H')}"
				)
				total_fetched_counts[subreddit] += len(results)
				comments.extend(results)

			output_object = {
			    "date": date.strftime('%Y-%m-%d'),
			}

			if GROUP_BY_HOUR:
				output_object["hour"] = start_time.strftime('%Y-%m-%dT%H')

			output_object["comments"] = comments

			with open(OUTPUT_FILE, "a") as file:
				if not is_first_entry:
					file.write(",\n")

				file.write(json.dumps(output_object, indent="\t"))

				is_first_entry = False

	print(total_fetched_counts)

	with open(OUTPUT_FILE, "a") as file:
		file.write("\n]")


def get_comments(subreddit: str, start_time: datetime.datetime,
                 end_time: datetime.datetime, limit: int) -> List[dict]:
	last_timestamp = int(end_time.timestamp())
	comments = []
	while True:
		# We are limited to fetching 500 comments at a time, so after
		# each request, check the timestamp of the last comment, and only
		# fetch comments from before that timestamp in the next request
		results = list(
		    api.search_comments(limit=limit - len(comments),
		                        subreddit=subreddit,
		                        before=last_timestamp))
		for result in results:
			if (result.created_utc <= int(start_time.timestamp())):
				limit = 0  # Hack because Python doesn't have loop labels -_-
				break
			if (is_comment_valid(result)):
				comments.append(result)

		if len(results) == 0 or len(comments) >= limit:
			break
		last_timestamp = results[-1].created_utc

	comment_json_data = [{
	    "user": comment.author,
	    "subreddit": subreddit,
	    "timestamp": comment.created_utc,
	    "karma": comment.score,
	    "body": comment.body,
	} for comment in comments]

	return comment_json_data


def is_comment_valid(comment) -> bool:
	return (comment.author != "[deleted]" and
		comment.author != "PrinceKael") # Bot on /r/CryptoMarkets


def get_time_ranges_for_day(
    day: datetime.datetime
) -> List[Tuple[datetime.datetime, datetime.datetime]]:
	if GROUP_BY_HOUR:
		return [(day + datetime.timedelta(hours=hour),
		         day + datetime.timedelta(hours=hour + 1)) for hour in range(24)]
	else:
		return [(day, day + datetime.timedelta(days=1))]


def all_dates_in_year_range(start_year: int,
                            end_year: int) -> List[datetime.datetime]:
	dates = []
	for year in range(start_year, end_year + 1):
		for month in range(1, 13):
			for day in range(1, 32):
				try:
					date = datetime.datetime(year, month, day)
					if date > datetime.datetime.now():
						continue
					dates.append(date)
				except ValueError:
					pass
	return dates


if __name__ == "__main__":
	main()
