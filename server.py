from flask import (Flask, session, redirect, render_template, flash, 
                    request, jsonify)

from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, Doctor, Hospital, Review
import os

app = Flask(__name__)

#Set key to use sessions and debug toolbar
app.secret_key = os.environ['FLASK_SESSION_KEY']

@app.route("/user-dashboard-copy")
def search_test():
    """Search for providers and render on one page """
    return render_template("user-dashboard.html")

@app.route('/')
def login():
    """Login page for Patient Prime."""
    return render_template("login.html")

#Route for homepage
@app.route('/search-doctors')
def homepage():
    """ Homepage"""

    return render_template("search-doctors.html")

@app.route('/reviews.json')
def search_reviews():
    """Route to send reviews to dashboard"""

    # TODO: Replace with session for doctor and username
    first_name = "david"
    last_name = "maine"

    # TODO: Future implementation to return back suggested doctors
    doctor = Doctor.query.filter(Doctor.first_name.ilike(first_name)&Doctor.last_name.ilike(last_name)).first()
    
    if not doctor:
        flash("This doctor is not found in the database. Please try again.")
        return redirect('/')

    print(jsonify(doctor.first_name, doctor.last_name), "\n\n\n\n\n\n\n\n*********************")
    return jsonify({"fn":doctor.first_name, "ln":doctor.last_name})

    doctor_id = doctor.doctor_id

    # import pdb; pdb.set_trace()
    
    # TODO: Update query to Doctor.reviews once model relationship updated
    reviews = Review.query.filter_by(doctor_id=doctor_id).all()
    # print(doctor_id, reviews)
    review_list = list(map(lambda x: x.review_text_body, reviews))

    return jsonify({"reviews": review_list})

# TODO: Include name in path
@app.route('/user-dashboard')
def search_doctors():
    """Search doctors in database"""
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")

    # TODO: Future implementation to return back suggested doctors
    doctor = Doctor.query.filter(Doctor.first_name.ilike(first_name)&Doctor.last_name.ilike(last_name)).first()
    
    if not doctor:
        flash("This doctor is not found in the database. Please try again.")
        return redirect('/')

    doctor_id = doctor.doctor_id

    # TODO: Map function to list all reviews

    # import pdb; pdb.set_trace()
    reviews = Review.query.filter_by(doctor_id=doctor_id).all()
    print(doctor_id, reviews)
    review_list = list(map(lambda x: x.review_text_body, reviews))
    print(review_list,"\n\n\n\n\n\n\n\n\n\n")
    print(list(review_list))

    # TODO: Needs to be updated with associated hospitals of doctor after 
    #relationships formed in tables
    associated_hospitals = Hospital.query.get(36)

    print("\n\n\n\n**********************Hospital Name:", associated_hospitals.name, "BSI:",
            associated_hospitals.m_bsi)

    #If full name match, return doctor object
    print("\n\n\n\n**********************Doctor Name:", doctor, doctor_id)

    
    return render_template('user-dashboard-mvp.html',doctor=doctor, 
                            assoc_hosp=associated_hospitals, reviews=review_list)
        

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