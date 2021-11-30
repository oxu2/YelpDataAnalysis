import json
import pandas as pd

data = []
with open('./yelp_dataset/business.json','rb') as f:
    while True:
        line_data = f.readline()
        if not line_data:
            break
        temp = json.loads(line_data)
        categories = str(temp['categories'])
        if ('Sandwiches' in categories or 'Burgers' in categories) and ('Pizza' not in categories) and ('Barbecue' not in categories) and ('Barbeque' not in categories):
            data.append(temp)
data = pd.DataFrame(data)
data.to_csv('./sandwiches.csv')
