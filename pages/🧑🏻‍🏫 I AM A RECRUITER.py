# import pdfplumber
import streamlit as st
import pandas as pd
import numpy as np
import nltk
import os
import base64
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
from nltk.corpus import words
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('words')
st.set_page_config(layout="wide", page_icon='logo/logo2.png', page_title="RECRUITER")

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://www.linkpicture.com/q/logo_19.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "TALENT HIVE";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()

def app():
    # Title & select boxes--------------------------display##
    st.title('Candidate Recommendation')
    # cv=st.file_uploader('Upload your CV', type='pdf')
    c1, c2 = st.columns((3,2))
    # upload jd + turn pdf to text------------------display##
    #try:
    # jd=c1.file_uploader('Upload your JD', type='pdf')
    # number of cv recommend slider------------------display##
    no_of_cv = c2.slider('Number of CV Recommendations:', min_value=0, max_value=6, step=1)
    #%%
    # text area for enter JD
    # default_value_goes_here='hi'
    jd = c1.text_area("PASTE YOUR JOB DESCRIPTION HERE")
    if st.button("Extract"):
        
        if len(jd) >=1:

            def nlp(x):
                word_sent = word_tokenize(x.lower().replace("\n",""))
                _stopwords = set(stopwords.words('english') + list(punctuation)+list("●")+list('–')+list('’'))
                word_sent=[word for word in word_sent if word not in _stopwords]
                lemmatizer = WordNetLemmatizer()
                NLP_Processed_JD = [lemmatizer.lemmatize(word) for word in word_tokenize(" ".join(word_sent))]
                #     return " ".join(NLP_Processed_CV)
                return NLP_Processed_JD


            def remove_stuff(jd):
                jd_clean = jd.replace("\xa0", "").replace("/", "").replace(".", ". ").replace("●", "")
                return jd_clean

            NLP_Processed_JD=nlp(jd)

            jd_df=pd.DataFrame()
            jd_df['jd']=[' '.join(NLP_Processed_JD)]
            def get_recommendation(top, df_all, scores):
                recommendation = pd.DataFrame(columns = ['name', 'degree',"email",'Unnamed: 0','mobile_number','skills','no_of_pages','score'])
                count = 0
                for i in top:
            #         recommendation.at[count, 'ApplicantID'] = u
                    
                    recommendation.at[count, 'name'] = df['name'][i]
                    recommendation.at[count, 'degree'] = df['degree'][i]
                    recommendation.at[count, 'email'] = df['email'][i]
                    recommendation.at[count, 'Unnamed: 0'] = df.index[i]
                    recommendation.at[count, 'mobile_number'] = df['mobile_number'][i]
                    recommendation.at[count, 'skills'] = df['skills'][i]
                    recommendation.at[count, 'no_of_pages'] = df['no_of_pages'][i]
                    recommendation.at[count, 'score'] =  scores[count]
                    count += 1
                return recommendation

            def get_cv(): #cleaned, processed, nlped cv content
                url='cv.csv'
                return pd.read_csv(url) 

            df = get_cv()   
            cv_data=[]
            for i in range(len(df["All"])):
                NLP_Processed_cv=nlp(df["All"].values[i])
                cv_data.append(NLP_Processed_cv)

            cv_=[]
            for i in cv_data:
                cv_.append([' '.join(i)])

            df["clean_all"]=pd.DataFrame(cv_)
            from sklearn.metrics.pairwise import cosine_similarity
            from sklearn.feature_extraction.text import TfidfVectorizer


            def TFIDF(scraped_data, cv):
                tfidf_vectorizer = TfidfVectorizer(stop_words='english')

                # TF-IDF Scraped data
                tfidf_jobid = tfidf_vectorizer.fit_transform(scraped_data)

                # TF-IDF CV
                user_tfidf = tfidf_vectorizer.transform(cv)

                # Using cosine_similarity on (Scraped data) & (CV)
                cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf,x),tfidf_jobid)

                output2 = list(cos_similarity_tfidf)
                return output2

            tf = TFIDF(df['clean_all'],jd_df['jd'])   

            top = sorted(range(len(tf)), key=lambda i: tf[i], reverse=True)[:100]
            list_scores = [tf[i][0][0] for i in top]
            TF=get_recommendation(top,df, list_scores)

            from sklearn.feature_extraction.text import CountVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            def count_vectorize(cv,jd):
                count_vectorizer = CountVectorizer()
                count_jobid = count_vectorizer.fit_transform(df["clean_all"]) #converting job data into vectors using count vectorizers
                user_count = count_vectorizer.transform(jd_df['jd'])#converting user cv data into vectors using count vectorizers
                cos_similarity_countv = map(lambda x: cosine_similarity(user_count, x),count_jobid)
                output3 = list(cos_similarity_countv)
                return output3
            countv = count_vectorize(df['clean_all'],jd_df['jd'])
            top = sorted(range(len(countv)), key=lambda i: countv[i], reverse=True)[:100]
            list_scores = [countv[i][0][0] for i in top]
            cv=get_recommendation(top, df, list_scores)

            from sklearn.neighbors import NearestNeighbors

            def KNN(scraped_data, cv):
                tfidf_vectorizer = TfidfVectorizer(stop_words='english')

                
                KNN = NearestNeighbors(n_neighbors=7,p=2)
                KNN.fit(tfidf_vectorizer.fit_transform(scraped_data))
            #     NNs = KNN.kneighbors(tfidf_vectorizer.transform(cv), return_distance=True)
                NNs = KNN.kneighbors(tfidf_vectorizer.transform(cv))
                top = NNs[1][0][1:]
                index_score = NNs[0][0][1:]

                knn = get_recommendation(top, df, index_score)
                return knn

            knn = KNN(df['clean_all'], jd_df['jd'])

            merge1 = knn[['Unnamed: 0','name', 'score']].merge(TF[['Unnamed: 0','score']], on= "Unnamed: 0")
            final = merge1.merge(cv[['Unnamed: 0','score']], on = 'Unnamed: 0')
            final = final.rename(columns={"score_x": "KNN", "score_y": "TF-IDF","score": "CV"})

            # Scale it
            from sklearn.preprocessing import MinMaxScaler
            slr = MinMaxScaler()
            final[["KNN", "TF-IDF", 'CV']] = slr.fit_transform(final[["KNN", "TF-IDF", 'CV']])

            # Multiply by weights
            final['KNN'] = (1-final['KNN'])/3
            final['TF-IDF'] = final['TF-IDF']/3
            final['CV'] = final['CV']/3
            final['Final'] = final['KNN']+final['TF-IDF']+final['CV']


            final =final.sort_values(by="Final", ascending=False)
            final1 = final.sort_values(by="Final", ascending=False).copy()
            final_df = df.merge(final1, on='Unnamed: 0')
            final_df = final_df.sort_values(by="Final", ascending=False)
            final_df = final_df.reset_index(drop=True)  # reset the index
            final_df = final_df.head(no_of_cv)
            #st.dataframe(final_df)
            
            
            db_expander = st.expander(label='CV recommendations:')
            with db_expander:        
                no_of_cols=3
                cols=st.columns(no_of_cols)
                for i in range(0, no_of_cv):
                    cols[i%no_of_cols].text(f"CV ID: {final_df['Unnamed: 0'][i]}")
                    cols[i%no_of_cols].text(f"Name: {final_df['name_x'][i]}")
                    cols[i%no_of_cols].text(f"Phone no.: {final_df['mobile_number'][i]}")
                    cols[i%no_of_cols].text(f"Skills: {final_df['skills'][i]}")
                    cols[i%no_of_cols].text(f"Degree: {final_df['degree'][i]}")
                    cols[i%no_of_cols].text(f"No. of Pages Resume: {final_df['no_of_pages'][i]}")
                    cols[i%no_of_cols].text(f"Email: {final_df['email'][i]}")
                    cols[i%no_of_cols].write("<p style='font-size:21px;'> DOWNLOAD RESUME👇🏻 </p>", unsafe_allow_html=True)

                    # T=final_df['file_path'][i] 
                    # pdf_display = f'<embed src="{T}" width="700" height="1000" >' 
                    cvID=final_df.iloc[i]['Unnamed: 0']
                
                    import webbrowser
                    # Display the button
                    button_label = f"{cvID}.pdf"
                    if cols[i%no_of_cols].button(button_label):
                        # Open the Google Drive link in a new tab
                        url = final_df['file_path'][i]
                        webbrowser.open_new_tab(url)
                        
                        # # Embed the PDF in the page
                        # pdf_display = f'<iframe src="{url}" width="100%" height="800px"></iframe>'
                        # st.markdown(pdf_display, unsafe_allow_html=True)

                    cols[i%no_of_cols].text('___________________________________________________')

                
        else:
            st.write("<p style='font-size:15px;'>Please Provide The Job Discription </p>",unsafe_allow_html=True)

# Set sidebar config
st.sidebar.title("About us")
st.sidebar.subheader("By")
st.sidebar.markdown("**Rakshit Khajuria - 19bec109**")
st.sidebar.markdown("**Prikshit Sharma - 19bec062**")
        


if __name__ == '__main__':
        app()