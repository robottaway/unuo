"""Code related to Docker operations.

"""
import subprocess
import shutil

from injector import inject

from unuo.errors import BuildError
from unuo.ioc import logmanager_key


class Docker_1_1_x(object):
    """provides integration with Docker and Git

    NOTE: rename this to be not just docker specific?
          Maybe inject other SCM providers?
    """

    @inject(log_manager=logmanager_key)
    def __init__(self, log_manager):
        self.log_manager = log_manager

    def run_and_log(self, args, build_log, cwd=None):
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

    def get_short_hash(self, build, build_log):
        """Get the short hash for the HEAD of the git repo."""
        args = ['git', 'rev-parse', '--short', 'HEAD']
        p = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=build.location)
        p.wait()
        if p.returncode:
            command = ' '.join(args)
            error_msg = "!! %s, exit code %s" % (command, p.returncode)
            raise BuildError(error_msg)
        return p.stdout.read().strip()

    def do_build(self, build):
        """Takes given build and kicks it off"""
        build_log = self.log_manager.get_logger(build)
        try:
            for line in self.run_and_log(
                    ['git', 'clone', build.repo, build.location], build_log):
                yield line

            for line in self.run_and_log(
                    ['docker', 'build', '-t', build.dockertag, '.'], build_log,
                    cwd=build.location):
                yield line

            if build.push:
                for line in self.run_and_log(['docker', 'push', build.tag],
                                             build_log):
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
            self.log_manager.close_handlers(build_log)
