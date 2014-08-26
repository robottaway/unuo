"""Blueprint for Docker related functions.

Contains API methods for kicking off a build profile, adding a build profile,
getting a listing of build profiles.
"""
import logging

from flask import Blueprint
from flask import jsonify, request
from unuo.errors import ApiError

docker_bp = Blueprint('docker', __name__)

logger = logging.getLogger('test')

backend = None


def inject_backend(_backend):
    global backend
    logger.info('Injecting backend %s', _backend)
    backend = _backend

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


@docker_bp.route('/build/<name>', methods=['POST'])
def build(name):
    """Run given build."""
    return backend.run_build(name)


@docker_bp.route('/profile', methods=['GET'])
def list_build_profiles():
    """Responsible for listing known builds."""
    builds = backend.get_all_profiles()
    return jsonify({"builds": builds})


@docker_bp.route('/profile/<name>', methods=['GET', 'POST'])
def build_container(name):
    """Responsible for creating/updating builds and launching them."""
    if request.method == 'POST':
        return backend.post_build(name, request.json)
    return jsonify(**backend.get_build_profile(name))
