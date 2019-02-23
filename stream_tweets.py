import pandas as pd
import numpy as np
import json
import pickle

import tweepy
from pymongo import MongoClient

import data_scientists

config = {
    'host': '127.0.0.1:27017',
    'username': 'mongo_user',
    'password': 'project-fletcher',
    'authSource': 'tweets'
}

client = MongoClient(**config)

db = client.tweets
api = data_scientists.get_api()
user_list = data_scientists.get_mongo_ids(config)

class MyStreamListener(tweepy.StreamListener):

	def __init__(self, follow, db, api):
		super().__init__()
		self.following = follow
		self.db = db
		self.api = api

	def on_data(self, data):
		tweet = json.loads(data)

		if 'id' in tweet.keys():

			print('Tweet:', tweet['id'])
			self.db.ds_tweets.insert_one(tweet)

		if 'in_reply_to_user_id_str' in tweet.keys() and tweet['in_reply_to_user_id_str'] != None:
			if tweet['in_reply_to_user_id_str'] not in self.following:

				print('User:', tweet['in_reply_to_user_id_str'])

				user = self.api.get_user(tweet['in_reply_to_user_id'])
				self.db.ds_users.insert_one(user._json)

				self.following.append(tweet['in_reply_to_user_id_str'])

	def on_error(self, status_code):
		print(status_code)
		if status_code == 420:
			return False

myStreamListener = MyStreamListener(user_list, db, api)
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

if __name__ == '__main__':
	
	print('Following:', len(myStreamListener.following))
	myStream.filter(follow=myStreamListener.following)
		