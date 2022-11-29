## Start up the libraries
import tweepy
import pandas as pd
import requests
import os
#insert your Twitter keys here
consumer_key = 'your key'
consumer_secret = 'your secret key'
access_token='your access token'
access_token_secret='your access token secret'
twitter_handle='handle'

## here for configuration
project_App = 'Post-tweets from CVS, once per day'
screen_name = 'your-twitter-name'
file_path = '/your-folder/Tweets-to-be-posted.csv'
################################################################################
###  Load Sheets
################################################################################
# dataframe of reference = List of Tweets
df = pd.read_csv(file_path)
df.Date = pd.to_datetime(df['tweetDate'],format='%Y-%m-%d')
df.set_index('tweetDate')
###############################################
### get tweet data of Today
###############################################
from datetime import date
from urllib.parse import urlparse

# Returns the current local date
today = date.today().strftime('%Y-%m-%d')

df['tweetDate']= pd.to_datetime(df['tweetDate'])
options = [today]

# selecting rows based on condition
tweetRow = df.loc[df['tweetDate'].isin(options)]
# set text
tweetText = str(tweetRow.iloc[0]['tweetText']) + "\n \n" + str(tweetRow.iloc[0]['tweetURL'])
# set image path and image filename
tweetImageURL = str(tweetRow.iloc[0]['tweetImage'])
print(tweetImageURL)
# set imageFileName
a = urlparse(tweetImageURL)
tweetImagePath = a.path
tweetImageFileName = os.path.basename(a.path)
tweetImageFilePath = tweetImageURL.partition(tweetImageFileName)[0]
print('completed')

###############################################
### Log-in in Twitter
###############################################

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#list= open('twitter_followers.txt','w')

if(api.verify_credentials):
    print ('We successfully logged in')

print('Completed')

###############################################
####  Post the daily Tweet
###############################################

# if there is image, we post with media, else, just text
if tweetImagePath == "nan":
  status = api.update_status(tweetText)
else:
  request = requests.get(tweetImageURL, stream=True)
  if request.status_code == 200:
    with open(tweetImageFileName, 'wb') as image:
      for chunk in request:
        image.write(chunk)

    api.update_with_media(tweetImageFileName, status=tweetText)
    os.remove(tweetImageFileName)

print('posted')
