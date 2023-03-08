import pymongo
import pandas as pd
import json
from dataclasses import dataclass 
import os
import streamlit as st
# st.write("DB username:", st.secrets["db_username"])


# class EnvironmentVariable:
#     mongo_db_url:str = os.getenv("MONGO_DB_URL")

# env_var = EnvironmentVariable()
client = pymongo.MongoClient(st.secrets["MONGO_DB_URL"])
# print ("connection established")

