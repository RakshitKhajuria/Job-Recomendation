import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords 
from string import punctuation
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.collocations import *
from nltk.corpus import words
import pandas as pd
from  JobRecommendation.exception import jobException
import os,sys
import numpy as np
import streamlit as st
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('words')
@st.cache_data
def nlp(x):
    try:
        word_sent = word_tokenize(x.lower().replace("\n",""))
        _stopwords = set(stopwords.words('english') + list(punctuation)+list("●")+list('–')+list('’'))
        word_sent=[word for word in word_sent if word not in _stopwords]
        lemmatizer = WordNetLemmatizer()
        NLP_Processed = [lemmatizer.lemmatize(word) for word in word_tokenize(" ".join(word_sent))]
        #     return " ".join(NLP_Processed_CV)
        return NLP_Processed
    except Exception as e:
            raise jobException(e, sys)