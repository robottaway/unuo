#!/usr/bin/env python

import subprocess  
import os.path
import uuid
import sys
import shutil
import logging


builds_folder = '/tmp/unuo'
logs_folder = '/var/log/unuo'


class Build():
    """Represents information about a docker build.

    Will contain the Git repo to clone, and the tag to apply to final build.
    """

    def __init__(self, name, repo, tag='latest'):
        self.name = name
        self.repo = repo
        self.tag = tag
        self.id = str(uuid.uuid4())
        self.location = os.path.join(builds_folder, self.id)


def get_logger(build):
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
    handlers = log.handlers[:]
    for handler in handlers:
        handler.close()
        log.removeHandler(handler)


def run_and_log(args, build_log, cwd='.'):
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    for line in p.stdout:
        line = line.strip()
        print line
        build_log.info(line)
    p.wait()
    if p.returncode:
        command = ' '.join(args)
        sys.stderr.write('!! %s, exit code %s' % (command, p.returncode))
        build_log.info('!! %s, exit code %s', command, p.returncode)
        return


def get_short_hash(build, build_log):
    p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, cwd=build.location)
    p.wait()
    if p.returncode:
        sys.stderr.write('Unable to get short hash for git repo')
        build_log.info('Unable to get short hash for git repo')
        return
    githash = p.stdout.read().strip()
    build_log.info('Git short hash is %s', githash)
    return githash


def do_build(build):
    """Takes given build and kicks it off
    """
    build_log = get_logger(build)
    try:
        run_and_log(['git', 'clone', build.repo, build.location], build_log)
        githash =  get_short_hash(build, build_log)
        build_log.info('Git short hash is %s', githash)
        run_and_log(['docker', 'build', '-t', build.tag, '.'], build_log, cwd=build.location)
        run_and_log(['docker', 'push', build.tag], build_log)
        shutil.rmtree(build.location)
    finally:
        close_handlers(build_log)


if __name__ == '__main__':
    git_repo='https://git.groovie.org/robottaway/kraken-cart-docker.git'
    tag = 'robottaway/krakencart'
    build = Build('krakenjs-cart', git_repo, tag)
    do_build(build)

