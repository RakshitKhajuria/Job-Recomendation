# import pymongo
# import pandas as pd
# import json
# from dataclasses import dataclass 
# import os
# import streamlit as st
# st.write("DB username:", st.secrets["db_username"])

# FOR STREMALIT
# # class EnvironmentVariable:
# #     mongo_db_url:str = os.getenv("MONGO_DB_URL")

# # env_var = EnvironmentVariable()
# client = pymongo.MongoClient(st.secrets["MONGO_DB_URL"])
# # print ("connection established")

# FOR LOCALHOST

import pymongo
import pandas as pd
import json
from dataclasses import dataclass 
import os

class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")

env_var = EnvironmentVariable()
client = pymongo.MongoClient(env_var.mongo_db_url)
print ("connection established")
print(env_var.mongo_db_url)

