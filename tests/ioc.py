from injector import Module


class FileBackendTest(Module):

    def configure(self, binder):
        from injector import singleton
        from unuo.filebackend import FileBackend
        from unuo.ioc import backend_key, buildsfolder_key, logsfolder_key, \
            logmanager_key, docker_key
        from unuo.config import config
        from unuo.filelogging import FileLoggerManager

        class MockDocker(object):
            """Expose the do_build but just return junk output"""

            def do_build(self, build):
                return (x for x in ['line1', 'line2'])

        binder.bind(
            buildsfolder_key,
            to=config.builds_folder)
        binder.bind(
            logsfolder_key,
            to=config.logs_folder)
        binder.bind(
            backend_key,
            to=FileBackend,
            scope=singleton)
        binder.bind(
            logmanager_key,
            to=FileLoggerManager,
            scope=singleton)
        binder.bind(
            docker_key,
            to=MockDocker,
            scope=singleton)
