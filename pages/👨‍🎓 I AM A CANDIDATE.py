import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd 
import re
import plotly.express as px
import time,datetime
import base64,random
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import folium_static
import folium
from geopy.extra.rate_limiter import RateLimiter
from pyresparser import ResumeParser
import os,sys
import pymongo
from JobRecommendation.animation import load_lottieurl
from streamlit_lottie import st_lottie, st_lottie_spinner
from JobRecommendation.side_logo import add_logo
from JobRecommendation.sidebar import sidebar
from JobRecommendation import utils , MongoDB_function
from JobRecommendation import text_preprocessing ,distance_calculation
from  JobRecommendation.exception import jobException


dataBase="Job-Recomendation"
collection1="preprocessed_jobs_Data"
collection2 = "Resume_from_CANDIDATE"
collection3 = "all_locations_Data"

st.set_page_config(layout="wide", page_icon='logo/logo2.png', page_title="CANDIDATE")

url = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_cDUGLTDdfh.json")
add_logo()
sidebar()


st.set_option('deprecation.showPyplotGlobalUse', False)
# set wide layout

def app():
    # Title & select boxes
    st.title('Job Recommendation')
    # cv=st.file_uploader('Upload your CV', type='pdf')
    c1, c2 = st.columns((3,2))
    # upload cv + turn pdf to text------------------display##
    cv=c1.file_uploader('Upload your CV', type='pdf')
    # career level
    job_loc = MongoDB_function.get_collection_as_dataframe(dataBase,collection3)
    all_locations=list(job_loc["location"].dropna().unique())

    RL = c2.multiselect('Filter', all_locations )
    #print(RL[0])
   
 
    # number of job recommend slider------------------display##
    no_of_jobs = st.slider('Number of Job Recommendations:', min_value=10, max_value=100, step=10)

    if cv is not None:
        if st.button('Proceed Further !! '):
            with st_lottie_spinner(url, key="download",    reverse=True,speed=1,loop=True,quality='high',):
                time.sleep(20)
                try:
                    count_=0
                    cv_text = utils.extract_data(cv) # (OCR function)
                        # print(cv_text)
                    encoded_pdf=utils.pdf_to_base64(cv)
                    resume_data = ResumeParser(cv).get_extracted_data()
                    resume_data["pdf_to_base64"]=encoded_pdf

                    # inserting data into mongodb           
                    timestamp = utils.generateUniqueFileName()
                    save={timestamp:resume_data}
                    if count_==0:
                        count_=1
                        MongoDB_function.resume_store(save,dataBase,collection2)

                    #----------------------------workings---------------------#

                    # (NLP funtion)

                    try:
                        NLP_Processed_CV=text_preprocessing.nlp(cv_text)   # caling (NLP funtion) for text processing
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
                    df= MongoDB_function.get_collection_as_dataframe(dataBase,collection1)
            
                
                    # recommendation function
                    @st.cache_data
                    def get_recommendation(top, df_all, scores):
                        try:

                            recommendation = pd.DataFrame(columns = ['positionName', 'company',"location",'JobID','description','score'])
                            count = 0
                            for i in top:
                                recommendation.at[count, 'positionName'] = df['positionName'][i]
                                recommendation.at[count, 'company'] = df['company'][i]
                                recommendation.at[count, 'location'] = df['location'][i]
                            
                                recommendation.at[count, 'JobID'] = df.index[i]
                                recommendation.at[count, 'description'] = df['description'][i]
                                recommendation.at[count, 'score'] =  scores[count]
                                count += 1
                            return recommendation
                        except Exception as e:
                            raise jobException(e, sys)


                    # TfidfVectorizer  function
                    output2 = distance_calculation.TFIDF(df['All'], df2['All'])
                    
                    # show top job recommendations using TF-IDF
                    top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:1000]
                    list_scores = [output2[i][0][0] for i in top]
                    TF=get_recommendation(top,df, list_scores)


                    # Count Vectorizer function
                    output3 = distance_calculation.count_vectorize(df['All'], df2['All'])
                
                    # show top job recommendations using Count Vectorizer
                    top = sorted(range(len(output3)), key=lambda i: output3[i], reverse=True)[:1000]
                    list_scores = [output3[i][0][0] for i in top]
                    cv=get_recommendation(top, df, list_scores)

                    # KNN function
                    top, index_score = distance_calculation.KNN(df['All'], df2['All'],number_of_neighbors=100)
                    knn = get_recommendation(top, df, index_score)
                    # Combine 3 methods into a dataframe
                    merge1 = knn[['JobID','positionName', 'score']].merge(TF[['JobID','score']], on= "JobID")
                    final = merge1.merge(cv[['JobID','score']], on = "JobID")
                    final = final.rename(columns={"score_x": "KNN", "score_y": "TF-IDF","score": "CV"})
                    # final.head()

                    
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
                    

                    final2 = final.sort_values(by="Final", ascending=False).copy()
                    final_df = df.merge(final2, on="JobID" )
                    final_df = final_df.sort_values(by="Final", ascending=False)
                    final_df.fillna('Not Available', inplace=True)

                    result_jd = final_df
                    if len(RL)==0:
                        result_jd = final_df    
                    else:

                        result_jd=result_jd[result_jd["location"].isin(list(RL))]

                    final_jobrecomm =result_jd.head(no_of_jobs)


            #<<<<<<<<<<<<<<<<<<VISUALIZATION>>>>>>>>>>>>>>>>>>>>>>>

                    df3 = final_jobrecomm.copy()
                    rec_loc = df3.location.value_counts()
                    locations_df = pd.DataFrame(rec_loc)
                    locations_df.reset_index(inplace=True)

                    locations_df['index'] = locations_df['index'].apply(lambda x: x.replace("Area", "") if "Area" in x else x)

                    #Adding request limit as 1 to follow guidelines
                    locator = Nominatim(user_agent="myGeocoder")
                    geocode = RateLimiter(locator.geocode, min_delay_seconds=1) #1 second per api request

                    #Extracting lat, long, alt
                    locations_df['loc_geo'] = locations_df['index'].apply(geocode)
                    locations_df['point'] = locations_df['loc_geo'].apply(lambda loc: tuple(loc.point) if loc else None)

                    # split point column into latitude, longitude and altitude columns
                    locations_df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(locations_df['point'].tolist(), index=locations_df.index)

                    #dropping any null values from lat / long
                    locations_df.dropna(subset=['latitude'], inplace=True)
                    locations_df.dropna(subset=['longitude'], inplace=True)

                    #Set start location for map
                    folium_map = folium.Map(location=[12.9767936, 77.590082],
                                            zoom_start=11,
                                            tiles= "openstreetmap",)
                    
                    #Adding points to map
                    for lat, lon, ind, job_no in zip(locations_df['latitude'], locations_df['longitude'], locations_df['index'], locations_df['location']):
                        label = folium.Popup("Area: " + ind + "<br> Number of Jobs: " + str(job_no), max_width=500)
                        folium.CircleMarker(
                            [lat, lon],
                            radius=10,
                            popup=label,
                            fill = True,
                            color='red',
                            fill_col = "lightblue",
                            icon_size = (150,150),
                            ).add_to(folium_map)

                    # qualification bar chart
                    db_expander = st.expander(label='CV dashboard:')
                    with db_expander:
                        available_locations = df3.location.value_counts().sum()
                        all_locations = df3.location.value_counts().sum() + df3.location.isnull().sum()
                
                        st.write(" **JOB LOCATIONS FROM**", available_locations, "**OF**", all_locations, "**JOBS**")

                        folium_static(folium_map, width=1380)

                        chart2, chart3,chart1 = st.columns(3)

                        with chart3:
                            st.write("<p style='font-size:17px;font-family: Verdana, sans-serif'> RATINGS W.R.T Company</p>", unsafe_allow_html=True)

                            rating_count = final_jobrecomm[["rating","company"]]
                            fig = px.pie(rating_count, values = "rating", names = "company", width=600)
                            fig.update_layout(showlegend=True)
                            st.plotly_chart(fig, use_container_width=True,)

                        with chart2:
                            st.write("<p style='font-size:17px;font-family: Verdana, sans-serif'> REVIEWS COUNT W.R.T Company</p>", unsafe_allow_html=True)
                            review_count = final_jobrecomm[["reviewsCount","company"]]
                            fig = px.pie(review_count, values = "reviewsCount", names = "company", width=600)
                            fig.update_layout(showlegend=True)
                            st.plotly_chart(fig, use_container_width=True,)

                        with chart1:


                            final_salary = final_jobrecomm.copy()

                    
                            col=final_salary["salary"].dropna().to_list()
                            y,m=utils.get_monthly_yearly_salary(col) #get_monthly_yearly_salary
                            yearly_salary_range=utils.salary_converter(y) #salary_converter (get salary from str)
                            monthly_salary_to_yearly=utils.salary_converter(m) # salary_converter (get salary from str)
                            final_salary=yearly_salary_range+monthly_salary_to_yearly
                            salary_df=pd.DataFrame(final_salary,columns=['Salary Range'])
                            sal_count = salary_df['Salary Range'].count() 

                            
                            st.write(" **SALARY RANGE FROM** ", sal_count, "**SALARY VALUES PROVIDED**")
                            fig2 = px.box(salary_df, y= "Salary Range", width=500,title="Salary Range For The Given Job Profile")
                            fig2.update_yaxes(showticklabels=True,title="Salary Range in Rupees" )
                            fig2.update_xaxes(visible=True, showticklabels=True)
                            st.write(fig2)
                                        
                    # expander for jobs df ---------------------------display#
                    db_expander = st.expander(label='Job Recommendations:')

                    final_jobrecomm = final_jobrecomm.replace(np.nan, "Not Provided")
                    @st.cache_data
                    def make_clickable(link):
                        # target _blank to open new window
                        # extract clickable text to display for your link
                        text = 'more details'
                        return f'<a target="_blank" href="{link}">{text}</a>'

                    with db_expander:
                        def convert_df(df):
                            try:
                                return df.to_csv(index=False).encode('utf-8')
                            except Exception as e:
                                raise jobException(e, sys)
                        final_jobrecomm['externalApplyLink'] = final_jobrecomm['externalApplyLink'].apply(make_clickable)
                        final_jobrecomm['url'] = final_jobrecomm['url'].apply(make_clickable)
                        # final_jobrecomm['salary'].replace({"0":"Not Available"}, inplace=True)
                        final_df=final_jobrecomm[['company','positionName_x','description','location','salary', 'rating', 'reviewsCount', "externalApplyLink", 'url']]
                        final_df.rename({'company': 'Company', 'positionName_x': 'Position Name', 'description' : 'Job Description', 'location' : 'Location', 'salary' : 'Salary', 'rating' : 'Company Rating', 'reviewsCount' : 'Company ReviewCount', 'externalApplyLink': 'Web Apply Link', 'url': 'Indeed Apply Link' }, axis=1, inplace=True)
                        show_df = final_df.to_html(escape=False)
                        st.write(show_df, unsafe_allow_html=True)    

                    csv=convert_df(final_df)
                    st.download_button("Press to Download",csv,"file.csv","text/csv",key='download-csv')           
                    st.balloons()
                except Exception as e:
                    raise jobException(e, sys)

if __name__ == '__main__':
        app()