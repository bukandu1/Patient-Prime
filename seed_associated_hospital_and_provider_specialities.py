import requests
from pprint import pprint
import json
import os
from server import app
from model import Provider, Hospital, AssociatedHospital, db, connect_to_db
from sqlalchemy import func

#Replace URL with string variable to use with other requests in the future
#url = "https://data.medicare.gov/resource/ukfj-tt6v.json" + "?$$app_token=" + os.environ['SOCRATA_API_KEY'] + "?state=MD"
#url="https://data.medicare.gov/resource/c8qv-268j.json?cred=MD&st=MD&$limit=20000"

def load_assoc_hosp_speciality(url):
    r = requests.get(url)

    #Return list of dicts. Each dict represents a measure at a single hospital
    cms_list = r.json()
    
    for i in range(len(cms_list)):

        #import pdb; pdb.set_trace()
        d = cms_list[i] #current provider
        lname = d['lst_nm'].lower()
        fname = d['frst_nm'].lower()

        #if name in db, store speciality and npi id
        provider = Provider.query.filter(Provider.fname.ilike(fname)&Provider.lname.ilike(lname)).first()
        #Provider.query.filter_by(lname=lname, fname=fname).first()
        if provider:
            print(f'FOUND! {provider.lname}, {provider.fname}')
            #store provider's speciality and NPI id
            provider.npi_id = d['npi']
            provider.speciality_name = d['pri_spec']
            provider.address = d['adr_ln_1']
            #provider.phone_number = d['phn_numbr'] not all prov have phone num stored
            provider.zipcode = d['zip'][:5]


            #Check if dictionary has value of affliated hospital. Some providers are
            #a part of clinics
            
            

            hospital_check1 = d.get('hosp_afl_lbn_1','not in system')#d['org_lgl_nm'])
            hospital_check2 = d.get('hosp_afl_lbn_2', 'not in system')
            hospital_check3 = d.get('hosp_afl_lbn_3', 'not in system')
            print(f'Hospital 1: {hospital_check1}, Hospital 2: {hospital_check2}, Hospital 3: {hospital_check3}')

            #This hospital is incorrectly formatted and breaks the code, will manually fix 
            if d['hosp_afl_lbn_1'] == d['hosp_afl_lbn_3'] == d['hosp_afl_lbn_2'] == "UNIV OF MD REHABILITATION &  ORTHOPAEDIC INSTITUTE":
                    d['hosp_afl_lbn_1'] = "UNIV OF MD REHABILITATION & ORTHOPAEDIC INSTITUTE"

            if hospital_check1 != 'not in system':

                #get the hospital id and store into provider's db item
                hospital = Hospital.query.filter_by(name=hospital_check).first()
                
                #Create associated hospital for provider and add to 
                hospital_id = hospital.hospital_id
                provider_id = provider.provider_id
                associated1 = AssociatedHospital(provider_id=provider_id, hospital_id=hospital_id)
                db.session.add(associated1)

                #If the provider has more than one affliation, add to db
                hospital_check = d.get('hosp_afl_lbn_2', 'not in system')
                print('Hospital Check:', hospital_check)
                if hospital_check != 'not in system':
                    hospital = Hospital.query.filter_by(name=hospital).first()
                    hospital_id = hospital.hospital_id
                    provider_id = provider.provider_id
                    associated2 = AssociatedHospital(provider_id=provider_id, hospital_id=hospital_id)
                    db.session.add(associated2)


                hospital_check = d.get('hosp_afl_lbn_3', 'not in system')
                print('Hospital Check:', hospital_check)
                if hospital_check != 'not in system':
                    hospital = Hospital.query.filter_by(name=hospital_check).first()
                    hospital_id = hospital.hospital_id
                    provider_id = provider.provider_id
                    associated3 = AssociatedHospital(provider_id=provider_id, hospital_id=hospital_id)
                    db.session.add(associated3)
            db.session.commit()
            print(f'Complete db add for {lname}, {fname}')

connect_to_db(app)

