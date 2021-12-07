
scale_final_score = read.csv(file = "df_topic_main_id.txt")[,(3:18)]

scale_final_score[14]#good
scale_final_score[15]#bad

test = head(scale_final_score[15])
strsplit(test[1,],",")
