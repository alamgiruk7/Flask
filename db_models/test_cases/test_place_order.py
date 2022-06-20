import unittest
from sys import path

path.append('d:\\Task1')
from main import app


class PlaceOrder(unittest.TestCase):
    '''Check whether the order was place correctly or not.'''
    
    post_data = {"ids": "9, 11"}
    
    def test_1_post(self):
            """Check for POST request response"""
            tester = app.test_client(self)
            resp = tester.post('/place_order', json=self.post_data)
            self.assertEqual(resp.status_code, 200)


    def test_2_output_values(self):
        """Check the output values"""
        tester = app.test_client(self)
        resp = tester.post('/place_order', json=self.post_data)
        self.assertTrue(b'id' in resp.data)
        self.assertTrue(b'item_name' in resp.data)
        self.assertTrue(b'item_price' in resp.data)

    def test_3_response_data(self):
        """Check the output values"""
        tester = app.test_client(self)
        resp = tester.post('/place_order', json=self.post_data)
        self.assertTrue(b'id' in resp.data)
        self.assertTrue(b'item_name' in resp.data)
        self.assertTrue(b'item_price' in resp.data)



if __name__ == '__main__':
    unittest.main()