import streamlit as st
import pickle
import pandas as pd
import requests


def feth_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=290c56582df36f9e41f90ba8edf56fad&language=en-US".format(movie_id)



    response = requests.get(url)
    data = response.json()
    full_path = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    return full_path


movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('tf_similarity.pkl', 'rb'))


# movies = pd.DataFrame(movies)



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommend_poster = []
    for i in movies_list:
        
    
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id

        # fetching_movie_posters
        recommend_poster.append(feth_poster(movie_id))


    return recommended_movies , recommend_poster



movies_list = movies['title'].values


st.title("Movie Recommender Sysytem")

selected_movie = st.selectbox("Select the movies" , movies_list)



if st.button("Recommend"):
    names , posters = recommend(selected_movie)

    col1,col2,col3,col4,col5  = st.columns(5)

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


