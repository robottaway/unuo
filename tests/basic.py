from unittest import TestCase


class TestLogger(TestCase):
    """Test the logger creation per build"""

    def test_get_logger(self):
        from unuo.filelogging import FileLoggerManager
        from unuo.models import Build
        import logging
        import tempfile
        import shutil
        import os

        logs_folder = tempfile.mkdtemp()
        logmanager = FileLoggerManager(logs_folder)
        build = Build('test-build')
        build.id = 'test'
        l = logmanager.get_logger(build)

        # check that folder named test exists in temp folder
        huh = os.path.exists(logs_folder)
        self.assertTrue(huh)

        # check that there is one file handler
        handlers = l.handlers
        self.assertEqual(len(handlers), 1)
        fh = handlers[0]
        self.assertEqual(type(fh), logging.FileHandler)
        shutil.rmtree(logs_folder)

    def test_close_handlers(self):
        from unuo.models import Build
        import tempfile
        from unuo.filelogging import FileLoggerManager
        import shutil

        logs_folder = tempfile.mkdtemp()
        logsmanager = FileLoggerManager(logs_folder)
        build = Build('test-build')
        build.id = 'test'
        l = logsmanager.get_logger(build)
        logsmanager.close_handlers(l)
        shutil.rmtree(logs_folder)

    def test_api_error(self):
        from unuo.errors import ApiError
        error = ApiError('ooops', 200)
        d = error.to_dict()
        self.assertIsNotNone(d)
        j = error.to_json()
        self.assertIsNotNone(j)
