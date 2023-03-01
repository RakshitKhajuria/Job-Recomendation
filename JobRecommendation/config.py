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