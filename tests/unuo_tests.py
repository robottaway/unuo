import unittest
import json
import logging
import tempfile
import shutil

from unuo.factories import default_factory


logger = logging.getLogger('test')
logging.basicConfig(level=logging.INFO)


class UnuoTests(unittest.TestCase):

    def setUp(self):
        from unuo.config import config
        self.buildfolder = tempfile.mkdtemp()
        logger.info('Created temp build dir %s', self.buildfolder)
        self.logfolder = tempfile.mkdtemp()
        logger.info('Created temp log dir %s', self.logfolder)

        config.builds_folder = self.buildfolder
        config.logs_folder = self.logfolder

        app = default_factory()
        self.app = app.test_client()

    def tearDown(self):
        logger.info('Removing temp build dir %s', self.buildfolder)
        shutil.rmtree(self.buildfolder)
        logger.info('Removing temp log dir %s', self.logfolder)
        shutil.rmtree(self.logfolder)

    def test_profiles(self):
        rv = self.app.get('/profile')
        j = json.loads(rv.data)
        self.assertEquals({u'builds': []}, j)
