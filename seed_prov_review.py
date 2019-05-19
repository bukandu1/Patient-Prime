import requests
from bs4 import BeautifulSoup 
from server import app
from seed_hospital import load_hospitals
from seed_hosp_spec import load_assoc_hosp_speciality
from model import (Provider, Review, Hospital, Speciality, AssociatedHospital, User, 
                    UserFavorite, db, connect_to_db)


def load_parsed_reviews(start, end):
    starting_page = start
    number_of_pages = end #When seeding, max pages on site = 3781 
    base_url = "https://www.ratemds.com/best-doctors/md/?page="
    last_rating = "" #for interactive testing on the last rating

    for page in range(starting_page,number_of_pages+1):
        print(f'Printing: {base_url}{page}')

        #Request information from each page and return doctor profile
        r = requests.get(base_url + str(page))
        c = r.content
        soup = BeautifulSoup(c, 'html.parser')
        all = soup.find_all("div", {"class": "search-item doctor-profile"})


        for item in all:
            try:
                n = item.find("a", {"class": "search-item-doctor-link"})
                a = n.get('href')
                
                #Obtain physician url for further parsing
                doctor_url = "https://www.ratemds.com" + a
                #print(doctor_url)

                #Filter on all attributes containing class="rating comment"
                #***This can be refactored (function use and chaining to make code clean)
                r = requests.get(doctor_url)
                c = r.content
                soup = BeautifulSoup(c, 'html.parser')
                text_list = soup.find_all(attrs={"class":"rating-comment-body"})
                date_list = soup.find_all(attrs={"class":"link-plain"})
                prov_name_list = soup.h1.text.split()[1:]

                #Return and load tuple of BS4 objects
                load_ratings_and_provs((text_list, date_list, prov_name_list))
                
            except:
                print("Continue")

            
def load_ratings_and_provs(bs4data):
    """Load ratings and providers to db"""
    
    #Unpack data to store into Review and Provider object
    (text_list, date_list, prov_name_list) = bs4data

    #Add providers from list to db transaction and commit
    last_name = prov_name_list[-1]
    first_name = prov_name_list[0]
    provider = Provider(lname=last_name, fname=first_name)
    db.session.add(provider)
    db.session.commit()

    #Query provider's newly assigned id (to assign reviews appropriately)
    prov_id = Provider.query.filter_by(lname=last_name, fname=first_name).first().provider_id
    print(prov_id)

    #import pdb; pdb.set_trace()
    #Add reviews from review list to db transaction

    for i in range(len(text_list)):
        review_text = text_list[i].text
        review_date = date_list[i].text
        review = Review(date=review_date, body_text=review_text, 
                        provider_id=prov_id, site_id=1)
        db.session.add(review)

    #To assist with notifying on progress on transction and committing
    db.session.commit()
    print("Committed up to Provider ID:", prov_id)

    #***Make reviews and dates more readable on screen    
    #Only parse information when called from database/dictionary
    #     prog = re.compile(r'(.+)(\\nWas this rating useful\? 0 flag)( \|.+)',)
    #     #Matches the first half of the text r'.+(?=Was this rating useful\? 0 flag)')
    #     result = prog.match(rating.text)
    #     print(result)
    #last_rating = ratings_text_list.text


###########################

if __name__ == "__main__":
    connect_to_db(app)
    print("Connected to db")
    db.create_all()
    #data = load_parsed_reviews(11,11)
    #load_hospitals("https://data.medicare.gov/resource/ukfj-tt6v.json?state=MD")
    load_assoc_hosp_speciality("https://data.medicare.gov/resource/c8qv-268j.json?st=MD&$limit=30000&$where=hosp_afl_lbn_1%20IS%20NOT%20NULL")
        #"https://data.medicare.gov/resource/c8qv-268j.json?cred=MD&st=MD&$where=hosp_afl_lbn_1%20in(%27UNIVERSITY%20OF%20MARYLAND%20MEDICAL%20CENTER%27,%27UNIVERSITY%20OF%20MARYLAND%20ST%20JOSEPH%20MEDICAL%20CENTER%27,%27SIBLEY%20MEMORIAL%20HOSPITAL%27,%27BON%20SECOURS%20HOSPITAL%27,%27SUBURBAN%20HOSPITAL%27,%27UNITED%20MEDICAL%20CENTER%27,%27HOLY%20CROSS%20HOSPITAL%27,%27ANNE%20ARUNDEL%20MEDICAL%20CENTER%27,%27MERITUS%20MEDICAL%20CENTER%27,%27JOHNS%20HOPKINS%20HOSPITAL,%20THE%27)")
