import unittest
import json
import logging
import tempfile
import shutil

from injector import Module


logger = logging.getLogger('test')
logging.basicConfig(level=logging.INFO)


class SimpleModel(Module):

    def configure(self, binder):
        from injector import singleton
        from unuo.filebackend import FileBackend
        from unuo.ioc import backend_key
        from unuo.config import config
        binder.bind(
            backend_key,
            to=FileBackend(config.builds_folder),
            scope=singleton)


class UnuoTests(unittest.TestCase):

    def setUp(self):
        from unuo.config import config
        from unuo.factories import default_factory
        config.builds_folder = tempfile.mkdtemp()
        logger.info('Created temp build dir %s', config.builds_folder)
        config.logs_folder = tempfile.mkdtemp()
        logger.info('Created temp log dir %s', config.logs_folder)
        app = default_factory(modules=[SimpleModel])
        self.app = app.test_client()

    def tearDown(self):
        from unuo.config import config
        logger.info('Removing temp build dir %s', config.builds_folder)
        shutil.rmtree(config.builds_folder)
        logger.info('Removing temp log dir %s', config.logs_folder)
        shutil.rmtree(config.logs_folder)

    def test_profiles(self):
        rv = self.app.get('/profile')
        j = json.loads(rv.data)
        self.assertEquals({u'builds': []}, j)
