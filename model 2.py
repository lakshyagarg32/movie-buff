import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import pickle

movies_df = pd.read_csv('movies.csv',usecols=['movieId','title'],dtype={'movieId': 'int32', 'title': 'str'})
rating_df=pd.read_csv('ratings.csv',usecols=['userId', 'movieId', 'rating'],
    dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

df = pd.merge(rating_df,movies_df,on='movieId')

combine_movie_rating = df.dropna(axis = 0, subset = ['title'])
movie_ratingCount = (combine_movie_rating.
     groupby(by = ['title'])['rating'].
     count().
     reset_index().
     rename(columns = {'rating': 'totalRatingCount'})
     [['title', 'totalRatingCount']]
    )

rating_with_totalRatingCount = combine_movie_rating.merge(movie_ratingCount, left_on = 'title', right_on = 'title', how = 'left')

popularity_threshold = 0
rating_popular_movie= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')

movie_features_df=rating_popular_movie.pivot_table(index=['title','movieId'],columns='userId',values='rating').fillna(0)


movie_features_df_matrix = csr_matrix(movie_features_df.values)
similarity = cosine_similarity(movie_features_df)

pickle.dump(movie_features_df,open('movie_features_df.pkl','wb'))
pickle.dump(similarity,open('user.pkl','wb'))

