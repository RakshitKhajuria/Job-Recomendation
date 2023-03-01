import pandas as pd
import os,sys,io,time,datetime
import numpy as np
import base64,random
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from  JobRecommendation.exception import jobException
import streamlit as st

            
@st.cache_data
def pdf_to_base64(file_path:str) -> str:
        try:
    
            encoded_pdf = base64.b64encode(file_path.read()).decode('utf-8')
            return encoded_pdf
        
        except Exception as e:
                raise jobException(e, sys)

@st.cache_data
def pdf_reader(file):
    try:
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        
        for page in PDFPage.get_pages(file,
                                        caching=True,
                                        check_extractable=True):
                page_interpreter.process_page(page)
                print(page)
        text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        return text
    except Exception as e:
            raise jobException(e, sys)
    

@st.cache_data
def generateUniqueFileName():
    try:
        ts = time.time()
        cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        timestamp = str(cur_date+'_'+cur_time)
        return timestamp
    except Exception as e:
            raise jobException(e, sys)
    

@st.cache_data
def show_pdf(encoded_pdf:str):
    try:
        embed_code = f'<embed src="data:application/pdf;base64,{encoded_pdf}" width="700" height="1000" type="application/pdf">'
        return embed_code
    except Exception as e:
        raise jobException(e, sys)
