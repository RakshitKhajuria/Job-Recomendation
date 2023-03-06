# Core Pkgs
import streamlit as st 
from JobRecommendation.side_logo import add_logo
from JobRecommendation.sidebar import sidebar
import altair as alt
import plotly.express as px 
from streamlit_extras.switch_page_button import switch_page

# EDA Pkgs
import pandas as pd 
import numpy as np 
from datetime import datetime
st.set_page_config(layout="centered", page_icon='logo/logo2.png', page_title="HOMEPAGE")


add_logo()
sidebar()


st.markdown("<h1 style='text-align: center; font-family: Verdana, sans-serif; padding: 20px; border: 2px solid #758283; border-radius: 5px;'>Welcome to Talent Hive !</h1>", unsafe_allow_html=True)

st.markdown("<div style='background-color: rgba(255, 0, 0, 0); padding: 10px;'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-family: Verdana, sans-serif; padding: 20px;'>WHAT WE OFFER : </h2>", unsafe_allow_html=True)

s1,s2, s3 = st.columns(3)
with s1:

    candidate = st.button("Job Recomendation")
    if candidate:
        switch_page("i am a candidate")
    st.balloons()

with s2:
        analyzer = st.button("Resume Analyzer")
        if analyzer:
            switch_page("resume analyzer")
        st.balloons()

with s3:
        recruiter = st.button("Candidate Recomendation")
        if recruiter:
            switch_page("i am a recruiter")
        st.balloons()



st.image('logo/TALENTHIVE.png', use_column_width="auto")
st.markdown("</div>", unsafe_allow_html=True)

# Project Description Section
st.markdown("<h2 style='text-align: center; font-family: Verdana, sans-serif; padding: 20px;'>Why Talent Hive ?</h2>", unsafe_allow_html=True)
st.write("<p style='font-size:20px;'>Job seekers and recruiters struggle to find the right match for open job positions, leading to a time-consuming and inefficient recruitment process. TalentHive offers a solution to this problem with its advanced technologies that provide personalized job and candidate recommendations based on qualifications and experience.</p>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-family: Verdana, sans-serif; padding: 20px;'>AIM</h2>", unsafe_allow_html=True)
st.write("<p style='font-size:20px;'>The job search process can be daunting and time-consuming for both job seekers and recruiters. That's where this app comes in!", unsafe_allow_html=True)
st.write("<p style='font-size:20px;'>This app is designed to assist applicants in searching for potential jobs and to help recruiters find talented candidates. The app offers a user-friendly interface that allows applicants to easily browse and search for job opportunities based on their preferences and qualifications. Users can create a profile, upload their resumes, and set up job alerts to receive notifications about new job postings that match their criteria. The app also provides helpful tips and resources for applicants, such as Resume Analyzer and tips to make your Resume even better !! ", unsafe_allow_html=True)

# Set footer config

# # Set footer config
# footer = "<div style='background-color: #758283; padding: 10px; color: white; text-align: center; position: absolute; bottom: 0; width: 100%;'>© 2023 TalentHive</div>"
# st.markdown(footer, unsafe_allow_html=True)


# Create a container for the footer
footer_container = st.container()

# Add content to the footer container
with footer_container:

    st.write("Github @ <a href='https://github.com/Ryzxxl/Job-Recomendation'>Repository</a>", unsafe_allow_html=True)