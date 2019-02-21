import pandas as pd
import numpy as np

import tweepy
from pymongo import MongoClient

import json



class MyStreamingListener(tweepy.StreamListener):

	def __init__():
		super().__init__()

	def on_status(self, status):
		clean_tweet = process_tweet(status)
		db.

	def on_error(self, status_code):
		print(status_code)
		if status_code == 420:
			return False

	def clean_tweet(self, tweet):
		json_dict = json.load(tweet)
		tweet_dict = {
			''
		}
		return tweet_dict


streamer = tweepy.StreamListener
