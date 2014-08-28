from injector import Key, singleton

from unuo.config import config
from unuo.filebackend import FileBackend


backend_key = Key('unuo_backend')


def simple_module(binder):
    """Setup app using file backend"""
    binder.bind(
        backend_key,
        to=FileBackend(config.builds_folder),
        scope=singleton)
