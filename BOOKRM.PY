import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(page_title='Book Recommender System', layout='wide')

# Load preprocessed data
@st.cache_data
def load_data():
    popular_df = pickle.load(open('popular.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    books = pickle.load(open('books.pkl', 'rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
    return popular_df, pt, books, similarity_scores

popular_df, pt, books, similarity_scores = load_data()

# Function to recommend books
def recommend(book_name):
    if book_name not in pt.index:
        return []
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    recommendations = []
    for i in similar_items:
        book_title = pt.index[i[0]]
        book_info = books[books['Book-Title'] == book_title].iloc[0]
        recommendations.append({
            'title': book_title,
            'author': book_info['Book-Author'],
            'image': book_info['Image-URL-M'],
            'score': i[1]
        })
    return recommendations

# Streamlit app UI
st.markdown(
    """
    <style>
    .header {
        font-size: 48px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.25rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .subheader {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .card {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgb(0 0 0 / 0.05);
        padding: 1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .book-title {
        font-weight: 600;
        font-size: 20px;
        margin-top: 0.5rem;
        color: #111827;
    }
    .book-author {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.markdown('<div class="header">Book Recommender System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subheader">Find similar books you will love by selecting one from the popular collection.</div>', 
    unsafe_allow_html=True
)

# Book selection
selected_book = st.selectbox(
    'Select a book to get recommendations:',
    options=popular_df['Book-Title'].values
)

# Show recommendations
if selected_book:
    st.markdown(f"### Books similar to \"{selected_book}\"")
    recommendations = recommend(selected_book)
    if not recommendations:
        st.info("Sorry, no recommendations found for the selected book.")
    else:
        # Display the recommended books in columns as cards
        cols = st.columns(len(recommendations))
        for col, rec in zip(cols, recommendations):
            with col:
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                st.image(rec['image'], width=120, caption=rec['title'])
                st.markdown(f'<div class="book-title">{rec["title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="book-author">by {rec["author"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
