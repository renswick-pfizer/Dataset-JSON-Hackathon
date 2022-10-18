import streamlit as st
import json
import pyreadr 
import xport.v56
import pandas as pd



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
    return new




dic={"sdtm_VS":"IG.VS","sdtm_AE":"IG.AE","sdtm_LB":"IG.LB","sdtm_DM":"IG.DM","adam_VS":"VS","adam_AE":"AE","adsl":"ADSL"}

st.title("Dataset-JSON Reader")

st.info("This Web Application will read a file and returns json or desired files !")
activities = ["Upload JSON", "upload xml","upload R","upload csv","upload sas(xpt)"]
choice = st.sidebar.selectbox("Input File Type", activities)

if choice == 'Upload JSON':
    domain_s=["sdtm_VS","sdtm_AE","sdtm_LB","sdtm_DM","adam_VS","adam_AE","adsl"]
    choice1=st.sidebar.selectbox("select the output file format",["xpt","csv","Rdata","xml"])
    choice2=st.sidebar.selectbox("select the domain",domain_s)
    #st.subheader("please upload your file  ")
    data = st.file_uploader("Upload your file here", type=["json"])
    st.write(data)
    if data is not None:
        df=json_to_df(f"./data/{data.name}",dic[str(choice2)]) 
        st.success("JSON Loaded successfully")
        #pn = int(st.number_input("Enter the page number: "))
        if choice1=="csv":
            # if choice2[0]=="s":
            #     temp=choice2[-2:]
            df.to_csv(choice2 +".csv")          
            with open(choice2 +".csv") as f:
                    st.download_button('DOWNLOAD !', f,file_name= choice2 +".csv")
            st.write('Your json file has been exported successfully !')
            st.write('Download your csvfile !')
        elif choice1=="Rdata":
            rd=pyreadr.write_rds(choice2+".Rds", df)
            with open(choice2 +".Rds") as f:
                    st.download_button('DOWNLOAD !', f,file_name= choice2 +".Rds")
            st.write('Your R file has been exported successfully !')
            st.write('Download your R file !')
        elif choice1=="xml":
            df.to_xml(choice2 +".xml")          
            with open(choice2 +".xml") as f:
                    st.download_button('DOWNLOAD !', f,file_name= choice2 +".xml")
            st.write('Your xml file has been exported successfully !')
            st.write('Download your xml file !')
        elif choice1=="xpt":
            li=df.to_dict('list')
            with open(choice2+".xpt", 'wb') as f:
                xport.from_columns(li, f)
            with open(choice2 +".xml") as f:
                st.download_button('DOWNLOAD !', f,file_name= choice2+".xpt")
            st.write('Your xpt file has been exported successfully !')
            st.write('Download your xpt file !')

elif choice == "upload csv":
    data =st.file_uploader("upload your file here",type=["csv"])
    if data is not None:
        df=pd.read_csv(data)
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
        df=pyreadr.read_r(data.name)
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
        with open (data.name,'r',encoding='utf-8') as f:
            df = xport.to_dataframe(f)
        st.success("csv loaded successfully")
        df1=df.to_json(choice+'_xpt.json',orient='records')
        st.write(df.head())
        st.write(df1)
        st.write('Your json file has been exported successfully !')
        st.write('Download your Jsonfile !')                
        with open(choice+'_xpt.json') as f:
            st.download_button('DOWNLOAD !',f,file_name=choice+'_xpt.json')
