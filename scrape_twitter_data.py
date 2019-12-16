import datetime
import calendar
import tweepy
import json
import boto3
import sys
import threading

class TwitterAPI():
    def __init__(self):
        self.api_key = 'CYNk3gteB84Yc74GHuB5HMQHy'
        self.api_secret = 'hlscuCisPhrfL1bD2aA5igLp95pbQW4jNxaWXtPgSAjDpSkIS1'
        self.access_token = '764225096642736128-MWzQKUROrQe9Ha7fHQoGI0pWwnJrtbC'
        self.access_secret = '9gPX4hpP7bMPvaUxI87FMC8MdcMju89OO6nWVCiRyerJY'
        self.auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        self.auth.set_access_token(self.access_token, self.access_secret)
        self.api = tweepy.API(self.auth)
        self.trendTable = DataBase().trendTable

    def addTrendsToDB(self):
        api = self.api
        currentTrends = api.trends_place(1)[0]
        d1 = datetime.datetime.strptime(currentTrends['created_at'],"%Y-%m-%dT%H:%M:%SZ")
        calendar.month_name[d1.month][:3]
        new_format = calendar.month_name[d1.month][:3] + " %d %H:%M"
        time = d1.strftime(new_format)
        trends = set()
        for trend in currentTrends['trends']:
            trends.add(trend['name'])
        # print('* adding to the trends DB:')
        print('* time: ', time)
        self.trendTable.put_item(
            Item={
                'id':time,
                'trends':trends
            }
        )

class DataBase():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        self.client = boto3.client('dynamodb', region_name='us-east-2')
        self.tweetTable = self.dynamodb.Table('TweetStream')
        self.trendTable = self.dynamodb.Table('trendTable')

class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.tweet_count = 0
        self.word_counts = {}
        self.totals = {}

        self.tweetTable = DataBase().tweetTable

        
    def addNewTweetToDB(self, newData):
        #add the new tweet json to the DB (new tweet DB)
        print("# :" + newData['time'] + newData['text'][:5] + "...")
        self.tweetTable.put_item(
           Item={
                'id': newData['id'],
                'time': newData['time'],
                'text': newData['text']
            }
        )

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
    
    def on_data(self, data):
        self.tweet_count += 1
        if self.tweet_count % 10 == 0:
            data = json.loads(data)
            if'text' in data:
                newData = {}
                newData['text'] = data['text']
                newData['time'] = data['created_at'][4:16]
                newData['id'] = data['id']
                self.addNewTweetToDB(newData)

def gatherTweets():
    print('gathering tweets...')
    myListener = MyStreamListener()
    api = TwitterAPI()
    myStream = tweepy.Stream(auth=api.auth, listener=myListener)
    myStream.sample()

def gatherTrends():
    print('gathering trends...')
    threading.Timer(300.0, gatherTrends).start()
    api = TwitterAPI()
    api.addTrendsToDB()

def main():
    print('running')
    if(sys.argv[1] == 'Tweets'):
        gatherTweets()
    elif(sys.argv[1] == 'Trends'):
        # threading.Timer(15.0, gatherTrends).start()
        gatherTrends()


main()
  

