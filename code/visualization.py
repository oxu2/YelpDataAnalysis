# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 22:26:58 2021

@author: ziyue
"""
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

month_bad_topic = pd.read_csv("D:\\yelp_dataset\\doc_top_dist_bad.csv",encoding='gbk')
month_good_topic = pd.read_csv("D:\\yelp_dataset\\doc_top_dist_good.csv",encoding='gbk')

topics = ['name','topic1','topic2','topic3','topic4','topic5','topic6']

winter_bad = month_bad_topic[(month_bad_topic['month'] == 12)|(month_bad_topic['month'] == 1)|(month_bad_topic['month'] == 2)][topics].groupby('name').mean()
spring_bad = month_bad_topic[(month_bad_topic['month'] == 3)|(month_bad_topic['month'] == 4)|(month_bad_topic['month'] == 5)][topics].groupby('name').mean()
summer_bad = month_bad_topic[(month_bad_topic['month'] == 6)|(month_bad_topic['month'] == 7)|(month_bad_topic['month'] == 8)][topics].groupby('name').mean()
fall_bad = month_bad_topic[(month_bad_topic['month'] == 9)|(month_bad_topic['month'] == 10)|(month_bad_topic['month'] == 11)][topics].groupby('name').mean()

winter_good = month_good_topic[(month_good_topic['month']==12)|(month_good_topic['month']==1)|(month_good_topic['month']==2)][topics].groupby('name').mean()
spring_good = month_good_topic[(month_good_topic['month']==3)|(month_good_topic['month']==4)|(month_good_topic['month']==5)][topics].groupby('name').mean()
summer_good = month_good_topic[(month_good_topic['month']==6)|(month_good_topic['month']==7)|(month_good_topic['month']==8)][topics].groupby('name').mean()
fall_good = month_good_topic[(month_good_topic['month']==9)|(month_good_topic['month']==10)|(month_good_topic['month']==11)][topics].groupby('name').mean()




topics = ['topic1','topic2','topic3','topic4','topic5','topic6']

plt.pie(spring_bad[topics].sum(),labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Spring bad topics")
plt.pie(summer_bad[topics].sum(),labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Summer bad topics")
plt.pie(fall_bad[topics].sum(),labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Fall bad topics")
plt.pie(winter_bad[topics].sum(),labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Winter bad topics")


# bad_spring_topics = spring_bad.astype('float').idxmax(axis='columns')
# bad_summer_topics = summer_bad.astype('float').idxmax(axis='columns')

plt.pie(spring_good[topics].sum(),labels=['Sandwiches taste','Burger taste','Customer service','Drinks and atmosphere','Breakfast taste','Convenient'],autopct='%1.2f%%')
plt.title("Spring Good topics")
plt.pie(summer_good[topics].sum(),labels=['Sandwiches taste','Burger taste','Customer service','Drinks and atmosphere','Breakfast taste','Convenient'],autopct='%1.2f%%')
plt.title("Summer Good topics")
plt.pie(fall_good[topics].sum(),labels=['Sandwiches taste','Burger taste','Customer service','Drinks and atmosphere','Breakfast taste','Convenient'],autopct='%1.2f%%')
plt.title("Fall Good topics")
plt.pie(winter_good[topics].sum(),labels=['Sandwiches taste','Burger taste','Customer service','Drinks and atmosphere','Breakfast taste','Convenient'],autopct='%1.2f%%')
plt.title("Winter Good topics")