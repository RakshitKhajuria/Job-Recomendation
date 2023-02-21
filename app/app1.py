import pdfplumber
import streamlit as st
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords 
from string import punctuation
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
import pandas as pd 
from nltk.collocations import *
import re
import plotly.express as px
import time
import sys
import streamlit
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
#%%
# Ignore warning
st.set_option('deprecation.showPyplotGlobalUse', False)
# set wide layout
st.set_page_config(layout="wide")

def app():
    # (OCR function)
    def extract_data(feed):
        text=''
        with pdfplumber.open(feed) as pdf:
            pages = pdf.pages
            for page in pages:
                text+=page.extract_text(x_tolerance=2)
        return text
    
    # Title & select boxes
    st.title('Job Recommendation')
    # cv=st.file_uploader('Upload your CV', type='pdf')
    c1, c2 = st.columns((3,2))
    # upload cv + turn pdf to text------------------display##
    cv=c1.file_uploader('Upload your CV', type='pdf')
    # career level
    levels = ["Entry Level","Middle", "Senior", "Top", "Not Specified"]
    CL = c2.multiselect('Career level', levels, levels)
        
    # number of job recommend slider------------------display##
    no_of_jobs = st.slider('Number of Job Recommendations:', min_value=20, max_value=100, step=10)

    if cv is not None:
        cv_text = extract_data(cv)
            # print(cv_text)

        #----------------------------workings---------------------#

        # (NLP funtion)
        # import stop word lists for NLP function

        #(NLP keywords function)
        @st.cache_data
        def nlp(x):
            word_sent = word_tokenize(x.lower().replace("\n",""))
            _stopwords = set(stopwords.words('english') + list(punctuation)+list("●")+list('–')+list('’'))
            word_sent=[word for word in word_sent if word not in _stopwords]
            lemmatizer = WordNetLemmatizer()
            NLP_Processed_CV = [lemmatizer.lemmatize(word) for word in word_tokenize(" ".join(word_sent))]
        #     return " ".join(NLP_Processed_CV)
            return NLP_Processed_CV
        
        # (NLP keywords for CV workings)
        try:
            NLP_Processed_CV=nlp(cv_text)
        except NameError:
            st.error('Please enter a valid input')
        #NLP_Processed_CV=func(cv_text)
        
        # put CV's keywords into dataframe
        df2 = pd.DataFrame()
        # append columns to an empty DataFrame
        df2['title'] = ["I"]
        df2['job highlights'] = ["I"]
        df2['job description'] = ["I"]
        df2['company overview'] = ["I"]
        df2['industry'] = ["I"]

        # Compare with the entire CV
        df2['All'] = " ".join(NLP_Processed_CV)

        # import whole nlp csv
        @st.cache_data #method to get data once and store in cache.
        def get_jobcsv():
            url='preprocessed_jobs.csv'
            return pd.read_csv(url)
        df= get_jobcsv()

        # recommendation function
        @st.cache_data
        def get_recommendation(top, df_all, scores):
            recommendation = pd.DataFrame(columns = ['positionName', 'company',"location",'JobID','description','score'])
            count = 0
            for i in top:
        #         recommendation.at[count, 'ApplicantID'] = u
                
                recommendation.at[count, 'positionName'] = df['positionName'][i]
                recommendation.at[count, 'company'] = df['company'][i]
                recommendation.at[count, 'location'] = df['location'][i]
            
                recommendation.at[count, 'JobID'] = df.index[i]
                recommendation.at[count, 'description'] = df['description'][i]
                recommendation.at[count, 'score'] =  scores[count]
                count += 1
            return recommendation


        from sklearn.metrics.pairwise import cosine_similarity
        from sklearn.feature_extraction.text import TfidfVectorizer

        @st.cache_data
        def TFIDF(scraped_data, cv):
            tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            # TF-IDF Scraped data
            tfidf_jobid = tfidf_vectorizer.fit_transform(scraped_data)
            # TF-IDF CV
            user_tfidf = tfidf_vectorizer.transform(cv)
            # Using cosine_similarity on (Scraped data) & (CV)
            cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf,x),tfidf_jobid)
            output2 = list(cos_similarity_tfidf)
            return output2  # what does it return?
        output2 = TFIDF(df['All'], df2['All'])
        
        # show top job recommendations using TF-IDF
        top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:1000]
        list_scores = [output2[i][0][0] for i in top]
        TF=get_recommendation(top,df, list_scores)

        #st.dataframe(TF) #####Show TF

        # Count Vectorizer function
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        @st.cache_data
        def count_vectorize(scraped_data, cv):
            # CountV the scraped data
            count_vectorizer = CountVectorizer()
            count_jobid = count_vectorizer.fit_transform(scraped_data) #fitting and transforming the vector
            # CountV the cv
            user_count = count_vectorizer.transform(cv)
            cos_similarity_countv = map(lambda x: cosine_similarity(user_count, x),count_jobid)
            output3 = list(cos_similarity_countv)
            return output3
        output3 = count_vectorize(df['All'], df2['All'])
    
        # show top job recommendations using Count Vectorizer
        top = sorted(range(len(output3)), key=lambda i: output3[i], reverse=True)[:1000]
        list_scores = [output3[i][0][0] for i in top]
        cv=get_recommendation(top, df, list_scores)

        # KNN function
        from sklearn.neighbors import NearestNeighbors

        @st.cache_data   
        def KNN(scraped_data, cv):
            tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            n_neighbors = 1000
            KNN = NearestNeighbors(n_neighbors, p=2)
            KNN.fit(tfidf_vectorizer.fit_transform(scraped_data))
            NNs = KNN.kneighbors(tfidf_vectorizer.transform(cv), return_distance=True)
            top = NNs[1][0][1:]
            index_score = NNs[0][0][1:]
            knn = get_recommendation(top, df, index_score)
            return knn
        knn = KNN(df['All'], df2['All'])

         ############ SHOW KNN
        #%%
        # Combine 3 methods into a dataframe
        merge1 = knn[['JobID','positionName', 'score']].merge(TF[['JobID','score']], on= "JobID")
        final = merge1.merge(cv[['JobID','score']], on = "JobID")
        final = final.rename(columns={"score_x": "KNN", "score_y": "TF-IDF","score": "CV"})
        # final.head()

        #%%
        
        # Scale it
        from sklearn.preprocessing import MinMaxScaler
        slr = MinMaxScaler()
        final[["KNN", "TF-IDF", 'CV']] = slr.fit_transform(final[["KNN", "TF-IDF", 'CV']])

        # Multiply by weights
        final['KNN'] = (1-final['KNN'])/3
        final['TF-IDF'] = final['TF-IDF']/3
        final['CV'] = final['CV']/3
        final['Final'] = final['KNN']+final['TF-IDF']+final['CV']
        final.sort_values(by="Final", ascending=False)
        
        #job recommendations after career level & no. of jobs filter
        # @st.cache
        # def Job_recomm(x):
        #     final_ = final[['JobID','title','career level','company','location','industry']]
        #     st.dataframe(final_)
        #     # cl_select = final_[final_["career level"]==CL]
        #     st.dataframe(cl_select)
        #     return cl_select
        final2 = final.sort_values(by="Final", ascending=False).copy()
        final_df = df.merge(final2, on="JobID" )
        final_df = final_df.sort_values(by="Final", ascending=False)
        final_df.fillna('Not Available', inplace=True)



        st.dataframe(final_df)
        # df_fin = final2.merge(df, on="JobID")
        def Job_recomm(x):
            final_ = final[['JobID','company','positionName','description','salary','location','rating', 'postedAt', 'externalApplyLink']]
            selected_levels = final_['career level'].isin(CL)
            cl_select = final_[selected_levels]
            return cl_select
        
        # result_jd = Job_recomm(CL)
        # result_jd = final
        # final_jobrecomm =result_jd.head(no_of_jobs)


if __name__ == '__main__':
        app()
##kfnsajnfs