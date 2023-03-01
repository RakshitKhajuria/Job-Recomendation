import streamlit as st

# Set sidebar config
def sidebar():
    st.sidebar.title("About us")
    st.sidebar.subheader("By")
    text_string_variable1="Rakshit Khajuria - 19bec109"
    url_string_variable1="https://www.linkedin.com/in/rakshit-khajuria/"
    link = f'[{text_string_variable1}]({url_string_variable1})'
    st.sidebar.markdown(link, unsafe_allow_html=True)

    text_string_variable2="Prikshit Sharma - 19bec062"
    url_string_variable2="https://www.linkedin.com/in/prikshit7766/"
    link = f'[{text_string_variable2}]({url_string_variable2})'
    st.sidebar.markdown(link, unsafe_allow_html=True) 


