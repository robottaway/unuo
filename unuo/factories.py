"""Flask factories for running the app and testing it.
"""
import logging

from flask import Flask
from flask_injector import FlaskInjector

from unuo.blueprints.docker import docker_bp
from unuo.ioc import simple_module

logger = logging.getLogger(__name__)


def default_factory(conf_env=None, conf_dict=None, modules=[simple_module]):
    app = Flask(__name__)
    app.config.from_object('unuo.config.DefaultConfig')
    if conf_dict:
        app.config.update(**conf_dict)
    if conf_env:
        app.config.from_envvar(conf_env)
    app.register_blueprint(docker_bp)
    FlaskInjector(app=app, modules=modules)
    return app
