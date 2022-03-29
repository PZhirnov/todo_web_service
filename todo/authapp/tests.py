from django.test import TestCase

# Create your tests here.

class TestToken(TestCase):

    def setUp(self):
        self.user = 'django'
        self.password = 'geekbrains'

    def test_get_token(self):

        self.assertFalse(False)

    def test_something_that_will_fail(self):
        self.assertTrue(False)
