
import requests
from pprint import pprint
import json
import os
import sys
sys.path.append("..")

from server import app
from model import Hospital, db, connect_to_db


#Request response object with results

def load_hospitals(url):
    #Replace URL with string variable to use with other requests in the future
    #url = "https://data.medicare.gov/resource/ukfj-tt6v.json" + "?$$app_token=" + os.environ['SOCRATA_API_KEY'] + "?state=MD"
    r = requests.get(url)

    #import pdb; pdb.set_trace()
    #Return list of dicts. Each dict represents a measure at a single hospital
    cms_list = r.json() 
    for i in range(len(cms_list)):

        d = cms_list[i] #current hospital

        # for index, d in enunerate(cms_list):
        hospital_id = d['provider_id']
        name = d['hospital_name']
        #This hospital is incorrectly formatted in the  API, manually fixing
        if name in ["UNIV OF MD REHABILITATION &  ORTHOPAEDIC INSTITUTE"]:
            name = "UNIV OF MD REHABILITATION & ORTHOPAEDIC INSTITUTE"
        if name in ["UNIVERSITY OF MD BALTO WASHINGTON  MEDICAL CENTER"]:
            name = "UNIVERSITY OF MD BALTO WASHINGTON MEDICAL CENTER"
        if name in ["UNIVERSITY OF MD CHARLES REGIONAL  MEDICAL CENTER"]:
            name = "UNIVERSITY OF MD CHARLES REGIONAL MEDICAL CENTER"
        if name in ["DOCTORS'  COMMUNITY HOSPITAL"]:
            name = "DOCTORS' COMMUNITY HOSPITAL"
        
        address = d['address']
        city = d['city']
        state = d['state']
        zipcode = d['zip_code']
        phone_num = d['phone_number']

        hospital = Hospital.query.filter_by(name=name).first()
        print("This will be either a name or None: ", hospital)

        #add new hospital if hospital not found in db
        if hospital == None:
            hospital = Hospital(name=name, address=address, city=city, 
                                    state=state, zipcode=zipcode,
                                    phone_number=phone_num)
        
        db.session.add(hospital)
        db.session.commit()
        print("Committed hospital: ", hospital)

        hospital = Hospital.query.filter_by(name=name).first()

        try:
            #if score not available, do not to table and continue
            if d['score']=='Not Available':
                pass

            #Add measures in according to their measure name
            elif d['measure_id'] == "PSI_4_SURG_COMP":
                hospital.m_surg = d['score']
                hospital.m_surg_natl = d['compared_to_national']

            elif d['measure_id'] == "PSI_13_POST_SEPSIS":
                hospital.m_bsi = d['score']
                hospital.m_bsi_natl = d['compared_to_national']

            elif d['measure_id'] == "PSI_12_POSTOP_PULMEMB_DVT":
                hospital.m_dvt = d['score']
                hospital.m_dvt_natl = d['compared_to_national']

            elif d['measure_id'] == "PSI_3_ULCER":
                hospital.m_ulcer = d['score']
                hospital.m_ulcer_natl = d['compared_to_national']

            elif d['measure_id'] == "PSI_14_POSTOP_DEHIS":
                hospital.m_wound_dehis = d['score']
                hospital.m_wound_dehis_natl = d['compared_to_national']

            elif d['measure_id'] == "PSI_15_ACC_LAC":
                hospital.m_lac = d['score']
                hospital.m_lac_natl = d['compared_to_national']
        except:
            print(f'Measure id: {measure_id} will not be saved at this time')
###########################

if __name__ == "__main__":
    app = app()
    app.app_context().push()
    connect_to_db(app)
    db.create_all()
    print("Connected to db")

