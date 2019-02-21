import numpy as np
import pandas as pd

import tweepy
import json
import time

from pymongo import MongoClient

from twitter_credentials import credentials

def get_api(consumer_key=credentials['TWITTER_CONSUMER_KEY'],consumer_secret=credentials['TWITTER_CONSUMER_KEY_SECRET'],
	access_token_key=credentials['TWITTER_ACCESS_TOKEN'],access_token_secret=credentials['TWITTER_ACCESS_TOKEN_SECRET']):

	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token_key,access_token_secret)

	api = tweepy.API(auth)

	return api

def handle_limit(cursor):
	while True:
		try:
			cursor.next()
		except tweepy.TweepError:
			time.sleep(15 * 60)
			continue
		except StopIteration:
			break

def get_seed_list(api=get_api(), username='stephenilhardt', twitter_list='data-scientists'):

	user_list = []

	for user in tweepy.Cursor(api.list_members, username, twitter_list, tweet_mode='extended').items():

		if user.friends_count <= 5000:
			user_list.append(user)

	return user_list
	
def get_data_scientists(api=get_api(), seed_list=get_seed_list()):

	ds_accounts = pd.DataFrame(columns=['name','id','counter'])

	for user in seed_list:
		for friends_id in handle_limit(tweepy.Cursor(api.friends_ids, user._json['id']).items()):
			friend_frame = pd.DataFrame()

			friend_frame['name'] = user._json['name']
			friend_frame['id'] = friends_id
			friend_frame['counter'] = 1

			ds_accounts.append(friend_frame)

	return ds_accounts
