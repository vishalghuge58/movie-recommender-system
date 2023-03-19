import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=290c56582df36f9e41f90ba8edf56fad&language=en-US".format(movie_id)

    response = requests.get(url)
    data = response.json()
    full_path = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    return full_path


movies = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('tf_similarity.pkl', 'rb'))

movies = pd.DataFrame(movies)


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
        recommend_poster.append(fetch_poster(movie_id))

    return recommended_movies , recommend_poster


# Set page title and favicon
st.set_page_config(page_title='Movie Recommender System', page_icon=':movie_camera:')

# Set app title and description
st.title("Movie Recommender System")
st.write("This app recommends similar movies based on the selected movie.")

# Set user input
selected_movie = st.selectbox("Select a movie", movies['title'].values)

# Set recommendation button
if st.button("Get Recommendations"):

    # Get recommendations
    recommended_movies, recommended_posters = recommend(selected_movie)

    # Set recommendation header
    st.subheader(f"Movies Similar to {selected_movie}:")

    # Set recommendation cards
    col1, col2, col3, col4, col5 = st.columns(5)

    for i, (movie, poster) in enumerate(zip(recommended_movies, recommended_posters)):
        with eval(f"col{i+1}"):
            st.image(poster, use_column_width=True)
            st.write(f"<p style='text-align: center;'>{movie}</p>", unsafe_allow_html=True)
