from unittest import TestCase


class TestLogger(TestCase):
    """Test the logger creation per build"""

    def test_get_logger(self):
        from unuo.filelogging import get_logger
        from unuo.models import Build
        import logging

        build = Build('test-build')
        build.id = 'test'
        l = get_logger(build)
        handlers = l.handlers
        self.assertEqual(len(handlers), 1)
        fh = handlers[0]
        self.assertEqual(type(fh), logging.FileHandler)

    def test_close_handlers(self):
        from unuo.filelogging import get_logger, close_handlers
        from unuo.models import Build

        build = Build('test-build')
        build.id = 'test'
        l = get_logger(build)
        close_handlers(l)
