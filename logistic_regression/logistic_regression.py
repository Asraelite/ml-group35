import numpy
import pandas
from matplotlib import pyplot
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
from sklearn.dummy import DummyClassifier

from typing import List, Tuple

DATASET_CSV_FILE = "/home/asraelite/College/4y2/Modules/Machine Learning/Group Project/scraping/twitter.csv"
BINANCE_CSV_FILE = "/home/asraelite/College/4y2/Modules/Machine Learning/Group Project/scraping/binance.csv"


def main():
	# [time, price_mean, price_std, qty, label]
	price_dataframe = pandas.read_csv(BINANCE_CSV_FILE, lineterminator="\n")

	# [date, category, popularity, content]
	input_dataframe = pandas.read_csv(DATASET_CSV_FILE, lineterminator="\n")

	# Ignore tweets after October 2021
	input_dataframe = input_dataframe[input_dataframe["date"] < "2021-11-01"]

	# Join all tweets for each day into one big string
	daily_dataframe = input_dataframe.groupby("date").aggregate({
	    "content": concatenate_content_values,
	    "popularity": "sum"
	})
	daily_content = daily_dataframe["content"]

	print(f"{len(input_dataframe)} tweets")
	print(f"{len(daily_dataframe)} days")
	print("Creating n-grams")

	# feature counts:
	# min_df=0.1: 2913
	# min_df=0.01: 16177 (~2 minutes to run)

	vectorizer = CountVectorizer(
	    ngram_range=(1, 1), # bigrams=(2,2)
	    stop_words="english",
	    min_df=0.01,
	    max_df=1.0)

	x_values = vectorizer.fit_transform(daily_content)
	y_values = price_dataframe["label"]

	print(f"{len(vectorizer.get_feature_names_out())} features")

	x_train = x_values[:-300]
	y_train = y_values[:-300]
	x_test = x_values[-300:]
	y_test = y_values[-300:]

	model = LogisticRegression(max_iter=5000)
	model.fit(x_train, y_train)
	model_prediction = model.predict(x_test)
	model_confusion_matrix = confusion_matrix(y_test, model_prediction)
	model_accuracy = numpy.sum(model_confusion_matrix.diagonal()) / numpy.sum(model_confusion_matrix)

	common_baseline_model = DummyClassifier(strategy="most_frequent")
	common_baseline_model.fit(x_train, y_train)
	common_baseline_prediction = common_baseline_model.predict(x_test)
	common_baseline_confusion_matrix = confusion_matrix(y_test, common_baseline_prediction)
	common_baseline_accuracy = numpy.sum(common_baseline_confusion_matrix.diagonal()) / numpy.sum(common_baseline_confusion_matrix)

	random_baseline_model = DummyClassifier(strategy="uniform")
	random_baseline_model.fit(x_train, y_train)
	random_baseline_prediction = random_baseline_model.predict(x_test)
	random_baseline_confusion_matrix = confusion_matrix(y_test, random_baseline_prediction)
	random_baseline_accuracy = numpy.sum(random_baseline_confusion_matrix.diagonal()) / numpy.sum(random_baseline_confusion_matrix)

	print("regression:")
	print(model_confusion_matrix)
	print(f"accuracy: {model_accuracy}")

	print("most frequent baseline:")
	print(random_baseline_confusion_matrix)
	print(f"accuracy: {common_baseline_accuracy}")

	print("random baseline:")
	print(random_baseline_confusion_matrix)
	print(f"accuracy: {random_baseline_accuracy}")


def concatenate_content_values(content_list):
	return content_list.str.cat(sep=" ")


if __name__ == "__main__":
	main()
