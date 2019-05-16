from flask import (Flask, session, redirect, render_template, flash, 
                    request, jsonify)

from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db
import os

app = Flask(__name__)

#Set key to use sessions and debug toolbar
app.secret_key = os.environ['FLASK_SESSION_KEY']

#Route for homepage
@app.route('/')
def homepage():
    """ HOMEPAGE placeholder"""

    #***Will need form on homepage template
    return render_template("homepage.html")

@app.route('/search-providers')
def search_providers():

    #Request provider name from homepage form
    provider_name = request.args.get("provider_name")
    print("\n\n\n\n**********************Provider Name:", provider_name)
    return jsonify(provider_name)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")