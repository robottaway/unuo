import unittest
import json
import logging

from unuo.factories import default_factory


logger = logging.getLogger('test')
logging.basicConfig(level=logging.INFO)


class UnuoTests(unittest.TestCase):

    def setUp(self):
        app = default_factory()
        self.app = app.test_client()

    def test_profiles(self):
        rv = self.app.get('/profile')
        j = json.loads(rv.data)
        self.assertEquals({u'builds': [u'mynewbuild']}, j)
