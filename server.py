from flask import (Flask, session, redirect, render_template, flash, 
                    request, jsonify)

from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, Doctor, Hospital, Review, AssociatedHospital
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

    associated_hospitals = [Hospital.query.get(22), Hospital.query.get(2)]
    # TODO: Can use this line of code once associated hospital table fixed (assoc_hosp_id in psql does not match model)
    #associated_hospitals = AssociatedHospital.query.filter_by(doctor_id=doctor_id).all()
    # TODO: When hospital object received, need to check if it is a list (more than one hospital) or one object (only one associated hospital found for the doctor)
    # print("\n\n\n\n**********************Hospital Name:", associated_hospitals.name, "BSI:",associated_hospitals.m_bsi)
    print(jsonify(doctor.first_name, doctor.last_name), "\n\n\n\n\n\n\n\n*********************")
    return jsonify({"first_name":doctor.first_name, "last_name":doctor.last_name, "main_address": doctor.doctor_main_address,
                    "speciality_name": doctor.speciality_name, "npi_id": doctor.npi_id, "zipcode": doctor.zipcode,
                    "doctor_id": doctor.doctor_id, "reviews": review_list})

########################################################DELETE ONCE REACT TEST COMPLETE
@app.route('/reviews')
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

    doctor_id = doctor.doctor_id

    # import pdb; pdb.set_trace()
    
    # TODO: Update query to Doctor.reviews once model relationship updated
    reviews = Review.query.filter_by(doctor_id=doctor_id).all()
    # print(doctor_id, reviews)
    review_list = list(map(lambda x: x.review_text_body, reviews))
    review_dict = {"reviews": review_list}

    return jsonify(review_dict)
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