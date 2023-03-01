from JobRecommendation.config import client
import pandas as pd
from  JobRecommendation.exception import jobException
import sys
import os,io,time,datetime

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        
        df = pd.DataFrame(list(client[database_name][collection_name].find()))
        
        if "_id" in df.columns:
            
            df = df.drop("_id",axis=1)
        
        return df
    except Exception as e:
        raise jobException(e, sys)



def resume_store(data,dataBase:str,collection:str): 
            try:
                client[dataBase][collection].insert_one(data)
            except Exception as e:
                raise jobException(e, sys)