import requests
from pprint import pprint
import json
import os
import sys
sys.path.append("..")

from server import app
from model import Doctor, Hospital, AssociatedHospital, db, connect_to_db
from sqlalchemy import func

#Replace URL with string variable to use with other requests in the future
#url = "https://data.medicare.gov/resource/ukfj-tt6v.json" + "?$$app_token=" + os.environ['SOCRATA_API_KEY'] + "?state=MD"
#url="https://data.medicare.gov/resource/c8qv-268j.json?cred=MD&st=MD&$limit=20000"

def load_associated_hospitals_and_specialities(url):
    r = requests.get(url)

    #Return list of dicts. Each dict represents a measure at a single doctor
    #TODO: Definitions of med terms

    cms_providers_associated_hospital_list = r.json()
    
    for current_doctor_dict in cms_providers_associated_hospital_list:
        try:
            #current doctor
            last_name = current_doctor_dict['lst_nm'].lower()
            first_name = current_doctor_dict['frst_nm'].lower()

            #if name in db, store speciality and npi id
            doctor = Doctor.query.filter(Doctor.first_name.ilike(first_name)&Doctor.last_name.ilike(last_name)).first()
                #Doctor.query.filter_by(last_name=last_name, fname=fname).first()
            if doctor:
                if doctor.doctor_id:
                    print(f'FOUND! {doctor.last_name}, {doctor.first_name}')
                    #store doctor's speciality and NPI id
                    doctor.npi_id = current_doctor_dict['npi']
                    doctor.speciality_name = current_doctor_dict['pri_spec']
                    doctor.doctor_main_address = current_doctor_dict['adr_ln_1']
                    #doctor.phone_number = current_doctor_dict['phn_numbr'] not all prov have phone num stored
                    doctor.zipcode = current_doctor_dict['zip'][:5]
                    
                    #Check if dictionary has value of affliated hospital. Some doctors are
                    #a part of clinics
                    hospital_check1 = current_doctor_dict.get('hosp_afl_lbn_1', None)#current_doctor_dict['org_lgl_nm'])
                    hospital_check2 = current_doctor_dict.get('hosp_afl_lbn_2', None)
                    #TODO: Implemenet 3rd associated hospital
                    # hospital_check3 = current_doctor_dict.get('hosp_afl_lbn_3', None)
                    print(f'Hospital 1: {hospital_check1}, Hospital 2: {hospital_check2}')
                    
                    #Create associated hospital for doctor and add to 
                    if hospital_check1 != None:
                        check_hospital_in_system(hospital_check1, doctor)

                    #If the doctor has more than one affliation, add to db
                    # import pdb; pdb.set_trace()
                    print(hospital_check2)
                    if hospital_check2 != None:
                        print("Hospital Check 2:", hospital_check2)
                        check_hospital_in_system(hospital_check2, doctor)

                    db.session.commit()
        except:
            print("Skipped Doctor: ", last_name, first_name)

# TODO: Update method with regex to account for all hospitals with issue
def check_hospital_in_system(hospital_name, doctor_object):
    #These hospitals is incorrectly formatted and breaks the code, will manually fix 
    if hospital_name in ["UNIV OF MD REHABILITATION &  ORTHOPAEDIC INSTITUTE"]:
        hospital_name = "UNIV OF MD REHABILITATION & ORTHOPAEDIC INSTITUTE"
    if hospital_name in ["UNIV OF MD REHABILITATION &  ORTHOPAEDIC INSTITUTE"]:
            hospital_name = "UNIV OF MD REHABILITATION & ORTHOPAEDIC INSTITUTE"
    if hospital_name in ["UNIVERSITY OF MD BALTO WASHINGTON  MEDICAL CENTER"]:
        hospital_name = "UNIVERSITY OF MD BALTO WASHINGTON MEDICAL CENTER"
    if hospital_name in ["UNIVERSITY OF MD CHARLES REGIONAL  MEDICAL CENTER"]:
        hospital_name = "UNIVERSITY OF MD CHARLES REGIONAL MEDICAL CENTER"
    if hospital_name in ["DOCTORS'  COMMUNITY HOSPITAL"]:
        hospital_name = "DOCTORS' COMMUNITY HOSPITAL"

    hospital_id = Hospital.query.filter_by(name=hospital_name).first().hospital_id
    doctor_id = doctor_object.doctor_id
    associated_hospital_current_doctor = AssociatedHospital(doctor_id=doctor_id, 
                                        hospital_id=hospital_id)
    db.session.add(associated_hospital_current_doctor)
    db.session.commit()
    print(f'Complete db add for {doctor_object.last_name}, {doctor_object.first_name}')


connect_to_db(app)

