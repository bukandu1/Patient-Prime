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
    speciality_name = db.Column(db.String(64), nullable=True)
    npi_id = db.Column(db.Integer, nullable=True)

def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Provider provider_id={self.provider_id} 
                    name=f'{self.fname} {self.lname}'
                    speciality={self.speciality}>"""

class Review(db.Model):
    """Review Model"""
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.String(64), nullable=True)
    body_text = db.Column(db.String(), nullable=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.provider_id'), 
                            nullable=False)
    site_id = db.Column(db.Integer, nullable=True)

def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Review={self.review_id} 
                    date={self.date} 
                    rating_truc={self.rating_text[:10]}>"""

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
    zipcode = db.Column(db.Integer, nullable=True)
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

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Hospital={self.hospital_id} name={self.name} bsi={self.m_bsi}> 
                    clots={self.m_dvt} ulcers={self.m_ulcer} tears={self.m_lac} serious={self.m_surg}
                    wound={self.m_wound_dehis}>"""

class AssociatedHospital(db.Model):
    """Associated_Hospital association model"""
    __tablename__ = "associated_hospitals"

    assoc_hosp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.provider_id'), 
                    nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'), 
                    nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Provider={self.provider_id} Hospital={self.assoc_hosp_id} 
                    name={self.hospital_name}>"""

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

