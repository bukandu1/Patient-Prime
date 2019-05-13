import requests
from pprint import pprint
import json

#Request response object with results
#Replace URL with string variable to use with other requests
r = requests.get("https://data.medicare.gov/resource/ukfj-tt6v.json")

#Return content as list of dictionary (see CMS )
#Possibly use JQuery ($.getJSON(URL))
cms_data_json_list = r.json()


print(type(cms_data_json_list))

for item_dict in cms_data_json_list:
    for key, value in item_dict.items():
        print ("key: ", key, "\n\t", value)

    print("___________________")