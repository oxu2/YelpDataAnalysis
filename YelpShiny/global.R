library(dplyr)

yelp <- read.csv("sandwiches.csv")[,-(13:15)]
advisor = read.table(file = "df_topic_main_id.txt")
# advisor = read.table(file = "df_topic_main_id.txt")
# advisor[,1] = as.character(advisor[,1])#name
# advisor[,16] = as.character(advisor[,16])#id
scale_final_score = read.csv("scale_final_score.csv")[,-1]
# scale_final_score = read.csv("df_topic_main_id.csv")[,-1]
scale_final_score[,1] = as.character(scale_final_score[,1])
mean_score = apply(scale_final_score[,-1], 2, median)
colnames(scale_final_score)[6] = "food and drink"

yelp$latitude <- jitter(yelp$latitude)
yelp$longitude <- jitter(yelp$longitude)
yelp$college <- yelp$stars
yelp$zipcode <- formatC(yelp$postal_code, width=5, format="d", flag="0")




cleantable <- yelp %>%
  select(
    Name = name,
    Business_id = business_id,
    City = city,
    State = state,
    Zipcode = postal_code,
    Rating = stars,
    Address = address,
    Lat = latitude,
    Long = longitude
  )

