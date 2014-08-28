"""Blueprint for Docker related functions.

Contains API methods for kicking off a build profile, adding a build profile,
getting a listing of build profiles.
"""
import logging

from flask import Blueprint, jsonify, request
from flask.views import View
from injector import inject

from unuo.errors import ApiError
from unuo.ioc import backend_key

docker_bp = Blueprint('docker', __name__)

logger = logging.getLogger(__name__)


# @docker_bp.errorhandler(500)
# def error_ise(error):
#     return '{"status_code":500,"description":"oh noes!"}', 500


@docker_bp.errorhandler(404)
@docker_bp.errorhandler(400)
@docker_bp.errorhandler(405)
@docker_bp.errorhandler(ApiError)
def error_json(error):
    return '{"status_code":"%s","description":"%s"}' % (
        error.code, error.description), error.code


class Builder(View):

    @inject(backend=backend_key)
    def __init__(self, backend):
        self.backend = backend

    def dispatch_request(self, name):
        """Run given build."""
        return self.backend.run_build(name)


docker_bp.add_url_rule(
    '/build/<name>', methods=['POST'], view_func=Builder.as_view('build'))


class ProfileList(View):

    @inject(backend=backend_key)
    def __init__(self, backend):
        self.backend = backend

    def dispatch_request(self):
        """Responsible for listing known builds."""
        builds = self.backend.get_all_profiles()
        return jsonify({"builds": builds})


docker_bp.add_url_rule(
    '/profile', methods=['GET'],
    view_func=ProfileList.as_view('list_build_profiles'))


class Profile(View):

    @inject(backend=backend_key)
    def __init__(self, backend):
        self.backend = backend

    def dispatch_request(self, name):
        """Responsible for creating/updating builds and launching them."""
        if request.method == 'POST':
            return self.backend.post_build(name, request.json)
        return jsonify(**self.backend.get_build_profile(name))


docker_bp.add_url_rule(
    '/profile/<name>', methods=['GET', 'POST'],
    view_func=Profile.as_view('get_profile'))
