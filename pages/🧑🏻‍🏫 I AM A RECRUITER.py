import streamlit as st
import pandas as pd
import numpy as np
import base64
import os,sys
import pymongo
from  JobRecommendation.exception import jobException
from JobRecommendation.side_logo import add_logo
from JobRecommendation.sidebar import sidebar
from JobRecommendation import utils ,MongoDB_function
from JobRecommendation import text_preprocessing,distance_calculation


dataBase = "Job-Recomendation"
collection = "Resume_Data"



st.set_page_config(layout="wide", page_icon='logo/logo2.png', page_title="RECRUITER")



add_logo()
sidebar()


   
def app():
    st.title('Candidate Recommendation')
    c1, c2 = st.columns((3,2))
    # number of cv recommend slider------------------display##
    no_of_cv = c2.slider('Number of CV Recommendations:', min_value=0, max_value=6, step=1)
    jd = c1.text_area("PASTE YOUR JOB DESCRIPTION HERE")
        
    if len(jd) >=1:


        NLP_Processed_JD=text_preprocessing.nlp(jd)   # caling (NLP funtion) for text processing

        jd_df=pd.DataFrame()
        jd_df['jd']=[' '.join(NLP_Processed_JD)]

        @st.cache_data
        def get_recommendation(top, df_all, scores):
            try:
                recommendation = pd.DataFrame(columns = ['name', 'degree',"email",'Unnamed: 0','mobile_number','skills','no_of_pages','score'])
                count = 0
                for i in top:
                    
                    
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
            except Exception as e:
                raise jobException(e, sys)



        df = MongoDB_function.get_collection_as_dataframe(dataBase,collection)

        cv_data=[]
        for i in range(len(df["All"])):
            NLP_Processed_cv=text_preprocessing.nlp(df["All"].values[i])
            cv_data.append(NLP_Processed_cv)

        cv_=[]
        for i in cv_data:
            cv_.append([' '.join(i)])

        df["clean_all"]=pd.DataFrame(cv_)



        # TfidfVectorizer  function

        tf = distance_calculation.TFIDF(df['clean_all'],jd_df['jd'])   

        top = sorted(range(len(tf)), key=lambda i: tf[i], reverse=True)[:100]
        list_scores = [tf[i][0][0] for i in top]
        TF=get_recommendation(top,df, list_scores)


        # Count Vectorizer function
        countv = distance_calculation.count_vectorize(df['clean_all'],jd_df['jd'])
        top = sorted(range(len(countv)), key=lambda i: countv[i], reverse=True)[:100]
        list_scores = [countv[i][0][0] for i in top]
        cv=get_recommendation(top, df, list_scores)

        # KNN function
        
        top, index_score = distance_calculation.KNN(df['clean_all'], jd_df['jd'],number_of_neighbors=19)
        knn = get_recommendation(top, df, index_score)

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
                encoded_pdf=final_df['pdf_to_base64'][i]
                cols[i%no_of_cols].markdown(f'<a href="data:application/octet-stream;base64,{encoded_pdf}" download="resume.pdf"><button style="background-color:GreenYellow;">Download Resume</button></a>', unsafe_allow_html=True)
                embed_code = utils.show_pdf(encoded_pdf)
                cvID=final1['Unnamed: 0'][i]
                show_pdf=cols[i%no_of_cols].button(f"{cvID}.pdf")
                if show_pdf:
                    st.markdown(embed_code, unsafe_allow_html=True)
                
                
                            
            
                
                
                cols[i%no_of_cols].text('___________________________________________________')

            
    else:
        st.write("<p style='font-size:15px;'>Please Provide The Job Discription </p>",unsafe_allow_html=True)



if __name__ == '__main__':
        app()