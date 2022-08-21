import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
	'''
	This function returns the poster path for the given movie id

	Parameters:
		movie_id :: int
			ID of movie
	Returns:
		poster_path :: str
			path of poster
	'''

	response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=fdcd4c35b6edbc6d4c1bb8a2cd72abc2'.format(movie_id))
	data = response.json()
	poster_path = 'https://image.tmdb.org/t/p/original'+data['poster_path']

	return poster_path

def recommend(movie):
    '''
    This functions lists top 5 movies similar to the movie passed
    
    Parameters:
        movie :: str
            Name of movie
    '''
    
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:6]
    
    recommended_movies = []
    for _ in movies_list:
        recommended_movies.append([movies.iloc[_[0]].title, fetch_poster(movies.iloc[_[0]].movie_id)])

    return recommended_movies

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select Movie', movies_list)


if st.button('Recommend'):
	names = []
	posters = []
	for movie in recommend(selected_movie_name):
		names.append(movie[0])
		posters.append(movie[1])

	col1, col2, col3, col4, col5 = st.columns(5)

	with col1:
		st.text(names[0])
		st.image(posters[0])

	with col2:
		st.text(names[1])
		st.image(posters[1])

	with col3:
		st.text(names[2])
		st.image(posters[2])

	with col4:
		st.text(names[3])
		st.image(posters[3])

	with col5:
		st.text(names[4])
		st.image(posters[4])
