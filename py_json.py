import streamlit as st
import json
import pyreadr 
import xport.v56
import pandas as pd
import numpy as np
import xmltodict


def json_to_df(file,domain):
    with open (file,'r',encoding='utf-8') as f:
        data_h=json.load(f)
    # f=file.read()
    # data_h=json.load(f)
    col_list=[]
    for i in range(len(data_h['clinicalData']['itemGroupData'][domain]['items'])):
        col_list.append(data_h['clinicalData']['itemGroupData'][domain]['items'][i]['name'])
        
    d1=data_h['clinicalData']['itemGroupData'][domain]['itemData']
    new=pd.DataFrame(d1,columns=col_list)
    new.drop("ITEMGROUPDATASEQ",axis=1,inplace=True)
    new.replace(np.nan,"",inplace=True)
    return new



sdtm_li=["AE","CM","DD","DI","DM","DS","EC","EX","FA","FT","IE","LB","MH","OE","QSPH","QSSL","RELREC","RS","DE","SUPPDM","SUPPEC","SV","TA","TE","TI","TS","TV","VS"]
adam_li=["ADAE","ADLBC","ADLBH","ADLBHY","ADQSADAS","ADQSCIBC","ADQSNPIX","ADSL","ADTTE","ADVS","ADCM","ADDD","ADDI","ADDM","ADDS","ADEC","ADEX","ADFA","ADFT","ADIE","ADLB","ADMH","ADOE","ADRS","ADDE","ADSV","ADTA","ADTE","ADTI","ADTS","ADTV"]
# dic={"Sdtm VS":"IG.VS","Sdtm AE":"IG.AE","Sdtm LB":"IG.LB","Sdtm DM":"IG.DM","Adam VS":"ADVS","Adam AE":"ADAE","ADSL":"ADSL","supp dm":"SUPPDM"}

st.title("Dataset-JSON Reader")
st.sidebar.header("Dataset-JSON Reader")
st.info("This Web Application will read a file and returns json or desired files !")
activities = ["Upload JSON", "upload xml","upload R","upload csv","upload sas(xpt)"]
choice = st.sidebar.selectbox("Input File Type", activities)

if choice == 'Upload JSON':
    domain_s=["SDTM","ADaM"]
    choice1=st.sidebar.selectbox("select the output file format",["xpt","csv","Rdata","xml"])
    choice2=st.sidebar.selectbox("select the standards",domain_s)
    if choice2=="SDTM":
        choice3=st.sidebar.selectbox("select the domain ",sdtm_li)
        choice3="IG."+choice3
    elif choice2=="ADaM":
        choice3=st.sidebar.selectbox("select the domain",adam_li)
    data = st.file_uploader("Upload your file here", type=["json"])

    if data is not None:
        df=json_to_df(f"./data/{data.name}",str(choice3)) 
        st.success("JSON Loaded successfully")

        if choice1=="csv":]
            df.to_csv(choice3 +".csv") 
            st.write(df.head())         
            with open(choice3 +".csv",encoding='cp437') as f:
                    st.download_button('DOWNLOAD !', f,file_name= choice3 +".csv")
            st.write('Your csv file has been exported successfully !')
            st.write('Download your csvfile !')
        elif choice1=="Rdata":
            rd=pyreadr.write_rds(choice3+".Rds", df)
            st.write(df.head())
            with open(choice3 +".Rds",encoding='cp437') as f:
                    st.download_button('DOWNLOAD !', f,file_name= choice3 +".Rds")
            st.write('Your R file has been exported successfully !')
            st.write('Download your R file !')
        elif choice1=="xml":
            df.to_xml(choice3 +".xml")     
            st.write(df.head())     
            with open(choice3 +".xml",encoding='cp437') as f:
                    st.download_button('DOWNLOAD !', f,file_name= choice3 +".xml")
            st.write('Your xml file has been exported successfully !')
            st.write('Download your xml file !')
        elif choice1=="xpt":
            li=df.to_dict('list')
            with open(choice3+".xpt", 'wb') as f:
                xport.from_columns(li, f)
            st.write(df.head())
            with open(choice3 +".xpt",encoding='cp437') as f:
                st.download_button('DOWNLOAD !', f,file_name= choice3 +".xpt")
            st.write('Your xpt file has been exported successfully !')
            st.write('Download your xpt file !')

elif choice == "upload csv":
    data =st.file_uploader("upload your file here",type=["csv"])
    if data is not None:
        df=pd.read_csv(f"./data/{data.name}")
        st.success("csv loaded successfully")
        df1=df.to_json(choice+'_csv.json',orient='records')
        st.write(df.head())
        st.write(df1)
        st.write('Your json file has been exported successfully !')
        st.write('Download your Jsonfile !')                
        with open(choice+'_csv.json') as f:
            st.download_button('DOWNLOAD !',f,file_name=choice+'_csv.json')


elif choice == "upload R":
    data =st.file_uploader("upload your file here",type=["Rda","Rds"])
    if data is not None:
        st.write(str(data))
        st.write(str(data.name))
        st.write(type(data))
        # with open(data.name,'r',encoding='utf-8') as f:
        df=pyreadr.read_r(f"./data/{data.name}")
        df=df[list(df.keys())[0]]
        st.success("R file loaded successfully")
        df1=df.to_json(choice+'_R.json',orient='records')
        st.write(df.head())
        st.write(df1)
        st.write('Your json file has been exported successfully !')
        st.write('Download your Jsonfile !')                
        with open(choice+'_R.json') as f:
            st.download_button('DOWNLOAD !',f,file_name=choice+'_R.json')


elif choice == "upload sas(xpt)":
    data =st.file_uploader("upload your file here",type=["xpt"])
    if data is not None:
        with open(f"./data/{data.name}",'rb') as f:
            df = xport.to_dataframe(f)
        st.success("xpt file loaded successfully")
        df1=df.to_json(choice+'_xpt.json',orient='records')
        st.write(df.head())
        st.write(df1)
        st.write('Your json file has been exported successfully !')
        st.write('Download your Jsonfile !')                
        with open(choice+'_xpt.json') as f:
            st.download_button('DOWNLOAD !',f,file_name=choice+'_xpt.json')

elif choice=="upload xml":
    data=st.file_uploader("upload your file here",type=["xml"])
    if data is not None:
        with open(f"./data/{data.name}") as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
        st.success("xml file loaded successfully")
        json_data = json.dumps(data_dict)
        with open(choice+"_xml.json", "w") as json_file:
            json_file.write(json_data)
        with open (choice+"_xml.json",'r') as f:
            st.download_button('DOWNLOAD !',f,file_name=choice+'_xml.json')
        
        