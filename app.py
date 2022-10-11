###
#Enter your comment here
###

########## read json #############

########### json to dataframe ######

import json
import pandas as pd



def json_to_df(file,domain):
    with open (file) as f:
        data_h=json.load(f)
    col_list=[]
    for i in range(len(data_h['clinicalData']['itemGroupData'][domain]['items'])):
        col_list.append(data_h['clinicalData']['itemGroupData'][domain]['items'][i]['name'])
        
    d1=data_h['clinicalData']['itemGroupData'][domain]['itemData']
    new=pd.DataFrame(d1,columns=col_list)
    return new

sdtm_vs=json_to_df(r'C:\Users\SENTHD02\OneDrive - Pfizer\Desktop\hackathon\hackathon_vs.json','IG.VS')

#df to xml file 
sdtm_vs.to_xml("convert_vs.xml")   

# df to csv file 
sdtm_vs.to_csv("csv_va.csv")

# df to R dataset 
import pyreadr
pyreadr.write_rds("rds_vs.Rds", sdtm_vs)

#df to xpt
import xport.v56
def df_to_xpt:
    sdtm_vs_=sdtm_vs.drop('ITEMGROUPDATASEQ',axis=1)
    li_dict=sdtm_vs_.to_dict('list')
    #li_dict
    with open('xpt_vs.xpt', 'wb') as f:
        xport.from_columns(li_dict, f)