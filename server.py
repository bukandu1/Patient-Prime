from flask import (Flask, session, redirect, render_template, flash, 
                    request, jsonify)

from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, Doctor, Hospital, Review
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

@app.route('/search-doctors')
def search_doctors():
    """Search doctors in database"""
    fname = request.args.get("fname")
    lname = request.args.get("lname")

    #Query db for doctor 
    #Future implementation to return back suggested doctors
    doctor = Doctor.query.filter(Doctor.fname.ilike(fname)&Doctor.lname.ilike(lname)).first()
    
    if not doctor:
        flash("This doctor is not found in the database. Please try again.")
        return redirect('/')

    doctor_id = doctor.doctor_id

    #***Map function to list all reviews

    # import pdb; pdb.set_trace()
    reviews = Review.query.filter_by(doctor_id=doctor_id).all()
    print(doctor_id,  reviews)
    review_list = list(map(lambda x: x.body_text, reviews))
    print(review_list,"\n\n\n\n\n\n\n\n\n\n")
    print(list(review_list))

    #***Needs to be updated with associated hospitals of doctor after 
    #relationships formed in tables
    associated_hospitals = Hospital.query.get(36)

    print("\n\n\n\n**********************Hospital Name:", associated_hospitals.name, "BSI:",
            associated_hospitals.m_bsi)

    #If full name match, return doctor object
    print("\n\n\n\n**********************Doctor Name:", doctor, doctor_id)
    return render_template('display-doctor-info.html',doctor=doctor, 
                            assoc_hosp=associated_hospitals, reviews=review_list)
        




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")