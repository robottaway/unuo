from injector import Key, singleton, Module

# Keys for IoC lookups and setting deps
backend_key = Key('unuo_backend')
logmanager_key = Key('unuo_logmanager')
docker_key = Key('unuo_docker')
buildsfolder_key = Key('unuo_builds_folder')
logsfolder_key = Key('unuo_logs_folder')


def simple_module(binder):
    """Setup app using file backend"""
    from unuo.config import config
    from unuo.filebackend import FileBackend
    from unuo.filelogging import FileLoggerManager
    from unuo.docker import Docker_1_1_x
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
        to=Docker_1_1_x,
        scope=singleton)


class FileBackendTest(Module):

    def configure(self, binder):
        from injector import singleton
        from unuo.filebackend import FileBackend
        from unuo.ioc import backend_key
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
