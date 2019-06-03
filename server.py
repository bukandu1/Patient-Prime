from flask import (Flask, session, redirect, render_template, flash, 
                    request, url_for, jsonify)
# from flask_oauth import OAuth

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import requests

from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, Doctor, Hospital, Review, AssociatedHospital, User
import os

app = Flask(__name__)

#Set key to use sessions and debug toolbar
app.secret_key = os.environ['FLASK_SESSION_KEY']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'

@app.route('/', methods=["GET"])
def display_login():
    """Home page for Patient Prime."""
    return render_template("login.html")

@app.route('/login')
def test_api_request():
    """ Login workflow"""
    if 'credentials' not in session:
        return redirect('authorize')

    # Load credentials from the session. Returns back as a JSON array
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    drive = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Makes request to
    files = drive.files().list().execute()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session['credentials'] = credentials_to_dict(credentials)

    # TODO: Think about if token really needs to be stored. If so, encrypt first!
    user_token = session['credentials']["token"]
    user_refresh_token = session['credentials']["refresh_token"]
    user_token_uri=session['credentials']["token_uri"]
    user_email_address = files['items'][0]['owners'][0]['emailAddress']

    #Add new user to database if not there already
    if 'user_id' not in session:
        user_id = User.query.filter_by(user_email=user_email_address).first().user_id
        if user_id == None:
            flash("You do not have an account. We're creating one for you right now!")
            new_user_created = User(user_token=user_token, 
                                    user_refresh_token=user_refresh_token,
                                    user_token_uri=user_token_uri, 
                                    user_email=user_email_address)
            db.session.add(new_user_created)
            db.session.commit()
        session['user_id'] = user_id
    
   #if email stored in database, continue
    # user_id = User.query.filter_by(user_email=user_email_address).all()[0].user_id
    # if 'user_id' not in session:
    #     session['user_id'] = user_id
    print("\n\n\n\n\n\n\nSession ID: ", session['user_id'], session['user_email_address'])
    
    # TODO: Uncomment this block when server can catch that there is a token already
    # added to the database for the user in session
    # try:
    #     session['user_id'] = User.query.filter_by(user_email_address=user_email_address).one()
    # except:
    #     print("There are either more than one tokens stored or none.")


    session['user_favorite_doctors'] = Doctor.query.get(2).last_name
        #TODO: Add favorite providers to session
        # query user's favorites
        # store to session['user_favorite_doctors']
        # if only one favorite, add to a list
        # if None, store value of None or empty list (login)
        # if more than one, add to session
        # doing this to format how info stored

    session['user_email_address'] = user_email_address

    #Save fullname to display in user's dashboard
    fullname = files['items'][0]['owners'][0]['displayName']

    print(files['items'][0]['owners'][0]['displayName'], 
        "*******************SESSION!!!!!!!!\n\n\n\n\n", "favorites are:", session['user_favorite_doctors'])
    
    return render_template("/user-dashboard.html", fullname=fullname)
    
    #Used for testing the response returned via json
    # return jsonify(**files)

@app.route('/authorize')
def authorize():
    """ Authorizatioib workflow for Patient Prime to receive auth key from 
    Google app on behalf of the user logging in
    """

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # TODO: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    print("Credentials are of type: ", type(credentials))
    session['credentials'] = credentials_to_dict(credentials)

    # #Add new user to database if not there already
    # db.session.add(new_user_created)
    # db.session.commit()

    print(session['credentials'])

    #Update database with credentials
    # TODO: Encrypt credentials prior to adding to database
    return redirect(url_for('test_api_request'))


@app.route('/logout')
def clear_credentials():
    #if credentials are still found in session, delete credentials
  if 'credentials' in session:
    del session['credentials']
    del session['user_id']
    del session['user_favorite_doctors']
  return ('Credentials have been cleared.<br><br> <a href="localhost:5000">')


def credentials_to_dict(credentials):
    """ Response from authorization is sent from the Credentials class. 
    client_id: which you obtain from the API Console
    
    redirect_uri: 
        HTTP endpoint on your server that will receive the response 
    from Google. The value must exactly match one of the authorized redirect 
    URIs for the OAuth 2.0 client, which you configured in the API Console. If 
    this value doesn't match an authorized URI, you will get a 
    'redirect_uri_mismatch' error."""

    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

# TODO: DONT THINK THIS IS NEEDED
# @app.route('/revoke')
# def revoke():
#   if 'credentials' not in session:
#     return ('You need to <a href="/authorize">authorize</a> before ' +
#             'testing the code to revoke credentials.')

#   credentials = google.oauth2.credentials.Credentials(
#     **session['credentials'])

#   revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
#       params={'token': credentials.token},
#       headers = {'content-type': 'application/x-www-form-urlencoded'})

#   #TODO: Add flash message for when revoked and reroute to homepage
#   status_code = getattr(revoke, 'status_code')
#   if status_code == 200:
#     return('Credentials successfully revoked.' + print_index_table())
#   else:
#     return('An error occurred.')

################GOOGLE OAUTH####################







@app.route('/', methods=["POST"])
def process_login():
    """Log into site 
    Find the user's login credentials, look up the user, and store them in the session.
    """

    email = request.form.get('email')

    #Search database for email entered

    return redirect("/user-dashboard")
    
# TODO: Remove this route and test to make sure does not break anything. 
@app.route('/search-doctors')
def homepage():
    """ Homepage"""

    return render_template("search-doctors.html")

@app.route("/user-dashboard/")
def search_test(username):
    """Search for providers and render on one page """

    #Retrieve username from login form
    print(username, "##################USERNAME#############")

    return render_template("/user-dashboard.html", username=username)

@app.route('/search-doctor')
def search_doctor():
    """Route to send reviews to dashboard"""

    # TODO: Replace with session for doctor and username
    first_name = request.args.get("firstName")
    last_name = request.args.get("lastName")

    # TODO: Future implementation to return back suggested doctors
    doctor = Doctor.query.filter(Doctor.first_name.ilike(first_name)&Doctor.last_name.ilike(last_name)).first()
    print(doctor, "********************Doctor***************")
    if doctor == None:
        print("This doctor is not in system!!!!")
        flash("This doctor is not found in the database. Please try again.")
        return redirect('/')

    doctor_id = doctor.doctor_id

    reviews = Review.query.filter_by(doctor_id=doctor_id).all()
    print(doctor_id, reviews)
    review_list = list(map(lambda x: x.review_text_body, reviews))
    print(review_list,"\n\n\n\n\n\n\n\n\n\n")
    print(list(review_list))

    associated_hospitals = [Hospital.query.get(22).hospital_id, Hospital.query.get(2).hospital_id]
    print(associated_hospitals)
    # TODO: Can use this line of code once associated hospital table fixed (assoc_hosp_id in psql does not match model)
    #associated_hospitals = AssociatedHospital.query.filter_by(doctor_id=doctor_id).all()
    # TODO: When hospital object received, need to check if it is a list (more than one hospital) or one object (only one associated hospital found for the doctor)
    # print("\n\n\n\n**********************Hospital Name:", associated_hospitals.name, "BSI:",associated_hospitals.m_bsi)
    print(jsonify(doctor.first_name, doctor.last_name), "\n\n\n\n\n\n\n\n*********************")
    return jsonify({"first_name":doctor.first_name, "last_name":doctor.last_name, "main_address": doctor.doctor_main_address,
                    "speciality_name": doctor.speciality_name, "npi_id": doctor.npi_id, "zipcode": doctor.zipcode,
                    "doctor_id": doctor.doctor_id, "reviews": review_list})

app.route('/display-favorite-doctors')
def display_favorite_doctors():
    print(session['user_favorite_doctors'])
    return 
#TODO: Implement React JS route for reviews in future
# @app.route('/reviews')
# def search_reviews():
#     """Route to send reviews to dashboard"""

#     # TODO: Replace with session for doctor and username
#     first_name = "david"
#     last_name = "maine"

#     # TODO: Future implementation to return back suggested doctors
#     doctor = Doctor.query.filter(Doctor.first_name.ilike(first_name)&Doctor.last_name.ilike(last_name)).first()
    
#     if not doctor:
#         flash("This doctor is not found in the database. Please try again.")
#         return redirect('/')

#     doctor_id = doctor.doctor_id

#     # import pdb; pdb.set_trace()
    
#     # TODO: Update query to Doctor.reviews once model relationship updated
#     reviews = Review.query.filter_by(doctor_id=doctor_id).all()
#     # print(doctor_id, reviews)
#     review_list = list(map(lambda x: x.review_text_body, reviews))
#     review_dict = {"reviews": review_list}

#     return jsonify(review_dict)
########################################################DELETE ONCE REACT TEST COMPLETE

@app.route('/logout')
def logout():
    return redirect('/login')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    # When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    app.run('localhost', 8080, debug=True)




