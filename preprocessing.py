import numpy as np
import pandas as pd
import re

from pymongo import MongoClient

from textblob import TextBlob

config = {
	'host': '3.17.23.52:27017',
    'username': 'mongo_user',
    'password': 'project-fletcher',
    'authSource': 'tweets'
}

def clean_tweet(tweet):

	lower_case = tweet.lower()

	strip_new_lines = re.sub('\n',' ',lower_case)
	strip_links = re.sub('http[^ ]+',' ',strip_new_lines)
	strip_usernames = re.sub('@[^ ]+', ' ',strip_links)
	strip_ccs = re.sub('cc:',' ',strip_usernames)
	strip_not_letters = re.sub("[^a-zA-Z]", ' ', strip_ccs)
	strip_rts = re.sub('^rt', ' ', strip_not_letters)

	return strip_rts

def get_clean_tweets(config=config,subset=None):

	client = MongoClient(**config)
	db = client.tweets

	cursor = db.ds_tweets.find()

	tweets = []

	if subset == None:
		while True:
			try:
				tweets.append(cursor.next())
			except:
				break
	else:
		for _ in range(subset):
			tweets.append(cursor.next())

	documents = []

	for tweet in tweets:
	    if 'delete' not in tweet.keys():
	        try:
	            documents.append(tweet['retweeted_status']['extended_tweet']['full_text'])
	        except:
	            try:
	                documents.append(tweet['extended_tweet']['full_text'])
	            except:
	                documents.append(tweet['text'])

	clean_tweets = []

	for tweet in documents:
		clean_tweets.append(clean_tweet(tweet))

	return clean_tweets

if __name__ == '__main__':

	get_clean_tweets(config=config)
