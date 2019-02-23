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
tweet_collection = db.ds_tweets

api = data_scientists.get_api()

user_list = data_scientists.get_list_ids(api=api)

class MyStreamListener(tweepy.StreamListener):

	def __init__(self, follow):
		super().__init__()
		self.following = follow

	def on_data(self, data):
		tweet = json.loads(data)

		if 'id' in tweet.keys():
			print('Tweet:', tweet['id'])

		if 'in_reply_to_user_id_str' in tweet.keys() and tweet['in_reply_to_user_id_str'] != None:
			if tweet['in_reply_to_user_id_str'] not in self.following:

				print('User:', tweet['in_reply_to_user_id_str'])
				api.add_list_member(owner_screen_name='stephenilhardt',slug='ds-project-list', user_id=tweet['in_reply_to_user_id'])
				self.following.append(tweet['in_reply_to_user_id_str'])

		db.ds_tweets.insert_one(tweet)

	def on_error(self, status_code):
		print(status_code)
		if status_code == 420:
			return False

myStreamListener = MyStreamListener(user_list)
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

if __name__ == '__main__':
	
	#print(myStreamListener.following)
	myStream.filter(follow=myStreamListener.following)
		