import unittest
from server import app

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class FlaskTests(unittest.TestCase):

    def setUp(TestCase):
        """ Set up test client before each test"""

        self.client = app.test_client()
        #show errors
        app.config['TESTING'] = True

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    def test_homepage(self):
        """Make sure homepage returns correct HTML."""

        # Use the test client to make requests
        result = client.get('/')

        # Compare result.data with assert method
        self.assertIn(b'<head</head>', result.data)

    def test_search_doctor_form(self):
        """Test that /doctor-form route processes form data correctly."""

        result = client.post('/', data={})

        self.assertIn(b'', result.data)


    #Functional Tests
    def test_doctor_retriveal_from_ORM(self):
        """ Test if doctor searched is found in database"""
        pass

def tearDown(self):
    self.testbed.deactivate()

if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()