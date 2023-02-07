#!/usr/bin/env python
# coding: utf-8

# In[246]:


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import  StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
import os


# In[183]:


# read-in all lyric files, append to text corpus and append artist to tag-list

directory = 'lyrics/'
all_lyrics = []
all_tags = []

print('Number of Songs:', len(os.listdir(directory)), '\n')

for file_name in os.listdir(directory):
    #print('\r' + file_name)
    file = open((directory + file_name), 'r')
    lines = file.read()
    artist_name = file_name[:file_name.find(' ')]
    all_lyrics.append(lines)
    all_tags.append(artist_name)


# In[212]:


# vectorize bag of words

vectorizer = TfidfVectorizer(stop_words='english', max_df=0.75)#, ngram_range=(1,2))
X = vectorizer.fit_transform(all_lyrics)
X = X.toarray()
y = all_tags


# In[248]:


#X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.05)

#parameters = {'alpha':np.arange(1, 0.01, -0.02)}
model = MultinomialNB(alpha=0.05)
#gs = GridSearchCV(model, param_grid=parameters)
#gs.fit(X,y)
#gs.best_params_
#model = gs.best_estimator_
model.fit(X, y)
model.score(X, y)


# In[266]:


# test

#test_lines = [
#    'beat it',
#    'I wanna rock with you',
#    "Because I'm bad",
#    'Tarnish point of the supreme Is it the strength of your fearless over throwing your pain',
#    'prince minikid',
#    'The grain of pixel equation',
#    'yellow submarine',
#    'a hard days night',
#    'I love you',
#    'walking on the moon',
#    'every breath you take',
#    'A man owns a big house'
#]
while 1:
    print('Please input a test line:')
    test_line = [input()]
    X_test = vectorizer.transform(test_line)
    print(model.predict(X_test))

