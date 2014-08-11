import unittest
import json

from unuo.app import app


class UnuoTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_profiles(self):
        rv = self.app.get('/profile')
        j = json.loads(rv.data)
