import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import student
import pandas as pd

dictCHUGI = []

df = pd.read_excel(r"C:\Users\ACER\Downloads\Students_10_with_account.xlsx")  # Sheet mặc định

for _, row in df.iterrows():
    student_data = {
        "id" : row["id"],
        "name": row["name"],
        "gender": row["gender"],
        "dob": row["dob"],
        "parent_account": row["parent_account"],
        "parent_password": row["parent_password"]
    }
    dictCHUGI.append(student_data)

def output(data):
    for st in data:
        print(st['id'])

output(dictCHUGI)