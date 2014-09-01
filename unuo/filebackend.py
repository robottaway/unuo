"""File based backend.

Profiles will be stored on disk.
"""
import os
from os import listdir
import json
import logging

from voluptuous import MultipleInvalid
from flask import Response
from injector import inject

from unuo.models import build_schema, Build
from unuo.errors import ApiError
from unuo.ioc import buildsfolder_key, docker_key

logger = logging.getLogger(__name__)


class FileBackend(object):
    """A file based backend for Unuo objects"""

    @inject(builds_folder=buildsfolder_key, docker=docker_key)
    def __init__(self, builds_folder, docker):
        self.builds_folder = builds_folder
        self.docker = docker

    def post_build(self, name, jdata):
        """Create or update a build."""
        try:
            build_schema(jdata)
        except MultipleInvalid as e:
            raise ApiError('; '.join([str(i) for i in e.errors]))
        build_file = os.path.join(self.builds_folder, name)
        with open(build_file, 'w') as fd:
            json.dump(jdata, fd)
        return jdata

    def get_build_profile(self, name):
        """Return build profile with given name."""
        build_file = os.path.join(self.builds_folder, name)
        if not os.path.exists(build_file):
            raise ApiError("Build profile '%s' not found" % name, code=404)
        with open(build_file, 'r') as fd:
            build_json = json.load(fd)
        return build_json

    def run_build(self, name):
        """Kick off a build.

        Returns a Flask Response generator which allows for streaming console
        output back to browser/agent.
        """
        build_json = self.get_build_profile(name)
        build = Build(name, **build_json)

        def generate():
            for line in self.docker.do_build(build):
                yield line
        return Response(generate(), mimetype='text/plain')

    def get_all_profiles(self):
        """Return back a list of the builds."""
        builds = []
        for phile in listdir(self.builds_folder):
            fp = os.path.join(self.builds_folder, phile)
            if os.path.isfile(fp):
                builds.append(phile)
        return builds
