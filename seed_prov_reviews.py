import requests
from bs4 import BeautifulSoup 
import re
from model import Provider, Review

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
                print(doctor_url)

                #Filter on all attributes containing class="rating comment"
                #***This can be refactored (function use and chaining to make code clean)
                r = requests.get(doctor_url)
                c = r.content
                soup = BeautifulSoup(c, 'html.parser')
                # import pdb; pdb.set_trace()
                text_list = soup.find_all(attrs={"class":"rating-comment-body"})
                date_list = soup.find_all(attrs={"class":"link-plain"})
                prov_name_list = soup.h1.text.split()[1:]
            except:
                print("Continue")

    #Returns tuple of BS4 objects
    return [text_list, date_list, prov_name_list]
            
def load_ratings_and_provs(bs4data):
    """Load ratings and providers to db"""
    
    #Unpack tuple 
    t[0], t[1], t[2] = bs4data.split()

    print(ratings_text_list.text)
    print("complete for ", a)

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
    db.create_all()

    data = parse_provider_ratings(1,1)
    #load_ratings_and_provs(data)
