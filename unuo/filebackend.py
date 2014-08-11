"""File based backend.

Profiles will be stored on disk.
"""
import os
from os import listdir
from voluptuous import MultipleInvalid
import json

from flask import Response

from unuo.models import build_schema, Build
from unuo.errors import ApiError
from unuo.docker import do_build
from unuo.config import config


def post_build(name, json):
    """Create or update a build."""
    try:
        build_schema(json)
    except MultipleInvalid as e:
        raise ApiError('; '.join([str(i) for i in e.errors]))
    build_file = os.path.join(config.builds_folder, name)
    exists = os.path.exists(build_file)
    with open(build_file, 'w') as fd:
        json.dump(json, fd)
    if exists:
        return "build updated!"
    return "build created!"


def get_build_profile(name):
    """Return build profile with given name."""
    build_file = os.path.join(config.builds_folder, name)
    if not os.path.exists(build_file):
        raise ApiError("Build profile '%s' not found" % name, code=404)
    with open(build_file, 'r') as fd:
        build_json = json.load(fd)
    return build_json


def run_build(name):
    """Kick off a build."""
    build_json = get_build_profile(name)
    build = Build(name, **build_json)

    def generate():
        for line in do_build(build):
            yield line
    return Response(generate(), mimetype='text/plain')


def get_all_profiles():
    builds = []
    print config.builds_folder
    for phile in listdir(config.builds_folder):
        print phile
        fp = os.path.join(config.builds_folder, phile)
        if not os.path.isfile(fp):
            continue
        builds.append(phile)
    return builds
