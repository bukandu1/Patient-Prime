from flask import (Flask, session, redirect, render_template, flash, 
                    request, jsonify)

from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, Provider, Hospital, Review
import os

app = Flask(__name__)

#Set key to use sessions and debug toolbar
app.secret_key = os.environ['FLASK_SESSION_KEY']

#Route for homepage
@app.route('/')
def homepage():
    """ Homepage"""

    #***Will need form on homepage template
    return render_template("homepage.html")

@app.route('/search-providers')
def search_providers():
    """Search providers in database"""
    fname = request.args.get("fname")
    lname = request.args.get("lname")

    #Query db for provider 
    #Future implementation to return back suggested providers
    provider = Provider.query.filter(Provider.fname.ilike(fname)&Provider.lname.ilike(lname)).first()
    
    provider_id = provider.provider_id

    #***Map function to list all reviews

    # import pdb; pdb.set_trace()
    reviews = Review.query.filter_by(provider_id=provider_id).all()
    print(provider_id,  reviews)
    review_list = map(lambda x: x.body_text, reviews)
    print(review_list,"\n\n\n\n\n\n\n\n\n\n")
    print(list(review_list))

    #***Needs to be updated with associated hospitals of provider after 
    #relationships formed in tables
    associated_hospitals = Hospital.query.get(36)

    print("\n\n\n\n**********************Hospital Name:", associated_hospitals.name, "BSI:",
            associated_hospitals.m_bsi)

    #If full name match, return provider object
    if provider:
        print("\n\n\n\n**********************Provider Name:", provider, provider_id)
        return render_template('display-provider-info.html',provider=provider, 
                                assoc_hosp=associated_hospitals)
        
    else:
        flash("This provider is not found in the database. Please try again.")
        return redirect('/')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")