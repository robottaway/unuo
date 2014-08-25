"""Blueprint for Docker related functions.

Contains API methods for kicking off a build profile, adding a build profile,
getting a listing of build profiles.
"""
from flask import Blueprint
from flask import jsonify, request
from unuo.errors import ApiError

from unuo.filebackend import post_build, run_build, get_build_profile, \
    get_all_profiles

docker_bp = Blueprint('docker', __name__)


#@docker_bp.errorhandler(500)
#def error_ise(error):
#    return '{"status_code":500,"description":"oh noes!"}', 500
#

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
    return run_build(name)


@docker_bp.route('/profile', methods=['GET'])
def list_build_profiles():
    """Responsible for listing known builds."""
    builds = get_all_profiles()
    return jsonify({"builds": builds})


@docker_bp.route('/profile/<name>', methods=['GET', 'POST'])
def build_container(name):
    """Responsible for creating/updating builds and launching them."""
    if request.method == 'POST':
        return post_build(name, request.json)
    return jsonify(**get_build_profile(name))
