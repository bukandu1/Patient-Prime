import requests
from bs4 import BeautifulSoup 

import sys
sys.path.append(".")
sys.path.append("../server")

from server import app

from seed_hospitals import load_hospitals
from seed_associated_hospitals_and_doctors_specialities import load_associated_hospitals_and_specialities
from model import (Doctor, Review, Hospital, Speciality, AssociatedHospital, User, 
                    UserFavorite, db, connect_to_db)

URL_TEMPLATE = "https://www.ratemds.com/best-doctors/{}/?page="

def load_reviews_and_doctors(starting_page, ending_page, state_abbreviation="md"):
    """ Load reviews and doctors into database. """
   
   # TODO: Review over template
    base_url = URL_TEMPLATE.format(state_abbreviation)
    

    for page in range(starting_page, ending_page + 1): 
        print(f'Printing: {base_url}{page}')
        # ximport pdb; pdb.set_trace()
        # Request information from each page and return doctor profile
        r = requests.get(base_url + str(page))
        c = r.content
        soup = BeautifulSoup(c, 'html.parser')

        # Returns back list of div elements containing each doctor's profile
        all_doctors_profiles = soup.find_all("div", {"class": "search-item doctor-profile"})

        for doctor_profile in all_doctors_profiles:

            # TODO: Update try-except clauses to smaller portions of code
            try:

                # Parse the search link for current doctor
                doctor_url = doctor_profile.find("a", {"class": "search-item-doctor-link"})
                doctor_endpoint = doctor_url.get('href')
                doctor_url = "https://www.ratemds.com" + doctor_endpoint

                # Filter on all attributes containing class="rating comment"
                r = requests.get(doctor_url)
                c = r.content
                soup = BeautifulSoup(c, 'html.parser')
                review_text_body_list = soup.find_all(attrs={"class":"rating-comment-body"})
                review_date_list = soup.find_all(attrs={"class":"link-plain"})
                doctor_name_list = soup.h1.text.split()[1:]

                # Add doctors from list to db transaction and commit
                last_name = doctor_name_list[-1]
                first_name = doctor_name_list[0]
                doctor = Doctor(last_name=last_name, first_name=first_name)
                db.session.add(doctor)
                db.session.commit()

                doctor_id = doctor.doctor_id

                # Add reviews from review list to db transaction with appropriate doctor id
                for index in range(len(review_text_body_list)):
                    # import pdb; pdb.set_trace()
                    # Need to loop through both lists at the same time to ensure 
                    # dates match with reviews
                    review_text_body = review_text_body_list[index].text
                    review_date = review_date_list[index].text
                    review = Review(review_date=review_date, review_text_body=review_text_body, 
                                    doctor_id=doctor_id, review_site_id=1)
                    db.session.add(review)

                # To assist with notifying on progress on transction and committing
                db.session.commit()
                print("Committed up to Doctor ID:", doctor_id)
        
            except:
                print("Continue")



###########################

if __name__ == "__main__":
    connect_to_db(app)
    print("Connected to db")
    db.create_all()
    load_reviews_and_doctors(10,20) #NOTE: When seeding, max pages on site = 3781 
    #load_hospitals("https://data.medicare.gov/resource/ukfj-tt6v.json?state=MD")
    #load_associated_hospitals_and_specialities("https://data.medicare.gov/resource/c8qv-268j.json?st=MD&$limit=30000&$where=hosp_afl_lbn_1%20IS%20NOT%20NULL")
        #"https://data.medicare.gov/resource/c8qv-268j.json?cred=MD&st=MD&$where=hosp_afl_lbn_1%20in(%27UNIVERSITY%20OF%20MARYLAND%20MEDICAL%20CENTER%27,%27UNIVERSITY%20OF%20MARYLAND%20ST%20JOSEPH%20MEDICAL%20CENTER%27,%27SIBLEY%20MEMORIAL%20HOSPITAL%27,%27BON%20SECOURS%20HOSPITAL%27,%27SUBURBAN%20HOSPITAL%27,%27UNITED%20MEDICAL%20CENTER%27,%27HOLY%20CROSS%20HOSPITAL%27,%27ANNE%20ARUNDEL%20MEDICAL%20CENTER%27,%27MERITUS%20MEDICAL%20CENTER%27,%27JOHNS%20HOPKINS%20HOSPITAL,%20THE%27)")
