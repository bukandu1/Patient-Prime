"""Models and database functions for Patient Ready database"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

###############################################################
#Composing ORM

class Provider(db.Model):
    """Provider model"""
    __tablename__ = "providers"

    provider_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(64), nullable=False)
    lname = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=True)
    phone_number = db.Column(db.String(64), nullable=True)
    speciality_id = db.Column(db.String(64), 
                                db.ForeignKey('specialities.speciality_id'),
                                nullable=True)

class Review(db.Model):
    """Review Model"""
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.String(64), nullable=True)
    rating_text = db.Column(db.String(), nullable=True)
    site_id = db.Column(db.Integer, nullable=True)

class Speciality(db.Model):
    """Speciality model"""
    __tablename__ = "specialities"

    speciality_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=True)

# class Hospital (db.Model): 
#     """Hospital model"""
#     __tablename__ = "hospitals"

#     hospital_id = db.Column()
#     name = db.Column()
#     address = db.Column()
#     city = db.Column()
#     state = db.Column()
#     zipcode = db.Column()
#     phone_number = db.Column()

#     #***Need to review and finalize variables and datatypes from CMS API
#     m_bsi = db.Column()
#     m_blood_clots = db.Column()
#     m_pressure_sores = db.Column()
#     m_cuts_tears = db.Column()
#     m_serious_comp = db.Column()

# class AssociatedHospital(db.Model):
#     """Associated_Hospital association model"""
#     __tablename__ = "associated_hospitals"

#     assoc_hosp_id = db.Column()
#     provider_id = db.Column()
#     hospital_id = db.Column()


class User(db.Model):
    """User model. To be used for implementing user favorites and login"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

class UserFavorite(db.Model):
    """User_Favorite association model"""
    __tablename__ = "user_favorites"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.provider_id'))

###############################################################
#Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    db_name = 'patientready'

    #Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://' + db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

