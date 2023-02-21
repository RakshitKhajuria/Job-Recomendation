import os
import pandas as pd
import requests
import pdfplumber

invoice_pdf = 'rakshit_khajuria_resume.pdf'

with pdfplumber.open(invoice_pdf) as pdf:
     text=""
     pages = pdf.pages
     for page in pages:
         text += page.extract_text(x_tolerance=2)
         print(text)