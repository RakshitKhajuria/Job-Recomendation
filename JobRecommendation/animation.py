import time
import requests

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

# url = requests.get(
#     "https://assets5.lottiefiles.com/private_files/lf30_m075yjya.json%22"


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



