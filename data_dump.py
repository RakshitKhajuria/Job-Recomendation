import pymongo
import pandas as pd
import json 
from JobRecommendation.config import client
# Provide the mongodb localhost url to connect python to mongodb.

db = client.test

DATA_FILE_PATH="all_locations.csv"
# Database Name
dataBase = "Job-Recomendation"
# Collection  Name
collection = "all_locations_Data"
if __name__=="__main__":
    df=pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")
    # reseting the index
    df.reset_index(drop=True,inplace=True)
    #Convert dataframe to json so that we can dump these record in mongo db
    json_record = list(json.loads(df.T.to_json()).values())# this is the required format
    #print(json_record[0])

    # insert converted json record to modgoDB
    client[dataBase][collection].insert_many(json_record)