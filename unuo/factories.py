"""Flask factories for running the app and testing it.
"""

from flask import Flask

from unuo.blueprints.docker import docker_bp


def default_factory(config=None):
    app = Flask(__name__)
    app.config.from_object('unuo.config.DefaultConfig')
    app.register_blueprint(docker_bp)
    return app
