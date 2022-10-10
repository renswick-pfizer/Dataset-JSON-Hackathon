import pandas as pd
import ast
import json
import pyreadr


def convert_json(df):
    data = df.to_json(orient='records')
    result = json.loads(data)
    return result

#################################################
# sas to pd.df
# data_sas = pd.read_sas(r'./sample/EC.sas7bdat',encoding='utf-8')
# out = convert_json(data_sas)

#################################################
# R to pd.df
# result = pyreadr.read_r(r'./sample/adsl.Rda')
# data_r=result[list(result.keys())[0]]           #r_data.to_json(orient='records')        #, lines=True
# out = convert_json(data_r)

#################################################
# xml to pd.df

#################################################
# xpt to pd.df                                      #convert JSON to xport
# data_xpt = pd.read_sas(r'./sample/ec.xpt', format='xport', encoding='utf-8')
# out = convert_json(data_xpt)

#################################################
# csv to pd.df
# data_csv = pd.read_csv(r'./sample/EC.csv')
# out = convert_json(data_csv)

#################################################
# excel to pd.df
# data_csv = pd.read_excel(r'./sample/EC.csv')
# out = convert_json(data_csv)