"""Models and database functions for Patient Ready database"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

###############################################################
#Composing ORM

class Doctor(db.Model):
    """Doctor model"""
    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    doctor_main_address = db.Column(db.String(64), nullable=True)
    speciality_name = db.Column(db.String(64), nullable=True)
    npi_id = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.Integer, nullable=True) #For future analysis of data
        
    #Not all doctors have phone numbers but will keep for possible future
    #phone_number = db.Column(db.String(64), nullable=True) 

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Doctor doctor_id={self.doctor_id} 
                    name=f'{self.first_name} {self.last_name}'
                    speciality={self.speciality_name}>"""



class Review(db.Model):
    """Review Model"""
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    review_date = db.Column(db.String(64), nullable=True)
    review_text_body = db.Column(db.String(), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), 
                            nullable=False)
    review_site_id = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {"review_text_body": self.review_text_body}

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Review={self.review_id} 
                    date={self.review_date} 
                    rating_truc={self.review_text_body[:10]}>"""

class Speciality(db.Model):
    """Speciality model"""
    __tablename__ = "specialities"

    speciality_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=True)

class Hospital (db.Model): 
    """Hospital model"""
    __tablename__ = "hospitals"

    hospital_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64), nullable=True)
    zipcode = db.Column(db.String(11), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)

    #Hospital patient safety measures. Can add to list in future.
    m_surg = db.Column(db.Float(), nullable=True)
    m_surg_natl = db.Column(db.String(64), nullable=True)
    m_bsi = db.Column(db.Float(), nullable=True)
    m_bsi_natl = db.Column(db.String(64), nullable=True)
    m_dvt = db.Column(db.Float(), nullable=True)
    m_dvt_natl = db.Column(db.String(64), nullable=True)
    m_ulcer = db.Column(db.Float(), nullable=True)
    m_ulcer_natl = db.Column(db.String(64), nullable=True)
    m_wound_dehis = db.Column(db.Float(), nullable=True)
    m_wound_dehis_natl = db.Column(db.String(64), nullable=True)
    m_lac = db.Column(db.Float(), nullable=True)
    m_lac_natl = db.Column(db.String(64), nullable=True)

    doctors = db.relationship("Doctor", secondary="associated_hospitals", backref="hospitals")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Hospital={self.hospital_id} name={self.name} bsi={self.m_bsi}> 
                    clots={self.m_dvt} ulcers={self.m_ulcer} tears={self.m_lac} serious={self.m_surg}
                    wound={self.m_wound_dehis}>"""

class AssociatedHospital(db.Model):
    """Associated_Hospital association model"""
    __tablename__ = "associated_hospitals"

    associated_hosp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), 
                    nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'), 
                    nullable=False)

    hospital = db.relationship("Hospital", backref="associated_hospitals")
    doctor = db.relationship("Doctor", backref="associated_hospitals")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Doctor={self.doctor_id} Hospital={self.associated_hosp_id}>"""

class User(db.Model):
    """User model. To be used for implementing user favorites and login"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_token = db.Column(db.Text, nullable=False)
    user_refresh_token = db.Column(db.String(64), nullable=False)
    user_token_uri = db.Column(db.String(64), nullable=True)
    user_email_address = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User={self.user_id}>"""


class UserFavorite(db.Model):
    """User_Favorite association model"""
    __tablename__ = "user_favorites"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User Fav={self.fav_id} {self.doctor_id}>"""

###############################################################
#Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    db_name = 'patientprime'

    #Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # leave in a state of being able to work with the database directly

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")

