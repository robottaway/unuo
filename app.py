#!/usr/bin/env python

import subprocess  
import os.path
import uuid
import sys
import shutil
import logging
import json
from flask import Flask
from flask import request, Response
from flask import abort, redirect, url_for
from voluptuous import Schema, Required, All, Length, Range
from voluptuous import MultipleInvalid, Invalid, Optional
from werkzeug.exceptions import HTTPException, NotFound, BadRequest


builds_folder = '/tmp/unuo'
logs_folder = '/var/log/unuo'
app_folder = '/var/local/unuo'


build_schema = Schema({
    Required('repo'): All(basestring, Length(min=1, max=1024)),
    Optional('checkout'): All(basestring, Length(min=1, max=256)),
    Required('dockertag'): All(basestring, Length(min=1, max=256)),
    Required('push'): bool
})


class Build():
    """Represents information about a docker build.

    Will contain the Git repo to clone, and the tag to apply to final build.
    """

    def __init__(self, name, repo=None, dockertag='latest', push=False):
        self.name = name
        self.repo = repo
        self.dockertag = dockertag
        self.id = str(uuid.uuid4())
        self.location = os.path.join(builds_folder, self.id)
        self.push = push
        self.githash = None


class BuildError(Exception):
    pass


def get_logger(build):
    """Get a logger for the given build.

    This logger can target a specific file just for this build.
    """
    build_log = logging.getLogger(build.id)
    build_log.setLevel(logging.INFO)
    filename = "%s/%s-%s.log" % (logs_folder, build.name, build.id)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter()
    handler.setFormatter(formatter)
    build_log.addHandler(handler)
    return build_log


def close_handlers(log):
    """Clean up after given logger. 
    
    Should be called on logger when no longer needed.
    """
    handlers = log.handlers[:]
    for handler in handlers:
        handler.close()
        log.removeHandler(handler)


def run_and_log(args, build_log, cwd=None):
    """Run given args as process, log output to given build logger.
    """
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    for line in p.stdout:
        yield line
    p.wait()
    if p.returncode:
        command = ' '.join(args)
        error_msg = "!! %s, exit code %s" % (command, p.returncode)
        raise BuildError(error_msg)


def get_short_hash(build, build_log):
    """Get the short hash for the HEAD of the git repo.
    """
    args = ['git', 'rev-parse', '--short', 'HEAD']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=build.location)
    p.wait()
    if p.returncode:
        command = ' '.join(args)
        error_msg = "!! %s, exit code %s" % (command, p.returncode)
        raise BuildError(error_msg)
    return p.stdout.read().strip()


def do_build(build):
    """Takes given build and kicks it off
    """
    build_log = get_logger(build)
    try:
        for line in run_and_log(['git', 'clone', build.repo, build.location], build_log):
            yield line
        for line in run_and_log(['docker', 'build', '-t', build.dockertag, '.'], build_log, cwd=build.location):
            yield line
        if build.push:
            for line in run_and_log(['docker', 'push', build.tag], build_log):
                yield line
        try:
            shutil.rmtree(build.location)
            yield 'Build folder %s deleted' % build.location
        except:
            yield '!! Unable to remove build folder'
    except BuildError as be:
        yield str(be)
    except OSError as ose:
        yield ose.strerror
    finally:
        close_handlers(build_log)


class ApiError(Exception):
    code = 400

    def __init__(self, description, code=None, payload=None):
        Exception.__init__(self)
        self.description = description
        if status_code is not None:
            self.code = status_code

    def to_dict(self):
        return { 'message': self.description, 'status_code': self.status_code }

    def to_json(self):
        return json.dumps(self.to_dict())


app = Flask(__name__)
app.debug = True


@app.errorhandler(404)
@app.errorhandler(400)
@app.errorhandler(405)
@app.errorhandler(ApiError)
def error_json(error):
    return '{"status_code":"%s","description":"%s"}' % (error.code, error.description), error.code


def post_build(name):
    """Create or update a build
    """
    try:
        build_schema(request.json)
    except MultipleInvalid as e:
        raise ApiError('; '.join([str(i) for i in e.errors]))
    build_file = os.path.join(app_folder, name)
    exists = os.path.exists(build_file)
    with open(build_file, 'w') as fd:
        json.dump(request.json, fd)
    if exists:
        return "build updated!"
    return "build created!"


def get_build(name):
    """Kick off a build
    """
    build_file = os.path.join(app_folder, name)
    if not os.path.exists(build_file):
        raise ApiError("Build '%s' not found" % name, code=404)
    with open(build_file, 'r') as fd:
        build_json = json.load(fd)
    build = Build(name, **build_json)
    def generate():
        for line in do_build(build):
            yield line
    return Response(generate(), mimetype='text/plain')


@app.route('/build/<name>', methods=['GET', 'POST'])
def build_container(name):
    """Responsible for creating/updating builds and launching them
    """
    if request.method == 'POST':
        return post_build(name)
    if request.method == 'GET':
        return get_build(name)
    abort(405)


if __name__ == '__main__':
    app.run()

