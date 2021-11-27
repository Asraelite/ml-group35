import numpy
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import KFold
import numpy as np
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier

DATASET_CSV_FILE = "twitter.csv"
BINANCE_CSV_FILE = "binance.csv"

# [time, price_mean, price_std, qty, label]
price_dataframe = pandas.read_csv(BINANCE_CSV_FILE, lineterminator="\n")

# [date, category, popularity, content]
input_dataframe = pandas.read_csv(DATASET_CSV_FILE, lineterminator="\n")

# Ignore tweets after October 2021
input_dataframe = input_dataframe[input_dataframe["date"] < "2021-11-01"]


def concatenate_content_values(content_list):
    return content_list.str.cat(sep=" ")


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
    ngram_range=(1, 1),  # bigrams=(2,2)
    stop_words="english",
    min_df=0.01,
    max_df=1.0)

vectorizer.get_feature_names()

len(vectorizer.get_feature_names())

x_values = vectorizer.fit_transform(daily_content)
y_values = price_dataframe["label"]

print(f"{len(vectorizer.get_feature_names_out())} features")

x_train = x_values[:-280]
y_train = y_values[:-280]
x_test = x_values[-280:]
y_test = y_values[-280:]

best_models = {}
scores_avg = {}

for k in range(1, 100):
    kf = KFold(n_splits=5)
    scores = []
    for train, test in kf.split(x_values):
        model = KNeighborsClassifier(n_neighbors=k, weights='uniform')
        model.fit(x_values[train], y_values[train])
        pred = model.predict(x_values[test])
        scores.append(f1_score(y_values[test], pred, average='micro'))
    scores_avg[k] = sum(scores) / len(scores)

print(f'Dictionary with average f1 scores for every value of k: {scores_avg}')

for k, score in scores_avg.items():
    if score == max(list(scores_avg.values())):
        optmial_k = k
        print(f'optimal: k={optmial_k}, f1 score={score}')
        break

knn_model = KNeighborsClassifier(n_neighbors=65, weights='uniform')
knn_model.fit(x_train, y_train)
knn_model_prediction = knn_model.predict(x_test)
knn_model_confusion_matrix = confusion_matrix(y_test, knn_model_prediction)
knn_model_accuracy = numpy.sum(knn_model_confusion_matrix.diagonal()) / numpy.sum(knn_model_confusion_matrix)

print(f1_score(y_test, knn_model_prediction, average='micro'))
