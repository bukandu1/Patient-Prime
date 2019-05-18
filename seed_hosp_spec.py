import requests
from pprint import pprint
import json
import os
from server import app
from model import Provider, Hospital, AssociatedHospital, db, connect_to_db

#Replace URL with string variable to use with other requests in the future
#url = "https://data.medicare.gov/resource/ukfj-tt6v.json" + "?$$app_token=" + os.environ['SOCRATA_API_KEY'] + "?state=MD"
def load_assoc_hosp_speciality(url):
    r = requests.get(url)

    #Return list of dicts. Each dict represents a measure at a single hospital
    #import pdb; pdb.set_trace()
    cms_list = r.json()
    for i in range(len(cms_list)):

        d = cms_list[i] #current hospital

        lname = d['lst_nm']
        fname = d['frst_nm']

        #if name in db, store speciality and npi id
        provider = Provider.query.filter_by(lname=lname, fname=fname).first()
        if provider:
            #store provider's speciality and NPI id
            #provider.npi_id = d['npi_id']
            provider.speciality = d['pri_spec']
            provider.address = d['adr_ln_1']
            provider.phone_number = d['phn_numbr']
            
            #get the hospital id and store into provider's db item
            hospital = Hospital.query.filter_by(name=d['hosp_afl_lbn_1'])

            #Create associated hospital for provider and add to db
            associated1 = AssociatedHospital(provider.provider_id, hospital.hospital_id)
            db.add(associated1)

        #If the provider has more than one affliation, add to db
        if d.get('hosp_afl_2',0) != 0:
            hospital = Hospital.query.filter_by(name=d['hosp_afl_2'])
            associated2 = AssociatedHospital(provider.provider_id, hospital.hospital_id)
            db.add(associated2)

        if d.get('hosp_afl_3',0) != 0:
            hospital = Hospital.query.filter_by(name=d['hosp_afl_3'])
            associated3 = AssociatedHospital(provider.provider_id, hospital.hospital_id)
            db.add(associated3)

        db.commit()
        print(f'Complete db transaction for {lname} {fname}')

