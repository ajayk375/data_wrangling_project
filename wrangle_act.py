#!/usr/bin/env python
# coding: utf-8

# # Project: Wrangling and Analyze Data

# ## Data Gathering
# In the cell below, gather **all** three pieces of data for this project and load them in the notebook. **Note:** the methods required to gather each data are different.
# 1. Directly download the WeRateDogs Twitter archive data (twitter_archive_enhanced.csv)

# In[631]:


# Importing necessary Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import requests
import tweepy
from tweepy import OAuthHandler
from timeit import default_timer as timer


get_ipython().run_line_magic('matplotlib', 'inline')


# In[632]:


twitter_archive_df = pd.read_csv('twitter-archive-enhanced.csv')


# 2. Use the Requests library to download the tweet image prediction (image_predictions.tsv)

# In[633]:


url = "https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv"
response = requests.get(url)

with open ('image-predictions.tsv', mode ='wb') as file:
    file.write(response.content)

image_predictions_df = pd.read_csv('image-predictions.tsv' ,sep='\t')


# 3. Use the Tweepy library to query additional data via the Twitter API (tweet_json.txt)

# In[634]:


# We are not using Tweepy to access tweets. Instead will be refrencing Udacity's provided archive

twitter_extra_archive_list = []

with open ('tweet-json.txt', mode ='r' , encoding ='utf-8') as file:
    for line in file:
        data_line = json.loads(line)
        twitter_extra_archive_list.append({'tweet_id': data_line['id'],
                                            'favorites':data_line['favorite_count'],
                                            'retweets': data_line['retweet_count'],
                                            'timestamp': data_line['created_at']})
        
twitter_extra_archive_df = pd.DataFrame(twitter_extra_archive_list, columns=['tweet_id','favorites','retweets','timestamp'])


# ## Assessing Data
# In this section, detect and document at least **eight (8) quality issues and two (2) tidiness issue**. You must use **both** visual assessment
# programmatic assessement to assess the data.
# 
# **Note:** pay attention to the following key points when you access the data.
# 
# * You only want original ratings (no retweets) that have images. Though there are 5000+ tweets in the dataset, not all are dog ratings and some are retweets.
# * Assessing and cleaning the entire dataset completely would require a lot of time, and is not necessary to practice and demonstrate your skills in data wrangling. Therefore, the requirements of this project are only to assess and clean at least 8 quality issues and at least 2 tidiness issues in this dataset.
# * The fact that the rating numerators are greater than the denominators does not need to be cleaned. This [unique rating system](http://knowyourmeme.com/memes/theyre-good-dogs-brent) is a big part of the popularity of WeRateDogs.
# * You do not need to gather the tweets beyond August 1st, 2017. You can, but note that you won't be able to gather the image predictions for these tweets since you don't have access to the algorithm used.
# 
# 

# ### Visual assessment

# Each dataframe is displayed below for Visual assesment
# 

# Twitter enhanced Dataframe 

# In[635]:


twitter_archive_df.head()


# Twitter Image Prediction Dataframe

# In[636]:


image_predictions_df.head()


# Twitter Extra Archive DataFrame

# In[637]:


twitter_extra_archive_df.head()


# ### Programmatic Assement 

# In[638]:


twitter_archive_df.info()


# Checking for Duplicate Tweet id

# In[639]:


sum (twitter_archive_df['tweet_id'].duplicated())


# In[640]:


twitter_archive_df.rating_numerator.value_counts()


# In[641]:


print(twitter_archive_df.loc[twitter_archive_df.rating_numerator == 1776, 'text'])
print(twitter_archive_df['text'][979])

print(twitter_archive_df.loc[twitter_archive_df.rating_numerator == 144, 'text'])
print(twitter_archive_df['text'][1779])

print(twitter_archive_df.loc[twitter_archive_df.rating_numerator == 80, 'text'])
print(twitter_archive_df['text'][1254])

print(twitter_archive_df.loc[twitter_archive_df.rating_numerator == 666, 'text'])
print(twitter_archive_df['text'][189])


# In[642]:


twitter_archive_df.rating_denominator.value_counts()


# In[643]:


print(twitter_archive_df.loc[twitter_archive_df.rating_denominator == 16, 'text'])
print(twitter_archive_df['text'][1663])

print(twitter_archive_df.loc[twitter_archive_df.rating_denominator == 70, 'text'])
print(twitter_archive_df['text'][433])

print(twitter_archive_df.loc[twitter_archive_df.rating_denominator == 120, 'text'])
print(twitter_archive_df['text'][1779])

print(twitter_archive_df.loc[twitter_archive_df.rating_denominator == 15, 'text']) #No rating only comment
print(twitter_archive_df['text'][342])

print(twitter_archive_df.loc[twitter_archive_df.rating_denominator == 7, 'text']) #No rating only comment
print(twitter_archive_df['text'][516])


# Image Prediction

# In[644]:


image_predictions_df.info()


# In[645]:


sum(image_predictions_df.tweet_id.duplicated())


# In[646]:


sum(image_predictions_df.jpg_url.duplicated())


# In[647]:


pd.concat(url for _,url in image_predictions_df.groupby("jpg_url") if len(url) > 1)


# In[648]:


print(image_predictions_df.p1_dog.value_counts())
print(image_predictions_df.p2_dog.value_counts())
print(image_predictions_df.p3_dog.value_counts())


# In[649]:


print(image_predictions_df.img_num.value_counts())


# In[650]:


twitter_extra_archive_df.sample(10)


# In[651]:


twitter_extra_archive_df.info()


# ### Quality issues
# 
# 1. Preserve tweets with original ratings that have images in Twitter Archive
# 
# 2. Separate timestamp into day month and year
# 
# 3. Correct Numerators for ratings from twitter_archive_df
# 
# 4. Correct Denominators for ratings from twitter_archive_df
# 
# 5. Create single column for image prediction result and single column for confidence level
# 
# 6. Ratings is missing and needs to be calculated to assess results across dogs
# 	
# 7. Remove  duplicate jpg url entries from image_predictions_df
# 
# 8. Remove invalid dog names from twitter_archive_df
# 
# 9. Remove img_num column

# ### Tidiness issues
# 1. Dog Types are displayed in separate columns instead of a single column.
# 
# 2. All tables should be a part of one dataset for analysis.

# ## Cleaning Data
# In this section, clean **all** of the issues you documented while assessing. 
# 
# **Note:** Make a copy of the original data before cleaning. Cleaning includes merging individual pieces of data according to the rules of [tidy data](https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html). The result should be a high-quality and tidy master pandas DataFrame (or DataFrames, if appropriate).

# In[652]:


# Make copies of original pieces of data
twitter_archive_clean_df = twitter_archive_df.copy()
image_predictions_clean_df = image_predictions_df.copy()
twitter_extra_archive_clean_df = twitter_extra_archive_df.copy()


# ### Issue #1: Preserve tweets with original ratings that have images in Twitter Archive
# 

# #### Code

# In[653]:


twitter_archive_clean_df = twitter_archive_clean_df[pd.isnull(twitter_archive_clean_df['retweeted_status_user_id'])]


# #### Test

# In[654]:


sum(twitter_archive_clean_df.retweeted_status_user_id.value_counts())


# ### Issue # 2 Separate timestamp into day month and year.
# 
# We will first convert timestamp to datatime and then will perform extraction eventually will drop timestamp column.

# #### Code

# In[655]:


twitter_archive_clean_df['timestamp'] = pd.to_datetime(twitter_archive_clean_df['timestamp'])

twitter_archive_clean_df['year'] = twitter_archive_clean_df['timestamp'].dt.year

twitter_archive_clean_df['month'] = twitter_archive_clean_df['timestamp'].dt.month

twitter_archive_clean_df['day'] = twitter_archive_clean_df['timestamp'].dt.day

twitter_archive_clean_df = twitter_archive_clean_df.drop(['timestamp'],1)


# #### Test

# In[656]:


list (twitter_archive_clean_df)


# ### Issue #3: Correct Numerators for ratings from twitter_archive_df

# #### Code

# In[657]:


twitter_archive_clean_df[['rating_numerator', 'rating_denominator']] = twitter_archive_clean_df[['rating_numerator', 'rating_denominator']].astype(float)

#Update numerators

twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 883482846933004288), 'rating_numerator'] = 13.5
twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 786709082849828864), 'rating_numerator'] = 9.75
twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 778027034220126208), 'rating_numerator'] = 11.27
twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 681340665377193984), 'rating_numerator'] = 9.5
twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 680494726643068929), 'rating_numerator'] = 11.26


# #### Test

# In[658]:


with pd.option_context('max_colwidth', 200):
    display(twitter_archive_clean_df[twitter_archive_clean_df['text'].str.contains(r"(\d+\.\d*\/\d+)")]
            [['tweet_id', 'text', 'rating_numerator', 'rating_denominator']])


# ### Issue #4: Correct Denominators for ratings from twitter_archive_df
# 

# #### Code

# In[659]:


twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 666287406224695296), 'rating_numerator'] = 9
twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 666287406224695296), 'rating_denominator'] = 10

twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 716439118184652801), 'rating_numerator'] = 13.5
twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 716439118184652801), 'rating_denominator'] = 10

twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 682962037429899265), 'rating_numerator'] = 10
twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 682962037429899265), 'rating_denominator'] = 10

twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 722974582966214656), 'rating_numerator'] = 13
twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 722974582966214656), 'rating_denominator'] = 10

twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 740373189193256964), 'rating_numerator'] = 14
twitter_archive_clean_df.loc[(twitter_archive_clean_df.tweet_id == 740373189193256964), 'rating_denominator'] = 10

# We will now delete five tweets without actual ratings 
twitter_archive_clean_df = twitter_archive_clean_df[twitter_archive_clean_df['tweet_id'] != 835246439529840640]
twitter_archive_clean_df = twitter_archive_clean_df[twitter_archive_clean_df['tweet_id'] != 686035780142297088]
twitter_archive_clean_df = twitter_archive_clean_df[twitter_archive_clean_df['tweet_id'] != 832088576586297345]
twitter_archive_clean_df = twitter_archive_clean_df[twitter_archive_clean_df['tweet_id'] != 682808988178739200]
twitter_archive_clean_df = twitter_archive_clean_df[twitter_archive_clean_df['tweet_id'] != 810984652412424192]


# #### Test

# In[660]:


with pd.option_context('max_colwidth', 200):
    display(twitter_archive_clean_df[twitter_archive_clean_df['rating_denominator'] != 10][['tweet_id',
                                                                                      'text',
                                                                                      'rating_numerator',
                                                                                      'rating_denominator']])


# ### Issue #5: Create single column for image prediction result and single column for confidence level 
# 

# #### Code

# In[661]:


dog_type = []
confidence_list = []

#capture the dog type and confidence level from the first 'true' prediction
def image(image_predictions_clean_df):
    if image_predictions_clean_df['p1_dog'] == True:
        dog_type.append(image_predictions_clean_df['p1'])
        confidence_list.append(image_predictions_clean_df['p1_conf'])
    elif image_predictions_clean_df['p2_dog'] == True:
        dog_type.append(image_predictions_clean_df['p2'])
        confidence_list.append(image_predictions_clean_df['p2_conf'])
    elif image_predictions_clean_df['p3_dog'] == True:
        dog_type.append(image_predictions_clean_df['p3'])
        confidence_list.append(image_predictions_clean_df['p3_conf'])
    else:
        dog_type.append('Error')
        confidence_list.append('Error')
      
image_predictions_clean_df.apply(image, axis=1)

image_predictions_clean_df['dog_type'] = dog_type
image_predictions_clean_df['confidence_list'] = confidence_list

image_predictions_clean_df = image_predictions_clean_df[image_predictions_clean_df['dog_type'] != 'Error']


# #### Test

# In[662]:


image_predictions_clean_df.sample(5)


# ### Issue #6: Ratings is missing and needs to be calculated to assess results across dogs
# 

# #### Code

# In[663]:



twitter_archive_clean_df['rating'] = 10 * twitter_archive_clean_df['rating_numerator'] / twitter_archive_clean_df['rating_denominator'].astype(float)


# #### Test

# In[664]:


twitter_archive_clean_df.sample(10)


# ### Issue #7: Remove  duplicate jpg url entries from image_predictions_df.

# #### Code

# In[665]:


image_predictions_clean_df = image_predictions_clean_df.drop_duplicates(subset =['jpg_url'],keep = 'last')


# #### Test

# In[666]:


sum(image_predictions_clean_df.jpg_url.duplicated())


# ### Issue #8: Remove invalid dog names from twitter_archive_df

# #### Code

# In[667]:


twitter_archive_clean_df['name'] = twitter_archive_clean_df['name'].str.extract('\\b([A-Z]\\S*)\\b')

twitter_archive_clean_df.dropna(subset=['name'], inplace=True)

twitter_archive_clean_df = twitter_archive_clean_df[twitter_archive_clean_df.name != 'None']


# #### Test

# In[668]:


twitter_archive_clean_df.name.value_counts()


# ### Issue #9: Remove img_num column

# #### Code

# In[669]:


image_predictions_clean_df = image_predictions_clean_df.drop(['img_num'], 1) 


# #### Test

# In[670]:


image_predictions_clean_df.info()


# ### Tidiness Issue

# ### Issue #1: Delete columns that wont be uselful from twitter_archive_df

# #### Code

# In[671]:


twitter_archive_clean_df = twitter_archive_clean_df.drop(['source',
                                                          'in_reply_to_status_id',
                                                          'in_reply_to_user_id',
                                                          'retweeted_status_id',
                                                          'retweeted_status_user_id',
                                                          'retweeted_status_timestamp',
                                                          'expanded_urls'],1)

image_predictions_clean_df = image_predictions_clean_df.drop(['p1', 'p1_conf', 'p1_dog',
                                                              'p2', 'p2_conf', 'p2_dog',
                                                              'p3', 'p3_conf', 'p3_dog'], 1)


# #### Test

# In[672]:


twitter_archive_clean_df.info()

image_predictions_clean_df.info()


# ### Issue #2: Dog Types are displayed in separate columns instead of a single column

# ### Code

# In[673]:


twitter_archive_clean_df.doggo.replace('None', '', inplace=True)
twitter_archive_clean_df.doggo.replace(np.NaN, '', inplace=True)
twitter_archive_clean_df.floofer.replace('None', '', inplace=True)
twitter_archive_clean_df.floofer.replace(np.NaN, '', inplace=True)
twitter_archive_clean_df.pupper.replace('None', '', inplace=True)
twitter_archive_clean_df.pupper.replace(np.NaN, '', inplace=True)
twitter_archive_clean_df.puppo.replace('None', '', inplace=True)
twitter_archive_clean_df.puppo.replace(np.NaN, '', inplace=True)


twitter_archive_clean_df['dog_stages'] = twitter_archive_clean_df.text.str.extract('(doggo|floofer|pupper|puppo)', expand = True)

twitter_archive_clean_df['dog_stages'] = twitter_archive_clean_df.doggo + twitter_archive_clean_df.floofer + twitter_archive_clean_df.pupper + twitter_archive_clean_df.puppo
twitter_archive_clean_df.loc[twitter_archive_clean_df.dog_stages == 'doggopupper', 'dog_stages'] = 'doggo, pupper'
twitter_archive_clean_df.loc[twitter_archive_clean_df.dog_stages == 'doggopuppo', 'dog_stages'] = 'doggo, puppo'
twitter_archive_clean_df.loc[twitter_archive_clean_df.dog_stages == 'doggofloofer', 'dog_stages'] = 'doggo, floofer'

twitter_archive_clean_df.drop(['doggo','floofer','pupper','puppo'], axis=1, inplace = True)


# ### Test

# In[674]:


twitter_archive_clean_df.dog_stages.value_counts()


# ### Issue #12: All tables should be a part of one dataset for analysis

# ### Code

# In[675]:


df_twitter1 = pd.merge(twitter_archive_clean_df, image_predictions_clean_df, 
                       how = 'left', on = ['tweet_id'])

df_twitter1 = df_twitter1[df_twitter1['jpg_url'].notnull()]

df_twitter = pd.merge(df_twitter1, twitter_extra_archive_clean_df, 
                      how = 'left', on = ['tweet_id'])


# ### Test

# In[676]:


df_twitter.sample(50)


# In[677]:


df_twitter.info()


# In[678]:


df_twitter['rating_numerator'].value_counts()


# ## Storing Data
# Save gathered, assessed, and cleaned master dataset to a CSV file named "twitter_archive_master.csv".

# In[679]:


df_twitter.to_csv('twitter_archive_master.csv', index=False, encoding = 'utf-8')


# ## Analyzing and Visualizing Data
# In this section, analyze and visualize your wrangled data. You must produce at least **three (3) insights and one (1) visualization.**

# ### Insights & Visualisation:
# 1. Golden Retriever is the most popular breed
# 
# 2. Three dog names Lucy,Cooper and Charlie have popular names.
# 
# 3. Mean Numerator for dogs is 10. Highest numerator is 14.

# ### 1. Golden Retriever is the most popular breed

# In[680]:


df_twitter['dog_type'].value_counts()


# In[681]:


df_dog_type = df_twitter.groupby('dog_type').filter(lambda x: len(x) >= 25)

df_dog_type['dog_type'].value_counts().plot(kind = 'barh')
plt.title('Histogram of the Most Rated Dog Type')
plt.xlabel('Count')
plt.ylabel('Type of dog')

fig = plt.gcf() 
fig.savefig('Histogram.png',bbox_inches='tight');


# ###  2. Three dog names Lucy,Cooper and Charlie have popular names.

# In[682]:


df_twitter.name.value_counts()


# ### 3. Mean Numerator for dogs is 10. Highest numerator is 14.

# In[683]:


#Summary data for the rating numerator in the cleaned df_twitter dataframe
df_twitter.rating_numerator.describe()


# In[684]:


# Finding the dog breed with the highest numerator
df_twitter.groupby('dog_type')['rating_numerator'].mean().nlargest(10)


# #### Scatter Plot for retweet counts by ratings

# In[685]:


df_twitter.plot(x='retweets', y='rating', kind='scatter')
plt.xlabel('Retweet Counts')
plt.ylabel('Ratings')
plt.title('Retweet Counts by Ratings Scatter Plot')

fig = plt.gcf()
fig.savefig('RetweetsvsRatings.png',bbox_inches='tight');

