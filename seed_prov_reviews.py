import requests
from bs4 import BeautifulSoup 
import re
from model import Provider, Review, Speciality, User, UserFavorite, db, connect_to_db
from server import app


def parse_provider_ratings(start, end):
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

    import pdb; pdb.set_trace()
    #Add reviews from review list to db transaction
    for prov_list in range(len(text_list)):
        for i in range(len(prov_list)):
            review_text = text_list[i].text
            review_date = date_list[i].text
            review = Review(date=review_date, body_text=review_text, 
                            provider_id=prov_id, site_id=1)
            db.session.add(review)

        #To assist with notifying on progress on transction and committing
    db.session.commit()
    print("Committed up to Provider ID:", prov_id)

            #***complete code for storing physician name
            #if len(provider_name_list) = 2, store first and last name
            #else, store first, middle initial, and last name
            #should test to ensure 2 or 3 names being returned


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
    data = parse_provider_ratings(1,1)
    #load_ratings_and_provs(data)
