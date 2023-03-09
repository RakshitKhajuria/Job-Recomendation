import time
import requests

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

# url = requests.get(
#     "https://assets5.lottiefiles.com/private_files/lf30_m075yjya.json")

url_json = dict()

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# st_lottie(url_json,
#           # change the direction of our animation
#           reverse=True,
#           # height and width of animation
#           height=1000,  
#           width=400,
#           # speed of animation
#           speed=1,  
#           # means the animation will run forever like a gif, and not as a still image
#           loop=True,  
#           # quality of elements used in the animation, other values are "low" and "medium"
#           quality='high',
#            # THis is just to uniquely identify the animation
#           key='Car' 
#           )



