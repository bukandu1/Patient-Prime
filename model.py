"""Models and database functions for Patient Ready database"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

###############################################################
#Composing ORM

class Provider(db.Model):
    """Provider model"""
    __tablename__ = "providers"

    provider_id = db.Column()
    fname = db.Column()
    lname = db.Column()
    address = db.Column()
    phone_number = db.Column()

class Provider_Speciality(db.Model):
    """Provider-Speciality association model""" #***Not sure what to call these tables
    __tablename__ = "provider-speciality"

    prov_spec_id = db.Column()
    provider_id = db.Column()
    speciality_id = db.Column()

class Speciality(db.Model):
    """Speciality model"""
    __tablename__ = "specialities"

    speciality_id = db.Column()
    name = db.Column()

class Hospital (db.Model): 
    """Hospital model"""
    __tablename__ = "hospitals"

    hospital_id = db.Column()
    name = db.Column()
    address = db.Column()
    city = db.Column()
    state = db.Column()
    zipcode = db.Column()
    phone_number = db.Column()

    #***Need to review and finalize variables and datatypes from CMS API
    m_bsi = db.Column()
    m_blood_clots = db.Column()
    m_pressure_sores = db.Column()
    m_cuts_tears = db.Column()
    m_serious_comp = db.Column()
    m_ed_time_to_ip = db.Column()
    m_readmission = db.Column()
    m_payment = db.Column()

class Associated_Hospital(db.Model):
    """Associated_Hospital association model"""
    __tablename__ = "associated_hospitals"

    assoc_hosp_id = db.Column()
    provider_id = db.Column()
    hospital_id = db.Column()

class User(db.Model):
    """User model"""
    __tablename__ = "users"

    user_id = db.Column()

class User_Favorite(db.Model):
    """User_Favorite association model"""
    __tablename__ = "user_favorites"

    fav_id = db.Column()
    user_id = db.Column()
    provider_id = db.Column()

###############################################################
#Helper functions


def init_app():
    """Initialize the Flask app"""
    app = Flask(__name__)

    db_name = 'patientready'

    #Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://' + db_name
    app.config['SQLALCHEMY_ECHO'] = False #Show SQL execution when True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    print("Connected to DB!")

if __name__ = "__main__":
    #Allow to run interactively
    init_app()

