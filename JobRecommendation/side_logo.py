import streamlit as st
# def add_logo():
#     st.markdown(
#         """
#         <style>
#             [data-testid="stSidebarNav"] {
#                 background-image: url(https://www.linkpicture.com/q/bd7c7615682647e78d2fff0bbb8a3082-removebg-preview.png);
#                 background-repeat: no-repeat;
#                 size: 50px;
#                 padding-top: 120px;
#                 background-position: 20px 20px;
#             }
#             [data-testid="stSidebarNav"]::before {
#                 content: "TALENT HIVE";
#                 margin-left: 20px;
#                 margin-top: 20px;
#                 font-size: 30px;
#                 position: relative;
#                 top: 100px;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

    # background-image: url(https://www.linkpicture.com/q/logo_19.png);
from PIL import Image
import streamlit as st

# You can always call this function where ever you want

def add_logo(logo_path="logo/image.png", width=300, height=100):
 
    """Read and return a resized logo"""
    # logo = Image.open(logo_path)
    # modified_logo = logo.resize((width, height))
    # st.sidebar.image(modified_logo)
    st.markdown(
        """
        <style>
    
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
