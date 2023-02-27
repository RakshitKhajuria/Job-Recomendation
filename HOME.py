# Core Pkgs
import streamlit as st 
import altair as alt
import plotly.express as px 

# EDA Pkgs
import pandas as pd 
import numpy as np 
from datetime import datetime
st.set_page_config(layout="centered", page_icon='logo/logo2.png', page_title="HOMEPAGE")

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://www.linkpicture.com/q/logo_19.png);
                background-repeat: no-repeat;
                padding-top: 100px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "TALENT HIVE";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 40px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()

# Set sidebar config
st.sidebar.title("About us")
st.sidebar.subheader("By")
#st.sidebar.markdown("**Rakshit Khajuria - 19bec109**")
#st.sidebar.markdown("**Prikshit Sharma - 19bec062**")
text_string_variable1="Rakshit Khajuria - 19bec109"
url_string_variable1="https://www.linkedin.com/in/rakshit-khajuria/"
link = f'[{text_string_variable1}]({url_string_variable1})'
st.sidebar.markdown(link, unsafe_allow_html=True)

text_string_variable2="Prikshit Sharma - 19bec062"
url_string_variable2="https://www.linkedin.com/in/prikshit7766/"
link = f'[{text_string_variable2}]({url_string_variable2})'
st.sidebar.markdown(link, unsafe_allow_html=True)
# Set main page config
st.markdown("<h1 style='text-align: center; font-family: Verdana, sans-serif; padding: 20px; border: 2px solid #758283; border-radius: 5px;'>Welcome to Talent Hive !</h1>", unsafe_allow_html=True)

st.markdown("<div style='background-color: rgba(255, 0, 0, 0); padding: 10px;'>", unsafe_allow_html=True)

    
st.image('logo/TALENTHIVE.png', width=705)
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

st.balloons()

# Create a container for the footer
footer_container = st.container()

# Add content to the footer container
with footer_container:

    st.write("Github @ <a href='https://github.com/Ryzxxl/Job-Recomendation'>Repository</a>", unsafe_allow_html=True)
