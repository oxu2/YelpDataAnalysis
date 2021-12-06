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

def num2color(values, cmap):
    """number to color"""
    norm = mpl.colors.Normalize(vmin=np.min(values), vmax=np.max(values))
    cmap = mpl.cm.get_cmap(cmap)
    return [cmap(norm(val)) for val in values]

num = np.arange(6)
topics = ['topic1','topic2','topic3','topic4','topic5','topic6']

cols = num2color(num,'summer')
plt.pie(spring_bad[topics].sum(),colors = cols, labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Spring bad topics")
plt.savefig("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/image/Spring_bad.png")
plt.show()
plt.pie(summer_bad[topics].sum(),colors = cols,labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Summer bad topics")
plt.savefig("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/image/Summer_bad.png")
plt.show()
plt.pie(fall_bad[topics].sum(),colors = cols,labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Fall bad topics")
plt.savefig("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/image/Fall_bad.png")
plt.show()
plt.pie(winter_bad[topics].sum(),colors = cols,labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Winter bad topics")
plt.savefig("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/image/Winter_bad.png")
plt.show()


# bad_spring_topics = spring_bad.astype('float').idxmax(axis='columns')
# bad_summer_topics = summer_bad.astype('float').idxmax(axis='columns')

cols = num2color(num,'Wistia')
plt.pie(spring_good[topics].sum(),colors = cols, labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Spring good topics")
plt.savefig("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/image/Spring_good.png")
plt.show()
plt.pie(summer_good[topics].sum(),colors = cols,labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Summer good topics")
plt.savefig("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/image/Summer_good.png")
plt.show()
plt.pie(fall_good[topics].sum(),colors = cols,labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Fall good topics")
plt.savefig("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/image/Fall_good.png")
plt.show()
plt.pie(winter_good[topics].sum(),colors = cols,labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
plt.title("Winter good topics")
plt.savefig("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/image/Winter_good.png")
plt.show()
