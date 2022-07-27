import pandas as pd
import numpy as np
import pickle
from flask import Flask, request, jsonify, render_template
import difflib
import requests

app = Flask(__name__)

def fetch_poster(movie_id):
	url='https://api.themoviedb.org/3/movie/{}?api_key=bfd470bb347673be6f880519447e4b68&language=en-US'.format(movie_id)
	response=requests.get(url)
	data=response.json()
	return 'https://image.tmdb.org/t/p/w500'+data['poster_path']

movies_data=pickle.load(open('movies_data.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movie_features_df=pickle.load(open('movie_features_df.pkl','rb'))
user=pickle.load(open('user.pkl','rb'))

@app.route('/')
def man():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def home():
    movie_name=request.form['movie']
    titles=movies_data['title'].values
    find_close_match = difflib.get_close_matches(movie_name,titles)
    recommend_movies=[]
    collab=[]
    card=[]
    if len(find_close_match)==0:
        return render_template('home.html',names=recommend_movies,collab=collab,card=card)
    closest_match = find_close_match[0]

    index_movie=movies_data[movies_data.title==closest_match]['index'].values[0]
    similarity_score=list(enumerate(similarity[index_movie]))
    sorted_similar=sorted(similarity_score,key=lambda x:x[1],reverse=True)
    movie_title='1'
    rel_dat='1'
    run_time='1'
    genre='1'
    desc='1'
    post='1'
    i=0
    for movie in sorted_similar:
        index=movie[0]
        title_from_index=movies_data[movies_data.index==index]['title'].values[0]
        id_from_index=movies_data[movies_data.index==index]['id'].values[0]
        if i==0:
            movie_title=title_from_index
            post=fetch_poster(id_from_index)
            run_time=movies_data[movies_data.index==index]['runtime'].values[0]
            desc=movies_data[movies_data.index==index]['overview'].values[0]
            genre=movies_data[movies_data.index==index]['genres'].values[0]
            rel_dat=movies_data[movies_data.index==index]['release_date'].values[0]
            rel_dat=rel_dat[0:4]
            i+=1  
        elif i<7:
            recommend_movies.append((title_from_index,fetch_poster(id_from_index)))
            i+=1
        else:
            break
    
    card.append(movie_title)
    card.append(post)
    card.append(rel_dat)
    card.append(run_time)
    card.append(genre)
    card.append(desc)
    query_index=-1
    for i in range(0,len(movie_features_df)):
        n=movie_features_df.index[i][0]
        k=0
        for j in range(0,len(n)):
            if n[j]==' ':
                k=j
        m=n[0:k]
        j=m.find(', The')
        if j!=-1:
            m='The '+m[0:j]+m[j+5:k+1]
        if m==closest_match:
            query_index=i
            break
    if query_index==-1:
        return render_template('home.html',names=recommend_movies,collab=collab,card=card)
    similar_score = list(enumerate(user[query_index]))
    similar_movies = sorted(similar_score, key = lambda x:x[1], reverse = True) 
    i=0
    for movie in similar_movies:
        ind=movie[0]
        title_from_index=movie_features_df.index[ind][0]
        id_from_index=-1
        if i==0:
            i+=1
        elif i<7:
            for j in range(0,len(title_from_index)):
                if title_from_index[j]==' ':
                    k=j
            m=title_from_index[0:k]
            j=m.find(', The')
            if j!=-1:
                m='The '+m[0:j]+m[j+5:k+1]

            for j in range(0,len(movies_data)):
                if movies_data.iloc[j]['title']==m:
                    id_from_index=movies_data.iloc[j]['id']
                    break
            if id_from_index!=-1:
                collab.append((m,fetch_poster(id_from_index)))
                i+=1

        else:
            break
    
    return render_template('home.html',names=recommend_movies,collab=collab,card=card)

if __name__ == "__main__":
    app.run(debug=True)