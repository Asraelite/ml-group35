# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1agt7w4XIBSMZZQwzTi5rksrcMxZzKwca
"""

import pandas as pd
import os
import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import LinearSVC
from sklearn import metrics
from sklearn.metrics import confusion_matrix, classification_report
from nltk.stem import PorterStemmer
import re

from sklearn.model_selection import KFold, train_test_split
import numpy as np
from sklearn.metrics import f1_score, mean_squared_error, accuracy_score, confusion_matrix, roc_curve
from sklearn.neighbors import KNeighborsClassifier
nltk.download('stopwords')

# change
BINANCE_DIR = "/content/drive/MyDrive/ML project data"
TWITTER_DIR = "/content/drive/MyDrive/ML project data"
REDDIT_DIR = "/content/drive/MyDrive/ML project data"

TWITTER_FILE = "twitter.csv"
REDDIT_FILE  = "reddit.csv"
BINANCE_FILE = "binance.csv"
# dont change
BINANCE_EXTENSION = "csv"

START_DATE = "2018-01-01"
END_DATE = "2021-10-31"

from google.colab import drive
drive.mount('/content/drive')


def concatenate_content_values(content_list):
	return content_list.str.cat(sep=" ")

"""# Dataset

### Binance
"""

# load binance data
df_binance = pd.read_csv(  os.path.join(BINANCE_DIR, BINANCE_FILE), lineterminator='\n' )

# convert time to date obj
df_binance['time'] = pd.to_datetime(df_binance['time'])

# change index to time
df_binance = df_binance.set_index('time')

# filter date range
df_binance = df_binance.loc[START_DATE:END_DATE]

df_binance.head()

"""### Reddit"""

# read reddit
df_reddit = pd.read_csv(  os.path.join(REDDIT_DIR, REDDIT_FILE), lineterminator='\n' )

# convert to date obj
df_reddit['date'] = pd.to_datetime(df_reddit['date'])

# Join all reddit posts for each day into one big string
df_reddit = df_reddit.groupby("date").aggregate({
    "content": concatenate_content_values,
    "popularity" : "sum"
})

# filter date range
df_reddit = df_reddit.loc[START_DATE:END_DATE]

df_reddit.head()

"""### Twitter"""

# load twitter data
df_twitter = pd.read_csv( os.path.join(TWITTER_DIR, TWITTER_FILE), lineterminator="\n")

# convert to date obj
df_twitter['date'] = pd.to_datetime(df_twitter['date'])

# Join all tweets for each day into one big string
df_twitter = df_twitter.groupby("date").aggregate({
    "content": concatenate_content_values,
    "popularity" : "sum"
})

# filter date range
df_twitter = df_twitter.loc[START_DATE:END_DATE]

df_twitter.head()

input_data = pd.concat([df_reddit,df_twitter]).groupby("date").aggregate({
    "content": concatenate_content_values,
    "popularity" : "sum"
})

daily_content = input_data.content

daily_content

"""## Preprocess Data"""

# check if there exist any empty column
daily_content.isna().sum()

"""## Prunning"""

stemmer = PorterStemmer()

# Adding stemmming with CountVectorizer
# https://stackoverflow.com/questions/36182502/add-stemming-support-to-countvectorizer-sklearn
analyzer = CountVectorizer().build_analyzer()
def stemmed_words(doc):
    words = []
    for w in analyzer(doc):
        
        # remove words with number
        if len(re.findall('\d+', w)) > 0:
            continue
        
        # only english letters
        w=re.sub('[^a-zA-Z]','',w)    
        if w == '':
            continue
        
        # stemming 
        stemmed_word = stemmer.stem(w)
        
        words.append(stemmed_word)
    return words

# prunning
vectorizer = CountVectorizer(
    ngram_range=(1, 1),
    stop_words=nltk.corpus.stopwords.words("english"),
    min_df=0.1,
    max_df=1.0,
    analyzer=stemmed_words
)

x = vectorizer.fit_transform(daily_content)

print(f"{len(vectorizer.get_feature_names())} features")

y = df_binance.label

"""### Training"""

y[y == 0] = 1

Xtrain, Xtest, ytrain, ytest = train_test_split(x,y,test_size=0.2)

best_models = {}
scores_avg = {}

from sklearn.model_selection import KFold, train_test_split
import numpy as np
from sklearn.metrics import f1_score, mean_squared_error, accuracy_score, confusion_matrix, roc_curve
from sklearn.neighbors import KNeighborsClassifier
for k in range(5,701, 5):
        print(k)
        kf = KFold(n_splits=5)
        scores = []
        for train, test in kf.split(x):
            model = KNeighborsClassifier(n_neighbors=k, weights='uniform')
            model.fit(x[train], y[train])
            pred = model.predict(x[test])
            scores.append(f1_score(y[test], pred))
        scores_avg[k] = sum(scores)/len(scores)
    
print(f'Dictionary with average f1 scores for every value of k: {scores_avg}')

for k, score in scores_avg.items():
    if score == max(list(scores_avg.values())):
        optmial_k = k
        print(f'optimal: k={optmial_k}, f1 score={score}')
        break

FIXED_k = 550
print(FIXED_k)
knn_model = KNeighborsClassifier(n_neighbors=FIXED_k, weights='uniform')
knn_model.fit(Xtrain, ytrain)
knn_model_prediction = knn_model.predict(Xtest)
knn_model_confusion_matrix = confusion_matrix(ytest, knn_model_prediction)
knn_model_accuracy = np.sum(knn_model_confusion_matrix.diagonal()) / np.sum(knn_model_confusion_matrix)

import matplotlib.pyplot as plt

plt.plot( list(scores_avg.keys()), list(scores_avg.values()))
plt.xlabel('n neighbors')
plt.ylabel('f1 score')
plt.title('f1 score vs number of neighbors considered')
plt.show()

