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
'''
good_rew = sandwiches[sandwiches['stars_x']==5]['text'].tolist()
bad_rew = sandwiches[(sandwiches['stars_x']== 1) | (sandwiches['stars_x'] == 2)]['text'].tolist()
good_rew_date = sandwiches[sandwiches['stars_x']==5]['date'].tolist()
bad_rew_date = sandwiches[(sandwiches['stars_x']== 1) | (sandwiches['stars_x'] == 2)]['date'].tolist()
'''
good_business_idx = sandwiches[sandwiches['stars_x']==5]['name'].to_list()
bad_business_idx = sandwiches[(sandwiches['stars_x']==1) | (sandwiches['stars_x']==2)]['name'].tolist()
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
#LDA_models.save("D:/yelp data/yelp_data/Lda_bad_6")
LDA_model =  LdaModel.load("D:/yelp data/yelp_data/Lda_bad_6")

"""
topics = LDA_model.show_topic(topicid = 1,topn = 10) #展示每个主题的前10个topic
for i, (word_, w) in enumerate(topics):
    print(i)
    print(word_)
    print(w)

LDA_model.print_topic(1, topn=10)

LDA_model[corpus[100]]

sum(LDA_model.alpha.array)

len(LDA_model[corpus[1]])
"""

## 每个主题的前15个关键词，方便和pyldavis对应
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
            topicId.append(s+1)
            word.append(word_)
            weight.append(w)
    return pd.DataFrame(list(zip(topicId, weight, word)), columns=['topicId', 'word', 'weight'])

topic_top_words = DF(6,LDA_model,15) #get the top words for each  topic
topic_top_words.to_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/topic_top_words_bad.csv")

def topic_distribution(num_topics, model, corpus):
    """
    function to compute the topical distribution in a document
    :param num_topics: number of topics
    """
    doc, topicId, distributions = [], [], []
    for i in range(0, len(corpus)):
        dist = model[corpus[i]]
        topic_dist = pd.DataFrame(dist, columns=['topicid', 'dist'])
        c = topic_dist['topicid'].to_list()
        for topic in range(0, num_topics):
            doc.append(i)
            topicId.append(topic)
            if (topic in c):
                distributions.append(topic_dist[topic_dist['topicid']== topic]['dist'].values[0])
            else:
                distributions.append(0)
    return pd.DataFrame(list(zip(doc, topicId, distributions)),
                        columns=['document', 'topicId', 'distribution'])

#提取每个document的主题分布
#LDA_model.get_document_topics(corpus[0], minimum_probability=0.0)
def topic_distribution(num_topics, model, corpus):
    """
    function to compute the topical distribution in a document
    :param num_topics: number of topics
    """
    topics = {}
    for i in range(0, num_topics):
        topics[i+1] = []
    for i in range(0, len(corpus)):
        dist = model[corpus[i]]
        topic_dist = pd.DataFrame(dist, columns=['topicid', 'dist'])
        c = topic_dist['topicid'].to_list()
        for topic in range(0, num_topics):
            if (topic in c):
                topics[topic+1].append(topic_dist[topic_dist['topicid']== topic]['dist'].values[0])
            else:
                topics[topic+1].append(0)
    return topics

# get the topic distribution for each document
doc_topic = topic_distribution(6, LDA_model, corpus)
col_names = ['topic'+str(i+1) for i in range(6)]
for i in range(6):
    df_bad[col_names[i]] = doc_topic[i+1]
df_bad.to_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/doc_top_dist_bad.csv")

text_good = df_good['text']
text = []
for line in text_good:
    text.append(line.lower().split())

dictionary = corpora.Dictionary(line.lower().split() for line in text_good)
four_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq <= 3]
dictionary.filter_tokens(four_ids)  # 去除只出现过一次的词
dictionary.compactify()       # 删除去除单词后的空格

class MyCorpus(object):
    def __iter__(self):
        for line in text_good:
            yield dictionary.doc2bow(line.lower().split())
corpus_memory_friendly = MyCorpus()
corpus = [vector for vector in corpus_memory_friendly]  # 将读取的文档转换成语料库
LDA_model =  LdaModel.load("D:/yelp data/yelp_data/Lda_good_6")

topic_top_words = DF(6,LDA_model,15) #get the top words for each  topic
topic_top_words.to_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/topic_top_words_good.csv")

# get the topic distribution for each document
doc_topic = topic_distribution(6, LDA_model, corpus)
col_names = ['topic'+str(i+1) for i in range(6)]
for i in range(6):
    df_good[col_names[i]] = doc_topic[i+1]
df_good.to_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/doc_top_dist_good.csv")

bad_name = set(df_bad['name'].tolist()) #4740 Name
good_name = set(df_good['name'].tolist()) #5007 Name
union_name = bad_name & good_name #4550 Name
only_good = good_name - union_name
only_bad = bad_name - union_name

union_name = list(union_name)
only_good = list(only_good)
only_bad = list(only_bad)

topic_good = pd.DataFrame(df_good,columns=['name','topic1','topic2','topic3','topic4','topic5','topic6'])
topic_good = topic_good.rename(columns = {'topic1':'good_topic1','topic2':'good_topic2','topic3':'good_topic3',
                                          'topic4':'good_topic4','topic5':'good_topic5','topic6':'good_topic6'})
topic_bad = topic_bad.rename(columns = {'topic1':'bad_topic1','topic2':'bad_topic2','topic3':'bad_topic3',
                                          'topic4':'bad_topic4','topic5':'bad_topic5','topic6':'bad_topic6'})

topic_good_mean = topic_good.mean()
topic_good_mean.to_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/good_topic_mean.csv")
topic_bad_mean = topic_bad.mean()
topic_bad_mean.to_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/bad_topic_mean.csv")

good_topic1 = topic_good['good_topic1'].groupby(topic_good['name']).mean()
good_topic2 = topic_good['good_topic2'].groupby(topic_good['name']).mean()
good_topic3 = topic_good['good_topic3'].groupby(topic_good['name']).mean()
good_topic4 = topic_good['good_topic4'].groupby(topic_good['name']).mean()
good_topic5 = topic_good['good_topic5'].groupby(topic_good['name']).mean()
good_topic6 = topic_good['good_topic6'].groupby(topic_good['name']).mean()
df_good_mean = pd.DataFrame(list(zip(list(good_topic6.keys()),list(good_topic1),list(good_topic2),list(good_topic3),
                            list(good_topic4),list(good_topic5),list(good_topic6))), columns = ['names','good_topic1',
                            'good_topic2','good_topic3','good_topic4','good_topic5','good_topic6'])

bad_topic1 = topic_bad['bad_topic1'].groupby(topic_bad['name']).mean()
bad_topic2 = topic_bad['bad_topic2'].groupby(topic_bad['name']).mean()
bad_topic3 = topic_bad['bad_topic3'].groupby(topic_bad['name']).mean()
bad_topic4 = topic_bad['bad_topic4'].groupby(topic_bad['name']).mean()
bad_topic5 = topic_bad['bad_topic5'].groupby(topic_bad['name']).mean()
bad_topic6 = topic_bad['bad_topic6'].groupby(topic_bad['name']).mean()
df_bad_mean = pd.DataFrame(list(zip(list(bad_topic6.keys()),list(bad_topic1),list(bad_topic2),list(bad_topic3),
                            list(bad_topic4),list(bad_topic5),list(bad_topic6))), columns = ['names','bad_topic1',
                            'bad_topic2','bad_topic3','bad_topic4','bad_topic5','bad_topic6'])

df_topic_mean_union = pd.merge(df_good_mean,df_bad_mean,on='names')
df_topic_mean_union.to_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/df_topic_mean_union.csv")
df_topic_mean = pd.merge(df_good_mean,df_bad_mean,on='names',how = 'outer')
df_topic_mean.to_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/df_topic_mean.csv")

df_topic_mean  = pd.read_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/df_topic_mean_union.csv",encoding = "ISO-8859-1")

good_mian_topic  = []

len(df_topic_mean)
type(df_topic_mean.columns.values[0])
df_topic_mean.iloc[1,1]
tmp_bad =  []
for i in range(len(df_topic_mean)):
    a = ""
    for j in range(7,13):
        if(df_topic_mean.iloc[i,j] > 0.1):
            name = df_topic_mean.columns.values[j]
            a += name
            a += ','
    a  = a[:-1]
    tmp_bad.append(a)


df_good = df_topic_mean[['good_topic1','good_topic2','good_topic3','good_topic4','good_topic5','good_topic6']]
tmp_good = df_good.idxmax(1).to_list()
df_topic_mean['main_good_topic'] = tmp_good
df_topic_mean['main_bad_topic'] = tmp_bad


df_topic_mean = pd.read_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/df_topic_main.csv")
df_topic_mean_union = pd.merge(df_good_mean,df_bad_mean,on='names')
business_id = sandwiches[['business_id','name']]
#value = np.repeat(1,len(business_id))
#business_id['value'] =  np.repeat(1,len(business_id))
business_id_uniq = business_id.groupby(business_id['business_id'])
df_topic_mean_union = pd.merge(df_topic_mean,business_id,on='names')
a = sandwiches[sandwiches['name']==business_name[1]]['business_id']
a = a.tolist()
a = list(set(a))[0]
business_name = df_topic_mean["names"].to_list()
for i in business_name:
