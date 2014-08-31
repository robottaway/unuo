from injector import Key, singleton

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
