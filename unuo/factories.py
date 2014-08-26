"""Flask factories for running the app and testing it.
"""
import logging

from flask import Flask

from unuo.blueprints.docker import docker_bp
from unuo.filebackend import FileBackend
from unuo.config import config

logger = logging.getLogger(__name__)


def default_factory(conf_env=None, conf_dict=None):
    from unuo.blueprints.docker import inject_backend
    app = Flask(__name__)
    app.config.from_object('unuo.config.DefaultConfig')
    if conf_dict:
        app.config.update(**conf_dict)
    if conf_env:
        app.config.from_envvar(conf_env)
    inject_backend(FileBackend(config.builds_folder))
    app.register_blueprint(docker_bp)
    return app
