import unittest
import json
import logging

from mock import patch


logger = logging.getLogger('test')
logging.basicConfig(level=logging.INFO)


class UnuoTests(unittest.TestCase):

    def setUp(self):
        from unuo.config import config
        from unuo.factories import default_factory
        from unuo.ioc import FileBackendTest
        import tempfile
        config.builds_folder = tempfile.mkdtemp()
        logger.info('Created temp build dir %s', config.builds_folder)
        config.logs_folder = tempfile.mkdtemp()
        logger.info('Created temp log dir %s', config.logs_folder)
        app = default_factory(modules=[FileBackendTest])
        self.app = app.test_client()

    def tearDown(self):
        from unuo.config import config
        import shutil
        logger.info('Removing temp build dir %s', config.builds_folder)
        shutil.rmtree(config.builds_folder)
        logger.info('Removing temp log dir %s', config.logs_folder)
        shutil.rmtree(config.logs_folder)

    def test_profiles(self):
        from unuo.filebackend import FileBackend
        # should be no profiles
        rv = self.app.get('/profile')
        j = json.loads(rv.data)
        self.assertEquals({u'builds': []}, j)

        # Make a profile
        rv = self.app.post(
            '/profile/test',
            data=json.dumps(dict(repo='arepo', push=False, dockertag='dtag')),
            content_type='application/json')
        self.assertEquals(200, rv.status_code)
        j = json.loads(rv.data)
        self.assertTrue('repo' in j)
        self.assertTrue('dockertag' in j)
        self.assertTrue('push' in j)

        # Get the profile
        rv = self.app.get('/profile/test')
        self.assertEquals(200, rv.status_code)
        j = json.loads(rv.data)
        self.assertTrue('repo' in j)
        self.assertTrue('dockertag' in j)
        self.assertTrue('push' in j)

        # Run a build (mock out docker commands)
        rv = self.app.post('/build/test')
        self.assertEquals(200, rv.status_code)
        self.assertTrue('line1' in rv.data)
