import pandas as pd
import numpy as np
import json

import tweepy
from pymongo import MongoClient

import data_scientists

config = {
    'host': '3.17.25.213:27017',
    'username': 'project-fletcher',
    'password': 'fletcher1234',
    'authSource': 'tweets'
}

client = MongoClient(**config)

db = client.tweets
tweet_collection = db.ds_tweets

api = data_scientists.get_api()

user_list = []

for user in tweepy.Cursor(api.list_members, 'stephenilhardt', 'data_scientists', tweet_mode='extended').items():
	user_list.append(user)

class MyStreamListener(tweepy.StreamListener):

	def __init__():
		super().__init__()

	def on_data(self, data):
		tweet = json.loads(data)
		
		db.ds_tweets.insert(tweet)

	def on_error(self, status_code):
		print(status_code)
		if status_code == 420:
			return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

stream.filter(track=)


		