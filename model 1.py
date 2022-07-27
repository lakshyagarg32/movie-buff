import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

movies_data = pd.read_csv('movies.csv')

selected_features = ['genres','keywords','tagline','cast','director']
for feature in selected_features:
	movies_data[feature] = movies_data[feature].fillna('')

combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

similarity = cosine_similarity(feature_vectors)

# pickle.dump(movies_data,open('movies_data.pkl','wb'))
# pickle.dump(similarity,open('similarity.pkl','wb'))