######################################################################################################
##                           Answered by: Yoni Shieber Date: 20/2/2022                              ##    
##  Question 1:                                                                                     ##
##  1. Read c onf ig . json file located in: /data/python/config.json                               ##  
##  2. make a GET request to the URL under ‘url’ key and add the first 15 characters to a key       ##
##  name ‘content’ in the json file                                                                 ##
##                                                                                                  ##
##  **IMPORTENT: Assuming we have one jason object, Otherwise the program will fail! ***            ##
##                                                                                                  ##
######################################################################################################

import json
import requests

#Make request to input url and Output first 15 characters string from the content
def Get15C(url):
    DataPage = (requests.get(url)).text
    return DataPage[0:15]

with open("/data/python/config.json", "r") as jsonfile:
    data = json.load(jsonfile)
    print("Read successful")
    for key in list(data):
        if key == "url":
#            print ("Sending request to:", key, data[key])
            first15 = Get15C(data[key])
            data.update({"content":first15})             
            
with open("config.json", "w") as outfile:
    json.dump(data, outfile) 


    
    
