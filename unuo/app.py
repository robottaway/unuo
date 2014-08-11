#!/usr/bin/env python

from flask import Flask, jsonify, request

from unuo.filebackend import post_build, run_build, get_build_profile, \
    get_all_profiles
from unuo.errors import ApiError


app = Flask(__name__)


@app.errorhandler(500)
def error_ise(error):
    return '{"status_code":500,"description":"oh noes!"}', 500


@app.errorhandler(404)
@app.errorhandler(400)
@app.errorhandler(405)
@app.errorhandler(ApiError)
def error_json(error):
    return '{"status_code":"%s","description":"%s"}' % (
        error.code, error.description), error.code


@app.route('/build/<name>', methods=['POST'])
def build(name):
    """Run given build."""
    return run_build(name)


@app.route('/profile', methods=['GET'])
def list_build_profiles():
    """Responsible for listing known builds."""
    builds = get_all_profiles()
    return jsonify({"builds": builds})


@app.route('/profile/<name>', methods=['GET', 'POST'])
def build_container(name):
    """Responsible for creating/updating builds and launching them."""
    if request.method == 'POST':
        return post_build(name, request.json)
    return jsonify(**get_build_profile(name))


if __name__ == '__main__':
    app.config.from_object('unuo.config.DefaultConfig')
    app.run()
