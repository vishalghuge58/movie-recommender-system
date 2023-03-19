import pickle
import pandas as pd
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=290c56582df36f9e41f90ba8edf56fad&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movies = pickle.load(open('movies_dict.pkl','rb'))
    similarity = pickle.load(open('tf_similarity.pkl', 'rb'))
    movies = pd.DataFrame(movies)
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommend_poster = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        recommend_poster.append(fetch_poster(movie_id))
    return recommended_movies , recommend_poster

@app.route('/', methods=['GET', 'POST'])
def home():
    movies = pickle.load(open('movies_dict.pkl','rb'))
    movies_list = pd.DataFrame(movies)['title'].tolist()
    if request.method == 'POST':
        selected_movie = request.form.get('selected_movie')
        if selected_movie:
            names, posters = recommend(selected_movie)
            return render_template('index.html', movie_list=movies_list, selected_movie=selected_movie, names=names, posters=posters,zip = zip)
    return render_template('index.html', movie_list=movies_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080)