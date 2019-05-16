import requests
from pprint import pprint
import json
import os

#***Place in function
#Request response object with results
#Replace URL with string variable to use with other requests in the future
#url = "https://data.medicare.gov/resource/ukfj-tt6v.json" + "?$$app_token=" + os.environ['SOCRATA_API_KEY'] + "?state=MD"
url = "https://data.medicare.gov/resource/ukfj-tt6v.json?state=MD"
r = requests.get(url)

#Return content of response. Each dictionary reps a measure at a single
#hospital
cms_list = r.json()
d = cms_list[11] #***update this line for loop

# for index, d in enunerate(cms_list):
hospital_id = d['provider_id']
name = d['hospital_name']
address = d['address']
city = d['city']
state = d['state']
zipcode = d['zip_code']
phone_num = d['phone_number']

#Add measures in according to their measure name
if d['measure_id'] == "PSI_4_SURG_COMP":
    m_surg_comp = d['score']
    m_surg_natl = d['compared_to_national']

elif d['measure_id'] == "PSI_13_POST_SEPSIS":
    m_bsi = d['score']
    m_bsi_natl = d['compared_to_national']

elif d['measure_id'] == "PSI_12_POSTOP_PULMEMB_DVT":
    m_dvt = d['score']
    m_dvt_natl = d['compared_to_national']

elif d['measure_id'] == "PSI_3_ULCER":
    m_ulcer = d['score']
    m_ulcer_natl = d['compared_to_national']

elif d['measure_id'] == "PSI_14_POSTOP_DEHIS":
    m_wound_dehis = d['score']
    m_wound_dehis_natl = d['compared_to_national']

elif d['measure_id'] == "PSI_15_ACC_LAC":
    m_lac = d['score']
    m_lac_natl = d['compared_to_national']

#if not in db, add hospital to db
    #create hospital object
    #db.session.add(hospital)

#else, only add new information (measure to hospital)
    #insert using sqlalchemy value (retrieve obj & updating attribute on obj)
    #add commit to session

# Commit after every 100 records reviewed (hospital_num from future loop)
# if index % 100 == 0: 
#     print(hospital_num)
#     db.session.commit()
