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
import pyLDAvis
from gensim.models import LdaModel, CoherenceModel
import numpy as np
import os
import random
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

sandwiches = pd.read_csv('D:/yelp data/yelp_data/sandwiches_review_1202.csv')
good_rew = sandwiches[sandwiches['stars_x']==5]['text'].tolist()
bad_rew = sandwiches[(sandwiches['stars_x']== 1) | (sandwiches['stars_x'] == 2)]['text'].tolist()
good_rew_date = sandwiches[sandwiches['stars_x']==5]['date'].tolist()
bad_rew_date = sandwiches[(sandwiches['stars_x']== 1) | (sandwiches['stars_x'] == 2)]['date'].tolist()
good_business_idx = sandwiches[sandwiches['stars_x']==5]['name']
bad_business_idx = sandwiches[(sandwiches['stars_x']==1) | (sandwiches['stars_x']==2)]['name']
"""
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

df_good = pd.DataFrame(good_rew,columns=['text','doclength'])
df_bad = pd.DataFrame(bad_rew,columns=['text','doclength'])
df_good['year'] = good_year
df_good['month'] = good_month
df_bad['year'] = bad_year
df_bad['month'] = bad_month
"""
df_good = pd.read_csv('C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/good_review.csv',encoding = "ISO-8859-1")
df_bad = pd.read_csv('C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/bad_review.csv',encoding = "ISO-8859-1")
df_good['name'] = good_business_idx
df_bad['name'] = bad_business_idx
df_good = df_good[df_good['doclength']>=20]
df_bad = df_bad[df_bad['doclength']>=20]
text_bad = df_bad['text']

text = []
for line in text_bad:
    text.append(line.lower().split())

dictionary = corpora.Dictionary(line.lower().split() for line in text_bad)
four_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq <= 3]
dictionary.filter_tokens(four_ids)  # 去除只出现过一次的词
dictionary.compactify()       # 删除去除单词后的空格

class MyCorpus(object):
    def __iter__(self):
        for line in text_bad:
            yield dictionary.doc2bow(line.lower().split())
corpus_memory_friendly = MyCorpus()
corpus = [vector for vector in corpus_memory_friendly]  # 将读取的文档转换成语料库

LDA_models = LdaModel(corpus=corpus,id2word= dictionary, num_topics=6,
                      update_every=1,chunksize=len(corpus),passes=100, alpha='auto',random_state=42)
data = pyLDAvis.gensim_models.prepare(LDA_models, corpus, dictionary)
pyLDAvis.save_html(data,'D:/yelp data/yelp_data/vis_lda_bad_6.html')
LDA_models.save("D:/yelp data/yelp_data/Lda_bad_6")

LDA_model =  LdaModel.load("D:/yelp data/yelp_data/Lda_bad_6")
LDA_model.get_topics()[1]

topics = LDA_model.show_topic(topicid = 1,topn = 10) #展示每个主题的前10个topic

for i, (word_, w) in enumerate(topics):
    print(i)
    print(word_)
    print(w)


LDA_model.print_topic(1, topn=10)

LDA_model[corpus[100]]

L
sum(LDA_model.alpha.array)

len(LDA_model[corpus[1]])

def DF(num_topics, model, num_words=15):
    """
    :param num_topics: number of topics
    :param model: DTM trained model
    :param num_words: number of words to display for the topicid at the time period
    :return: Dataframe with corresponding weight for each top word in each topic of each period
    """
    topicId, weight, word = [], [], []
    for s in range(num_topics):
        topics = model.show_topic(topicid=s, topn=num_words)
        for i, (word_, w) in enumerate(topics):
            topicId.append(s)
            word.append(word_)
            weight.append(w)
    return pd.DataFrame(list(zip(topicId, weight, word)), columns=['topicId', 'word', 'weight'])

a = DF(6,LDA_model,15)

def partitioning(df):
    """
    :param df: Dataframe with corresponding weight for each top word in each topic of each period
    :return: partition based on TopicID

    """

    d = {}  # d[i] contains records for TopicID i
    for topic in list(df['topicId'].unique()):  # for each topic
        d[topic] = df.loc[df['topicId'] == topic]  # create dataframe with records
        print('Number of records for Topic %d = %d' % (topic, len(d[topic])))
    return d

def topic_distribution(num_topics, model, corpus):
    """
    function to compute the topical distribution in a document
    :param num_topics: number of topics
    """
    doc, topicId, distributions = [], [], []
    for i in range(0, len(corpus)):
        dist = model[corpus[i]]
        topic_dist = pd.DataFrame(dist, columns=['topicid', 'dist'])
        for topic in range(0, num_topics):
            doc.append(i)
            topicId.append(topic)
            if (topic in topic_dist['topicid']):
                distributions.append(topic_dist[topic_dist['topicid']== topic]['dist'])
            else:
                distributions.append(0)
    return pd.DataFrame(list(zip(doc, topicId, distributions)),
                        columns=['document', 'topicId', 'distribution'])

doc_topic = topic_distribution(6, LDA_model, corpus[1])