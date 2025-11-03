import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e4b1e7d793db788defbcadb22224ccd6&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster for movie_id={movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]]['title'])
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))


    return recommended_movies,recommended_movies_posters


movies_dict =pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    sorted(movies['title'].unique())
)

if st.button('Recommend', key='recommend_button'):
    names, posters = recommend(selected_movie_name)

    if names:
        cols = st.columns(len(names))
        for idx, col in enumerate(cols):
            with col:
                st.text(names[idx])
                st.image(posters[idx])
    else:
        st.warning("No similar movies found. Try another title!")


import pickle
import gdown

# Replace with your own Google Drive file ID
url = "https://drive.google.com/uc?export=download&id=1pPpFWlP45oETFjzoDIGaZjsblY2LwrCp"
output = "similarity.pkl"
gdown.download(url, output, quiet=False)

with open(output, "rb") as file:
    similarity = pickle.load(file)



