import xmltodict
import json


with open("define.xml") as xml_file:
     
    data_dict = xmltodict.parse(xml_file.read())
         
    # generate the object using json.dumps()
    # corresponding to json data
     
    json_data = json.dumps(data_dict)
     
    # Write the json data to output
    # json file
    with open("data.json", "w") as json_file:
        json_file.write(json_data)





