# <img src="/static/title_icon_1.jpeg" alt="Patient Prime Logo" width="50" height="50"/>Patient Prime
A web application that assist patients with reviewing objective patient saftey indicators from hosptials and subjective doctor reviews together to make an informed recommendation and decision about their future care.

<!-- Click here for a video demo: [insert link herehttps://you.be]. -->

# Technologies

- Python
- Javascript
- JQuery
- AJAX
- Flask
- SQLAlchemy
- Postgesql
- Jinja2
- Bootstrap
- Flexbox
- BeautifulSoup 4
- Google OAuth 2.0
- Socrata API
- Twilio API

# Features

### Home/Login
![login](/static/screenshot_login.png)

### User's Dashboard
####Top
![homepage-top](/static/screenshot_dashboard_top.png)

####Bottom
![homepage-top](/static/screenshot_dashboard_bottom.png)

### Search for a doctor (currently the search work's for only)
![search-doctor](/static/gifs/Patient_Prime_Search_Doctor.gif)

### Share the current doctor via text & add/remove the doctor from your favorite's list
![favorites-and-text-recommendation](/static/gifs/Patient_Prime_Fav_Text.gif)

### Review the current Doctor's Review from RateMD.com

### Associated Hospitals Data Visualization & Patient Safety Measure Info
![favorites](/static/gifs/Patient_Prime_ChartJS.gif)

# Future TODOs
- Write tests!
- Expand doctor search search (search is )
- Autocomplete doctor search textbox
- Use of machine learning to recommend doctors based on user's preference
- Additional of more doctor review sites
- Allow for use to review more than 10 reviews (currently limited to saving 10 in the database.)

# Installation

Patient Prime requires Flask to run.

**For test environments...**
Obtain appropriate API keys for the following APIs/client:
- Google OAuth client
- Twilio
- Socrata (only needed if large number of requests per day)

Create a secrets.sh file to hold key or use your preferred method.

Install the dependencies, run load the database files, and start server.
```sh
$ cd patientprime
$ pip3 install -r requirements.txt
$ virtualenv env
$ source env/bin/activate
$ source secret.sh
$ python3 database/seed_reviews_and_doctors.py
$ python3 server.py
```

# License

 MIT