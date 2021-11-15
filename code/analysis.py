# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 16:09:46 2021

@author: ziyue
"""
import pandas as pd
import collections 
import matplotlib as plt


business = pd.read_csv('D:\\yelp_dataset\\sandwiches.csv')
review = pd.read_csv('D:\\yelp_dataset\\sandwiches_review.csv')

### DATA SUMMARY
print(business.loc[1])
print(review.loc[1])
print(business.groupby(['state'])['business_id'].count())
print(business.groupby(['state'])['review_count'].sum())
print(business.groupby(['state'])['stars'].mean())



### RESTRANUANT SCORE
res_score = business.groupby(['name'])['stars'].mean()
res_count = review.groupby(['name'])['name'].count()

res_score.sort_values()
res_count.sort_values()


### TO SEE THE OVERALL CATEGORIES FREQUENCY
def word_order(dataframe,separator):
    text = []
    for i in list(dataframe):
        j = i.split(separator)
        for k in j:
            text.append(k)
    word_counts = collections.Counter(text)
    return sorted(word_counts.items(),key=lambda x:x[1],reverse=True)


word_order(review['categories'], ', ')


### TO SEE THE CATEGORIES FREQUENCY BY SOCRE
word_order(review[review['stars_y']>=4]['categories'], ', ')
word_order(review[review['stars_y']<=2]['categories'], ', ')


### TO SEE THE WORD FREQUENCY BY SOCRE
word_order(review[review['stars_x']>=4]['text'], ' ')
word_order(review[review['stars_x']<=2]['text'], ' ')


### Analysis: Reasons of abnorm review
good_to_bad = review[(review['stars_y']<2)&(review['stars_x']>4)]['text']
bad_to_good = review[(review['stars_y']>4)&(review['stars_x']<2)]['text']
word_order(good_to_bad, ' ')
word_order(bad_to_good, ' ')


### Visualization
plt.pyplot.hist(res_score,edgecolor='black',facecolor='blue', alpha=0.5)
review_score = review['stars_x']
plt.pyplot.bar(range(1,6),[review_score.value_counts()[1],review_score.value_counts()[2],review_score.value_counts()[3],review_score.value_counts()[4],review_score.value_counts()[5]])
