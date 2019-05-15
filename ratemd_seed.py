import requests
from bs4 import BeautifulSoup 
import re

starting_page = 1
number_of_pages = 1
base_url = "https://www.ratemds.com/best-doctors/?page="
last_rating = ""

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
            print("https://www.ratemds.com/"+a)

            #Obtain physician url for further parsing
            doctor_url = "https://www.ratemds.com/" + a

            #Filter on all attributes containing class="rating comment"
            #***This can be refactored to a function
            r = requests.get(doctor_url)
            c = r.content
            soup = BeautifulSoup(c, 'html.parser')
            ratings_text_list = soup.find_all(attrs={"class":"rating-comment-body"})
            ratings_date_list = soup.find_all(attrs={"class":"link-plain"})
            for rating.text in ratings_list:
                print(rating)
                clean_rating = re.compile(r'(.+)(\\nWas this rating useful\? 0 flag)( \|.+)')
                #Matches the first half of the text r'.+(?=Was this rating useful\? 0 flag)')

            #Remove flag and react link from rating to get clean list


        except:
            pass
            print("Looped stopped due to error.")

###########################

