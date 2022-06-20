import unittest
from sys import path

path.append('d:\\Task1')
from main import app

class DisplayAllProducts(unittest.TestCase):

    def test_index_response(self):
        # Check for Response
        tester = app.test_client(self)
        response = tester.get('/')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    

    def test_index_type(self):
        # Check for the parsed data content type
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.content_type, "application/json")




if __name__ ==  '__main__':
    unittest.main()