import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

def get_count_vectorized(documents):

	cv = CountVectorizer(stop_words = 'english')

	cv_transformed = cv.fit_transform(documents)

	return cv_transformed, cv.get_feature_names()

def get_tfidf_vectorized(documents):

	tfidf = TfidfVectorizer(stop_words = 'english')

	tfidf_transformed = tfidf.fit_transform(documents)

	return tfidf_transformed, tfidf.get_feature_names()