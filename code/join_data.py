# -*- coding: utf-8 -*- 
"""
Created on Tue Nov  9 10:23:25 2021

@author: ziyue
"""
import json
import pandas as pd

data = []
with open('D:/yelp_dataset/review.json','rb') as f:
    while True:
        line_data = f.readline()
        if not line_data:
            break
        temp = json.loads(line_data)
        data.append(temp)
review = pd.DataFrame(data)
sandwiches = pd.read_csv('test.csv')
review['business_id']=review['business_id'].astype(str)
sandwiches['business_id']=sandwiches['business_id'].astype(str)
sandwiches_review = pd.merge(review,sandwiches,how='inner',on='business_id')
sandwiches_review.to_csv('./sandwiches_review.csv')