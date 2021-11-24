import snscrape.modules.twitter as sntwitter
import json
import datetime

# This file does not get overwritten; results are appended to it
OUTPUT_FILE = "twitter.json"

START_YEAR = 2018
END_YEAR = 2021

TWEETS_PER_DAY = 240

SEARCH_TERM = "Ethereum"


def main():
	dates = all_dates_in_year_range(2018, 2021)
	for i in range(len(dates) - 1):
		start_date = dates[i]
		end_date = dates[i + 1]
		get_tweets_for_date_range(start_date, end_date)

	print(dates)


# Return all dates in the given year range as strings in the format yyyy-mm-dd
def all_dates_in_year_range(start_year, end_year):
	dates = []
	for year in range(start_year, end_year + 1):
		for month in range(1, 13):
			for day in range(1, 32):
				try:
					date = datetime.datetime(year, month, day)
					if date > datetime.datetime.now():
						continue
					dates.append(date.strftime('%Y-%m-%d'))
				except ValueError:
					pass
	return dates


def get_tweets_for_date_range(start_date, end_date):

	query = f"{SEARCH_TERM} since:{start_date} until:{end_date}"
	query_result = sntwitter.TwitterSearchScraper(query)

	tweet_list = []
	for i, tweet in enumerate(query_result.get_items()):

		if i >= TWEETS_PER_DAY:
			break
		
		tweet_list.append({
			"timestamp": int(tweet.date.timestamp()),
			"id": tweet.id,
			"content": tweet.content,
			"user": tweet.user.username,
			"retweetCount": tweet.retweetCount,
			"likeCount": tweet.likeCount,
			"replyCount": tweet.replyCount
		})

	day_object = {
		"date": start_date,
		"tweets": tweet_list,
	}
	print(f"{len(tweet_list)} tweets for {start_date}")

	with open(OUTPUT_FILE, "a") as file:
		file.write(json.dumps(day_object, indent="\t") + ",\n")


if __name__ == "__main__":
	main()
