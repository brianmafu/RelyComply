from unittest import TestCase
import unittest
from flask import Flask


import requests

url = 'http://127.0.0.1:5000'

class TestIntegrations(TestCase):
  
    def test_all_items_status_code(self):
        response = requests.get('{}/v1/all-items'.format(url))
        assert 200 == response.status_code

    
    def test_404_status_code(self):
        response = requests.get('{}/v1/all-items-exists'.format(url))
        assert 404 == response.status_code


if __name__ == "__main__":
    unittest.main()