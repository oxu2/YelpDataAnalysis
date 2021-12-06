import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib as mpl

month_bad_topic = pd.read_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/doc_top_dist_bad.csv",encoding='gbk')
month_good_topic = pd.read_csv("C:/Users/20172/Documents/GitHub/YelpDataAnalysis/data_set/doc_top_dist_good.csv",encoding='gbk')

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

def num2color(values, cmap):
    """将数值映射为颜色"""
    norm = mpl.colors.Normalize(vmin=np.min(values), vmax=np.max(values))
    cmap = mpl.cm.get_cmap(cmap)
    return [cmap(norm(val)) for val in values]

num = np.arange(6)
cols = num2color(num, "summer")
#cols = np.array(['#ff165d','#f47c7c','#ff9234','#ffcd3c','#b693fe','#ff9de2'])
plt.pie(spring_bad[topics].sum(),colors = cols,labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
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
"""
cols = num2color(num, "autumn")
cols = num2color(num, "plasma")
cols = num2color(num, "Pastel1")
cols = num2color(num, "Pastel2")
"""
cols = num2color(num, "Wistia")
plt.pie(spring_good[topics].sum(),colors = cols,labels=['take out','sandwiches taste','Service','Burger taste','Wait minitues','Snack&Sides'],autopct='%1.2f%%')
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