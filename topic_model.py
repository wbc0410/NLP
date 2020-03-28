# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 11:33:12 2020

@author: chest
"""

from os import chdir
import gensim
import pandas as pd
import re
import pickle
import numpy as np
import random
import nltk

import logging
from logging import basicConfig, INFO
from gensim import corpora
from operator import itemgetter
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt

#system level config
chdir(r"C:\Users\chest\Desktop\Projects\Restaurant Chatbot\data")
basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)

#load restaurant reviews
with open(r"restReview_df.pkl", "rb") as file:
    reviews = pickle.load(file)

#random sample the reviews
random.seed(888)
reviews_sample = random.sample(list(reviews.index), 1000) 
reviews = reviews.iloc[reviews_sample, :]
reviews.reset_index(inplace=True, drop=True)

#condition for pos
def get_pos(x):    
    condlist = [x<3, x==3, x>3]
    choicelist = [-1,0,1]
    return np.select(condlist, choicelist)

reviews["pos"] = reviews.stars.apply(lambda x: get_pos(x))

pos = reviews[reviews.pos == 1]
neutral = reviews[reviews.pos == 0]
neg = reviews[reviews.pos == -1]

#pre-processing for negative
nltk_stopwords = stopwords.words("english")
additional_stopwords = ["got", "make", "first", "still",
                        "two", "one", "thing", "went",
                        "much", "n't", "does", "do",
                        "many", "something", "great",
                        "review", "even", "worst",
                        "hotel", "ve", "customer",
                        "right", "well", "bad",
                        "back", "minute", "anything",
                        "sure", "big", "wanted",
                        "want", "really", "finally",
                        "good", "best", "worst",
                        "bad", "took", "star",
                        "try", "doe", "think", 
                        "through", "horrible", "would",
                        "could", "like", "table",
                        "restaurant", "place", "never",
                        "came", "come", "friend", "way",
                        "going", "told", "ordered",
                        "get", "said", "people",
                        "better", "order", "also",
                        "\'ve", "another", "since",
                        "always", "eat", "ever",
                        "day", "though", "else"]

total_stopwords = nltk_stopwords + additional_stopwords
WNlemma = nltk.WordNetLemmatizer()

def pre_process(text, mystopwords):
    tokens = nltk.word_tokenize(text)
    tokens=[ WNlemma.lemmatize(t.lower()) for t in tokens]
    tokens=[ t for t in tokens if t not in mystopwords]
    tokens = [ t for t in tokens if len(t) >= 3 ]
    result = " ".join(tokens)
    return result

def tokenize_process(result):
    tokens = nltk.word_tokenize(result)
    return tokens

#Text Exploration
processed_text = neg["text"].apply(lambda x: pre_process(x, total_stopwords))
total_str = processed_text.str.cat(sep = " ")


# Create and generate a word cloud image:
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(total_str)
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

neg_reviews = neg.text.apply(lambda x: tokenize_process(pre_process(x, total_stopwords)))

#GENSIM Topic Model

#Dictionary FIltering
dictionary = corpora.Dictionary(neg_reviews)
total_doc = neg_reviews.shape[0]
min_percentage = 0.05
min_doc = round(total_doc * min_percentage)
max_doc = 0.4
dictionary.filter_extremes(no_below=min_doc, no_above=max_doc)

#Establish Document Term Matrix
dtm = [dictionary.doc2bow(d) for d in neg_reviews]

lda = gensim.models.ldamodel.LdaModel(dtm, num_topics = 5, id2word = dictionary, random_state=432)
lda.show_topics(num_words=10)

