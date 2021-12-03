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


"""
data_business = []
with open('D:/yelp data/yelp_dataset/business.json','rb') as f:
    while True:
        line_data = f.readline()
        if not line_data:
            break
        temp = json.loads(line_data)
        categories = str(temp['categories'])
        if 'Sandwiches' in categories:
            data_business.append(temp)
data_business = pd.DataFrame(data_business)


#with open('D:/yelp data/yelp_dataset/review.json','rb') as f:
data_review = []
with open('D:/yelp data/yelp_dataset/review.json','rb') as f:
    while True:
        line_data = f.readline()
        if not line_data:
            break
        temp = json.loads(line_data)
        data_review.append(temp)

review = pd.DataFrame(data_review)
del review
"""

sandwiches = pd.read_csv('D:/yelp data/yelp_data/sandwiches_review.csv')
review_five = sandwiches[sandwiches['stars_x']==5]['text'].tolist()
review_four = sandwiches[sandwiches['stars_x']==4]['text'].tolist()
review_three = sandwiches[sandwiches['stars_x']==3]['text'].tolist()
review_two = sandwiches[sandwiches['stars_x']==2]['text'].tolist()
review_one = sandwiches[sandwiches['stars_x']==1]['text'].tolist()
stopwords = pd.read_csv('D:/yelp data/yelp_data/stopwords.txt')
stopwords = stopwords['stopwords'].tolist()
stopwords = [i for i in stopwords if i!=""]

def dropstopwords(sentences):
    #sentences = sentences.replace("\\u3000", "").replace("%", "").replace("+", "").replace(".", "").replace("\n","\xa0", "")
    sentences = re.sub('[0-9]', "", sentences)  ## 去掉语料中的数字与字母
    sentences = re.sub(r'[^\w\s]', '', sentences)
    #sentences = re.sub("[^a-zA-Z]", '', sentences)
    sentences = sentences.lower()
    sentences = sentences.split()
    sentences = [i for i in sentences if i not in stopwords]
    doc_length = len(sentences)
    sentences = " ".join(sentences)
    return sentences,doc_length

review_five = list(map(lambda x: dropstopwords(x), review_five))
review_four = list(map(lambda x: dropstopwords(x), review_four))
review_three = list(map(lambda x: dropstopwords(x), review_three))
review_two = list(map(lambda x: dropstopwords(x), review_two))
review_one = list(map(lambda x: dropstopwords(x), review_one))
df_five = pd.DataFrame(review_five,columns=['text','doclength'])
df_four = pd.DataFrame(review_four,columns=['text','doclength'])
df_three = pd.DataFrame(review_three,columns=['text','doclength'])
df_two = pd.DataFrame(review_two,columns=['text','doclength'])
df_one = pd.DataFrame(review_one,columns=['text','doclength'])


text_five = df_five[df_five['doclength']>=20]['text'].tolist()
txt_five = random.sample(text_five, 5000)
text_four =df_four[df_four['doclength']>=20]['text'].tolist()
txt_four = random.sample(text_four, 5000)
text_three =df_three[df_three['doclength']>=20]['text'].tolist()
txt_three = random.sample(text_three, 5000)
text_two =df_two[df_two['doclength']>=20]['text'].tolist()
txt_two = random.sample(text_two, 5000)
text_one =df_one[df_one['doclength']>=20]['text'].tolist()
txt_one = random.sample(text_one, 5000)

with open("D:/yelp data/yelp_dataset/review_two_sample.txt",'w',encoding='utf-8') as f:
    f.writelines(txt_two)



"""
txt_test = random.sample(text_five, 20000)
txt_test = pd.DataFrame(columns="test content",txt_test)
txt_test.to_csv("D:/yelp data/test_file.csv")
"""
dictionary = corpora.Dictionary(line.lower().split() for line in text_five)
four_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq <= 4]
dictionary.filter_tokens(four_ids)  # 去除只出现过一次的词
dictionary.compactify()       # 删除去除单词后的空格

text = []
for line in text_five:
    text.append(line.lower().split())

class MyCorpus(object):
    def __iter__(self):
        for line in text_five:
            yield dictionary.doc2bow(line.lower().split())
corpus_memory_friendly = MyCorpus()
corpus = [vector for vector in corpus_memory_friendly]  # 将读取的文档转换成语料库

# Considering 1-15 topics, as the last is cut off
num_topics = list(range(20)[1:])
num_keywords = 30

LDA_models = {}
LDA_topics = {}
for i in num_topics:
    LDA_models[i] = LdaModel(corpus=corpus,
                             id2word= dictionary,
                             num_topics=i,
                             update_every=1,
                             chunksize=len(corpus),
                             passes=100,
                             alpha='auto',
                             random_state=42)
    shown_topics = LDA_models[i].show_topics(num_topics=i,
                                             num_words=num_keywords,
                                             formatted=False)
    LDA_topics[i] = [[word[0] for word in topic[1]] for topic in shown_topics]

"""
for i in num_topics:
    name_tmp = 'D:/yelp data/model_save/Lda_rmrb_' + str(i)
    LDA_models[i].save(name_tmp)
"""
def jaccard_similarity(topic_1, topic_2):
    """
    Derives the Jaccard similarity of two topics

    Jaccard similarity:
    - A statistic used for comparing the similarity and diversity of sample sets
    - J(A,B) = (A ∩ B)/(A ∪ B)
    - Goal is low Jaccard scores for coverage of the diverse elements
    """
    intersection = set(topic_1).intersection(set(topic_2))
    union = set(topic_1).union(set(topic_2))

    return float(len(intersection)) / float(len(union))


LDA_stability = {}
for i in range(0, len(num_topics) - 1):
    jaccard_sims = []
    for t1, topic1 in enumerate(LDA_topics[num_topics[i]]):  # pylint: disable=unused-variable
        sims = []
        for t2, topic2 in enumerate(LDA_topics[num_topics[i + 1]]):  # pylint: disable=unused-variable
            sims.append(jaccard_similarity(topic1, topic2))

        jaccard_sims.append(sims)
    LDA_stability[num_topics[i]] = jaccard_sims

mean_stabilities = [np.array(LDA_stability[i]).mean() for i in num_topics[:-1]]


coherences = [CoherenceModel(model=LDA_models[i], texts=text, dictionary=dictionary, coherence='c_v').get_coherence()\
              for i in num_topics[:-1]]

coh_sta_diffs = [coherences[i-1] - mean_stabilities[i-1] for i in num_topics[:-1]] # limit topic numbers to the number of keywords
coh_sta_max = max(coh_sta_diffs)
coh_sta_max_idxs = [i for i, j in enumerate(coh_sta_diffs) if j == coh_sta_max]
ideal_topic_num_index = coh_sta_max_idxs[0] # choose less topics in case there's more than one max
ideal_topic_num = num_topics[ideal_topic_num_index]


plt.figure(figsize=(20, 10))
ax = sns.lineplot(x=num_topics[:-1], y=mean_stabilities, label='Average Topic Overlap',markers=True, dashes=False)
ax = sns.lineplot(x=num_topics[:-1], y=coherences, label='Topic Coherence',markers=True, dashes=False)

ax.axvline(x=ideal_topic_num, label='Ideal Number of Topics', color='black')
ax.axvspan(xmin=ideal_topic_num - 1, xmax=ideal_topic_num + 1, alpha=0.5, facecolor='grey')

y_max = max(max(mean_stabilities), max(coherences)) + (0.10 * max(max(mean_stabilities), max(coherences)))
ax.set_ylim([0, y_max])
ax.set_xlim([1, num_topics[-1] - 1])

ax.axes.set_title('Model Metrics per Number of Topics', fontsize=25)
ax.set_ylabel('Metric Level', fontsize=20)
ax.set_xlabel('Number of Topics', fontsize=20)
plt.legend(fontsize=20)
plt.savefig("D:/yelp data/yelp_data/topic_choose.jpg")
plt.show()
sns.lineplot()


LDA_models = LdaModel(corpus=corpus,id2word= dictionary, num_topics=18,
                      update_every=1,chunksize=len(corpus),passes=100, alpha='auto',random_state=42)
data = pyLDAvis.gensim_models.prepare(LDA_models, corpus, dictionary)
pyLDAvis.save_html(data,'D:/yelp data/yelp_data/vis_lda.html')
LDA_models.save("D:/yelp data/yelp_data/Lda_18")