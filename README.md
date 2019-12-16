# Twitter Trends

Welcome! Before you begin, I recommend you read the [Report](https://github.com/jesmith14/TwitterTrends/blob/master/Report.pdf) that accompanies this study.

In this repository/tutorial, you are given many tools to help you attempt to reverse engineer Twitter's trending algorithm.

*:warning: Note: Please use this information responsibly. This study was motivated by recent malicious attacks on Twitter's trending algorithm, in an attempt to help Twitter users understand what creates Twitter trends. This study is **not** intended to aide in any effort to exploit or attack Twitter trends. :warning:*

### Table of Contents
1. [How to create an AWS DynamoDB and connect to it](#1-how-to-create-an-aws-dynamodb-and-connect-to-it)
2. [How to create a Twitter Developer account and connect to it](#2-how-to-create-a-twitter-developer-account-and-connect-to-it)
3. [How to stream 1% of all tweets world wide and store them in your DynamoDB](#3-how-to-stream-1-of-all-tweets-world-wide-and-store-them-in-your-dynamodb)
4. [How to collect Twitter trend data from the Twitter API every 5 minutes and store it in your DynamoDB](#4-how-to-collect-twitter-trend-data-from-the-twitter-api-every-5-minutes-and-store-it-in-your-dynamodb)
5. [How to convert DynamoDB data into a csv](#5-how-to-convert-dynamodb-data-into-a-csv)
6. [How to clean and work with Twitter data](#6-how-to-clean-and-work-with-twitter-data)
7. [How to calculate features and metrics that contribute to topic trending](#7-how-to-calculate-features-and-metrics-that-contribute-to-topic-trending)
8. [How to train a classifier to predict if a hashtag will trend on Twitter](#8-how-to-train-a-classifier-to-predict-if-a-hashtag-will-trend-on-twitter)

If you have any questions or concerns about this study, please reach out! Jessie.Smith-1@colorado.edu

## 1. How to create an AWS DynamoDB and connect to it
To create your first DynamoDB on AWS, [follow this tutorial](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SettingUp.DynamoWebService.html). I recommend checking out [this tutorial](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html) to make sure that you can connect to your DynamoDB in Python and on your local machine.

For this tutorial, you will need to create two DynamoDBs (both can be made with the free tier):
1. TweetStream (the key must be named "id" and will be a number - the Tweet ID)
2. trendTable (the key must be named "id" and will be a string - the time stamp of this trend array)

*Note: You will have to configure your local machine to include your AWS credentials. You should end up with a ".aws" folder that contains a config and credentials file. The ".aws" folder will need to be in the directory that you run your code, or you can set global environemnt variables to configure your device to connect to your AWS account.*

## 2. How to create a Twitter Developer account and connect to it

To get a Twitter Developer account, you need to [apply for access](https://developer.twitter.com/en/apply-for-access). Once accepted, you will need to gather four different keys:
1. API key
2. Secret API key
3. Access token
4. Secret Access Token

You will need this information for the next step.

## 3. How to stream 1% of all tweets world wide and store them in your DynamoDB

To begin collecting data, you will need to run the [scrape_twitter_data.py](https://github.com/jesmith14/TwitterTrends/blob/master/scrape_twitter_data.py) file. Make sure you run this file on your machine in the same directory as the ".aws" folder.

To run the script to collect tweets from Tweepy's streaming API, you wil likely need to import some libraries. All libraries can be installed using the command: `pip install [LIBRARY NAME]`

Run this command in your terminal to begin collecting streamed tweets and storing them in your TweetStream DynamoDB:
`stream_twitter_data.py Tweets`

You will know the script is running correctly if it prints out a time stamp and the first few characters of every tweet. Right now, the code is written to collect only 1/10 of all Tweets from the 1% sample that Tweepy's stream provides. If you would like to collect more or less than this, modify line 73 `if self.tweet_count % 10 == 0:` to filter for your preferred number of tweets.

## 4. How to collect Twitter trend data from the Twitter API every 5 minutes and store it in your DynamoDB

To begin collecting trend data, you will need to run the [scrape_twitter_data.py](https://github.com/jesmith14/TwitterTrends/blob/master/scrape_twitter_data.py) file. Make sure you run this file on your machine in the same directory as the ".aws" folder.

To collect Twitter trend data, you will need to make a call to the Twitter API every five minutes (more than this is not necessary as world wide trends do not change frequently enough to need to make additional calls). **Be careful while testing this code, if you make too many calls to the Twitter API in one minute, you may be blocked for a period of time**.

To run the script to collect trends, you wil likely need to import some libraries. All libraries can be installed using the command: `pip install [LIBRARY NAME]`

Run this command in your terminal to begin collecting trends and storing them in your trendTable DynamoDB:
`stream_twitter_data.py Trends`

You will know the script is running correctly if it prints out a time stamp for every Trend array collected. Right now, the code is written to run this command every 5 minutes. If you would like to collect more or less than this, modify line 91 `threading.Timer(300.0, gatherTrends).start()` to run it more or less than every 300 seconds.

*Notes: 
1. You will need to run the streaming script and the trend script at the same time in different terminal windows in order to gather trend data at the same time as the tweet data.
2. Alternatively, instead of running these scripts locally, you can run these scripts inside of an EC2 instance to collect continuously without time gaps, but I advise caution because you will need to add more code in for error handling in the event of a stream timeout. You will also need to configure your EC2 instance to include the AWS configuration data that you now have on your machine.*

## 5. How to convert DynamoDB data into a csv

For this report, I ran the scripts above intermittently for five days. In order to gather all of the collected data from the DynamoDBs, I used the library [DynamoDBtoCSV](https://github.com/edasque/DynamoDBtoCSV). This allowed me to get my total collection of trend arrays and streamed tweets over the course of the five days in two csv files.

If you would like to use these csvs in the [Tutorial.ipynb](some link here) notebook, you will need to save them as 'tweets.csv' and 'trends.csv'

Alternatively, you can use the csvs that I created for the study, saved in this GitHub repo with the same name as above.
- [tweets.csv](some link here)
- [trends.csv](some link here)

## 6. How to clean and work with Twitter data
Refer to section #2 of the [Tutorial.ipynb](https://github.com/jesmith14/TwitterTrends/blob/master/Tutorial.ipynb)

## 7. How to calculate features and metrics that contribute to topic trending
Refer to the last part of section #2 of the [Tutorial.ipynb](https://github.com/jesmith14/TwitterTrends/blob/master/Tutorial.ipynb)

## 8. How to train a classifier to predict if a hashtag will trend on Twitter
Refer to section #3 the [Tutorial.ipynb](https://github.com/jesmith14/TwitterTrends/blob/master/Tutorial.ipynb)

<hr/>

Congratulations! :tada: :confetti_ball: If you made it this far, you reverse engineered the Twitter trending algorithm (for hashtags) with an accuracy of about 93%! Together, we can work to make black boxes a little bit less opaque, and a little bit more *transparent*.

If you have any questions / concerns / comments about this tutorial or would like to add to it, please reach out! Jessie.Smith-1@colorado.edu
