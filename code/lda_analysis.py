from gensim import corpora
from six import iteritems
import re
import codecs
import copy
from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from gensim.models import LdaModel, CoherenceModel
import numpy as np
import pyLDAvis
import pyLDAvis.gensim_models
import os
import random
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

sandwiches = pd.read_csv('D:/yelp data/yelp_data/sandwiches_review_1202.csv')
good_rew = sandwiches[sandwiches['stars_x']==5]['text'].tolist()
bad_rew = sandwiches[(sandwiches['stars_x']== 1) | (sandwiches['stars_x'] == 2)]['text'].tolist()
good_rew_date = sandwiches[sandwiches['stars_x']==5]['date'].tolist()
bad_rew_date = sandwiches[(sandwiches['stars_x']== 1) | (sandwiches['stars_x'] == 2)]['date'].tolist()

def date_month(x):
    month_data = list(re.match('([0-9]{4})-([0-9]{2})-([0-9]{2})', x).groups())[1]
    return int(month_data)

def date_year(x):
    year_data = list(re.match('([0-9]{4})-([0-9]{2})-([0-9]{2})', x).groups())[0]
    return int(year_data)

date_good = sandwiches[sandwiches['stars_x']==5]['date'].tolist()
date_bad =  sandwiches[(sandwiches['stars_x']== 1) | (sandwiches['stars_x'] == 2)]['date'].tolist()
good_year = list(map(lambda x: date_year(x),date_good))
bad_year = list(map(lambda x: date_year(x),date_bad))
good_month = list(map(lambda x: date_month(x),date_good))
bad_month = list(map(lambda x: date_month(x),date_bad))

## drop stopwords
stopwords = pd.read_csv('D:/yelp data/yelp_data/stopwords.txt')
stopwords = stopwords['stopwords'].tolist()
stopwords = [i for i in stopwords if i!=""]

def cleanwords(sentences):
    #sentences = sentences.replace("\\u3000", "").replace("%", "").replace("+", "").replace(".", "").replace("\n","\xa0", "")
    sentences = re.sub('[0-9]', "", sentences)  ## 去掉语料中的数字与字母
    sentences = re.sub(r'[^\w\s]', '', sentences)
    #sentences = re.sub("[^a-zA-Z]", '', sentences)
    sentences = sentences.lower()
    sentences = sentences.split()
    sentences = [i for i in sentences if i not in stopwords]
    sentences = list(map(lambda x: wnl.lemmatize(x, 'n'), sentences)) #还原名词:例如cars变为car
    sentences = list(map(lambda x: wnl.lemmatize(x, 'v'), sentences)) #还原动词:例如went变为go
    doc_length = len(sentences)
    sentences = " ".join(sentences)
    return sentences,doc_length

"""
sentences = re.sub('[0-9]', "", good_rew[1])
sentences = ['cars','goes','eats','hours','went']
sentences = list(map(lambda x: wnl.lemmatize(x,'v'),sentences))
sentences = list(map(lambda x: wnl.lemmatize(x,'n'),sentences))
print(sentences)
"""
good_rew = list(map(lambda x: cleanwords(x), good_rew))
bad_rew = list(map(lambda x: cleanwords(x), bad_rew))

df_good = pd.DataFrame(good_rew,columns=['text','doclength'])
df_bad = pd.DataFrame(bad_rew,columns=['text','doclength'])
df_good['year'] = good_year
df_good['month'] = good_month
df_bad['year'] = bad_year
df_bad['month'] = bad_month
#df_good.to_csv("D:/yelp data/yelp_data/good_review.csv")
#df_bad.to_csv("D:/yelp data/yelp_data/bad_review.csv")
df_good = pd.read_csv('D:/yelp data/yelp_data/good_review.csv',encoding = "ISO-8859-1")
df_bad = pd.read_csv('D:/yelp data/yelp_data/bad_review.csv',encoding = "ISO-8859-1")
df_good = df_good[df_good['doclength']>=20]
df_bad = df_bad[df_bad['doclength']>=20]

#
df_good_spr = df_good[(df_good['month']==3)|(df_good['month']==4)|(df_good['month']==5)]
df_bad_spr = df_bad[(df_bad['month']==3)|(df_bad['month']==4)|(df_bad['month']==5)]
df_good_summer = df_good[(df_good['month']==6)|(df_good['month']==7)|(df_good['month']==8)]
df_bad_summer = df_bad[(df_bad['month']==6)|(df_bad['month']==7)|(df_bad['month']==8)]
df_good_aut = df_good[(df_good['month']==9)|(df_good['month']==10)|(df_good['month']==11)]
df_bad_aut = df_bad[(df_bad['month']==9)|(df_bad['month']==10)|(df_bad['month']==11)]
df_good_winter = df_good[(df_good['month']==12)|(df_good['month']==1)|(df_good['month']==2)]
df_bad_winter = df_bad[(df_bad['month']==12)|(df_bad['month']==1)|(df_bad['month']==2)]

text_good_spr = df_good_spr['text']
text_bad_spr = df_bad_spr['text']
text_good_summer = df_good_summer['text']
text_bad_summer = df_bad_summer['text']
text_good_aut = df_good_aut['text']
text_bad_aut = df_bad_aut['text']
text_good_winter = df_good_winter['text']
text_bad_winter = df_bad_winter['text']

dictionary = corpora.Dictionary(line.lower().split() for line in text_good_winter)
four_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq <= 3]
dictionary.filter_tokens(four_ids)  # 去除只出现过一次的词
dictionary.compactify()       # 删除去除单词后的空格

text = []
for line in text_good_winter:
    text.append(line.lower().split())

class MyCorpus(object):
    def __iter__(self):
        for line in text_good_winter:
            yield dictionary.doc2bow(line.lower().split())
corpus_memory_friendly = MyCorpus()
corpus = [vector for vector in corpus_memory_friendly]  # 将读取的文档转换成语料库

LDA_models = LdaModel(corpus=corpus,id2word= dictionary, num_topics=5,
                      update_every=1,chunksize=len(corpus),passes=100, alpha='auto',random_state=42)
data = pyLDAvis.gensim_models.prepare(LDA_models, corpus, dictionary)
pyLDAvis.save_html(data,'D:/yelp data/yelp_data/vis_lda_good_winter_5.html')


LDA_models.save("D:/yelp data/yelp_data/Lda_good_winter_5")


dictionary = corpora.Dictionary(line.lower().split() for line in text_bad_winter)
four_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq <= 3]
dictionary.filter_tokens(four_ids)  # 去除只出现过一次的词
dictionary.compactify()       # 删除去除单词后的空格
text = []
for line in text_bad_winter:
    text.append(line.lower().split())

class MyCorpus(object):
    def __iter__(self):
        for line in text_bad_winter:
            yield dictionary.doc2bow(line.lower().split())
corpus_memory_friendly = MyCorpus()
corpus = [vector for vector in corpus_memory_friendly]  # 将读取的文档转换成语料库

LDA_models = LdaModel(corpus=corpus,id2word= dictionary, num_topics=4,
                      update_every=1,chunksize=len(corpus),passes=100, alpha='auto',random_state=42)
data = pyLDAvis.gensim_models.prepare(LDA_models, corpus, dictionary)
pyLDAvis.save_html(data,'D:/yelp data/yelp_data/vis_lda_bad_winter_4.html')


LDA_models.save("D:/yelp data/yelp_data/Lda_bad_winter_4")