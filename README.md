# Patient Prime
A web application that assist patients with reviewing objective quality indicators and subjective reviews together and assist with make an informed decision about their future care.

Click here for a video demo: [insert link herehttps://you.be].

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
Top
![homepage_top](/static/screenshot_dashboard_top.png)
Bottom
![homepage_top](/static/screenshot_dashboard_bottom.png)

### Search Doctor
![search-doctor=250x250](/static/Patient_Prime_Search_Doctor.gif)

### Share Current Doctor via Text & Favorite Doctor
![favorites-and-text-recommendation](/static/gifs/Patient_Prime_Fav_Text.gif=250x205)

### Doctor Reviews
![user](/static/gifs/Patient_Prime_Reviews.gif)

### Associated Hospitals Data Visualization & Patient Safety Measure Info
![favorites](/static/gif/Patient_Prime_ChartJS.gif)

# Future TODOs
- Write tests!
- Autocomplete doctor search textbox
- Use of machine learning to recommend doctors based on user's preference
- Additional of more doctor review sites
- Allow for use to review more than 10 reviews (currently limited to saving 10 in the database.)

### Installation

Patient Prime requires Flask to run.

For test environments...
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