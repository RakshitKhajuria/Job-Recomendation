from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from  JobRecommendation.exception import jobException
import streamlit as st
import sys
@st.cache_data
def TFIDF(scraped_data, cv):
    try:
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        # TF-IDF Scraped data
        tfidf_jobid = tfidf_vectorizer.fit_transform(scraped_data)
        # TF-IDF CV
        user_tfidf = tfidf_vectorizer.transform(cv)
        # Using cosine_similarity on (Scraped data) & (CV)
        cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf,x),tfidf_jobid)
        output2 = list(cos_similarity_tfidf)
        return output2  # what does it return?
    except Exception as e:
        raise jobException(e, sys)
@st.cache_data
def count_vectorize(scraped_data, cv):
    try:
        # CountV the scraped data
        count_vectorizer = CountVectorizer()
        count_jobid = count_vectorizer.fit_transform(scraped_data) #fitting and transforming the vector
        # CountV the cv
        user_count = count_vectorizer.transform(cv)
        cos_similarity_countv = map(lambda x: cosine_similarity(user_count, x),count_jobid)
        output3 = list(cos_similarity_countv)
        return output3
    except Exception as e:
        raise jobException(e, sys)

@st.cache_data
def KNN(scraped_data, cv,number_of_neighbors):
    try:
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        # n_neighbors = 100
        KNN = NearestNeighbors(n_neighbors = number_of_neighbors, p=2)
        KNN.fit(tfidf_vectorizer.fit_transform(scraped_data))
        NNs = KNN.kneighbors(tfidf_vectorizer.transform(cv), return_distance=True)
        top = NNs[1][0][1:]
        index_score = NNs[0][0][1:]
        
        return top ,index_score
    except Exception as e:
        raise jobException(e, sys)
