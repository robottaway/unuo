"""Code related to Docker operations.

"""
import subprocess
import shutil

from unuo.errors import BuildError
from unuo.filelogging import close_handlers, get_logger


def run_and_log(args, build_log, cwd=None):
    """Run given args as process, log output to given build logger."""
    p = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    for line in p.stdout:
        yield line
    p.wait()
    if p.returncode:
        command = ' '.join(args)
        error_msg = "!! %s, exit code %s" % (command, p.returncode)
        raise BuildError(error_msg)


def get_short_hash(build, build_log):
    """Get the short hash for the HEAD of the git repo."""
    args = ['git', 'rev-parse', '--short', 'HEAD']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=build.location)
    p.wait()
    if p.returncode:
        command = ' '.join(args)
        error_msg = "!! %s, exit code %s" % (command, p.returncode)
        raise BuildError(error_msg)
    return p.stdout.read().strip()


def do_build(build):
    """Takes given build and kicks it off"""
    build_log = get_logger(build)
    try:
        for line in run_and_log(
                ['git', 'clone', build.repo, build.location], build_log):
            yield line

        for line in run_and_log(
                ['docker', 'build', '-t', build.dockertag, '.'], build_log,
                cwd=build.location):
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
