from unittest import TestCase
from unuo.app import Build, get_logger, close_handlers
import logging


class TestLogger(TestCase):
    """Test the logger creation per build"""

    def test_get_logger(self):
        build = Build('test-build')
        build.id = 'test'
        l = get_logger(build)
        handlers = l.handlers
        self.assertEqual(len(handlers), 1)
        fh = handlers[0]
        self.assertEqual(type(fh), logging.FileHandler)

    def test_close_handlers(self):
        build = Build('test-build')
        build.id = 'test'
        l = get_logger(build)
        close_handlers(l)
