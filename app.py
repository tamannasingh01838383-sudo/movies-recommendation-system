import streamlit as st
import pickle
import pandas as pd
import requests
import streamlit as st



API_KEY = "e4b1e7d793db788defbcadb22224ccd6"
session = requests.Session()

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e4b1e7d793db788defbcadb22224ccd6&language=en-US"
            response = session.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get("poster_path")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                # fallback if poster_path is missing
                return "https://via.placeholder.com/300x450?text=No+Poster"
        except Exception as e:
            print(f"Error fetching poster for movie_id={movie_id}: {e}")
            return "https://via.placeholder.com/300x450?text=Error"


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

import gdown
import pickle
import os

# File ID from your Google Drive link
file_id = "1pPpFWlP45oETFjzoDIGaZjsblY2LwrCp"
url = f"https://drive.google.com/uc?id=1pPpFWlP45oETFjzoDIGaZjsblY2LwrCp"
output = "similarity.pkl"

# Download only if it doesn't already exist
if not os.path.exists(output):
    print("Downloading similarity.pkl from Google Drive...")
    gdown.download(url, output, quiet=False)

# Now load the file
with open(output, "rb") as f:
    similarity = pickle.load(f)

print("similarity.pkl loaded successfully!")
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






