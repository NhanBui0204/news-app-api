from django.test import TestCase, SimpleTestCase

# Create your tests here.
class SimpleTest(SimpleTestCase):
    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual.S(response.status_code,200)