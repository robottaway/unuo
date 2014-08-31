import unittest
import logging

from mock import patch, Mock

logger = logging.getLogger('test')


class DockerTest(unittest.TestCase):
    """Test Docker integration"""

    def test_get_short_hash(self):
        """Test getting short hash"""
        from unuo.docker import Docker_1_1_x
        docker = Docker_1_1_x(None)
        with patch('unuo.docker.subprocess') as subprocess:
            build = Mock()
            build.build_location = "anywhere"
            subprocess.Popen.return_value.returncode = 0
            subprocess.Popen.return_value.stdout.read.return_value = " bah "
            rv = docker.get_short_hash(build, None)
            self.assertEquals("bah", rv)

    def test_get_short_hash_fail(self):
        """Test non-zero return code"""
        from unuo.docker import Docker_1_1_x
        from unuo.errors import BuildError
        docker = Docker_1_1_x(None)
        with patch('unuo.docker.subprocess') as subprocess:
            build = Mock()
            build.build_location = "anywhere"
            subprocess.Popen.return_value.returncode = 1
            try:
                docker.get_short_hash(build, None)
                self.fail('BuildError not thrown!')
            except BuildError:
                pass

    def test_run_and_log(self):
        """Test running of command"""
        from unuo.docker import Docker_1_1_x
        docker = Docker_1_1_x(None)
        with patch('unuo.docker.subprocess') as subprocess:
            subprocess.Popen.return_value.returncode = 0
            subprocess.Popen.return_value.stdout = ['line0', 'line1', 'line2']
            i = 0
            for line in docker.run_and_log([], None):
                val = 'line%s' % i
                self.assertEquals(val, line)
                i += 1
            self.assertEquals(3, i)

    def test_run_and_log_fail(self):
        """Test non-zero return code"""
        from unuo.docker import Docker_1_1_x
        from unuo.errors import BuildError
        docker = Docker_1_1_x(None)
        with patch('unuo.docker.subprocess') as subprocess:
            subprocess.Popen.return_value.returncode = 1
            subprocess.Popen.return_value.stdout = ['line0', 'line1', 'line2']
            i = 0
            try:
                for line in docker.run_and_log([], None):
                    val = 'line%s' % i
                    self.assertEquals(val, line)
                    i += 1
                self.fail('BuildError not thrown!')
            except BuildError:
                pass
            self.assertEquals(3, i)

    def test_do_build(self):
        """Test running of do_build"""
        from unuo.docker import Docker_1_1_x
        with patch.object(Docker_1_1_x, 'run_and_log') as run_and_log:
            logmanager = Mock()
            build = Mock()
            build.repo = 'arepo'
            build.dockertag = 'atag'
            build.location = 'alocation'
            build.push = True
            run_and_log.return_value = ['line1', 'line2']
            with patch('unuo.docker.shutil.rmtree') as rmtree:
                rmtree.return_value = None
                docker = Docker_1_1_x(logmanager)
                for line in docker.do_build(build):
                    pass

    def test_do_build_build_error(self):
        """Test running of do_build"""
        from unuo.docker import Docker_1_1_x
        from unuo.errors import BuildError
        with patch.object(Docker_1_1_x, 'run_and_log') as run_and_log:
            run_and_log.side_effect = BuildError('oh no')
            logmanager = Mock()
            build = Mock()
            build.repo = 'arepo'
            build.dockertag = 'atag'
            build.location = 'alocation'
            build.push = True
            docker = Docker_1_1_x(logmanager)
            self.assertEquals('oh no', docker.do_build(build).next())

    def test_do_build_shutil_errror(self):
        """Test running of do_build"""
        from unuo.docker import Docker_1_1_x
        with patch.object(Docker_1_1_x, 'run_and_log') as run_and_log:
            with patch('unuo.docker.shutil.rmtree') as rmtree:
                rmtree.side_effect = Exception('noooo')
                run_and_log.return_value = ['pass']
                logmanager = Mock()
                build = Mock()
                build.repo = 'arepo'
                build.dockertag = 'atag'
                build.location = 'alocation'
                build.push = False
                docker = Docker_1_1_x(logmanager)
                g = docker.do_build(build)
                self.assertEquals('pass', g.next())
                self.assertEquals('pass', g.next())
                self.assertEquals(
                    '!! Unable to remove build folder',
                    g.next())

    def test_do_build_oserror(self):
        """Test running of do_build"""
        from unuo.docker import Docker_1_1_x
        with patch.object(Docker_1_1_x, 'run_and_log') as run_and_log:
            run_and_log.side_effect = OSError('oh no', strerror='oh no')
            logmanager = Mock()
            build = Mock()
            build.repo = 'arepo'
            build.dockertag = 'atag'
            build.location = 'alocation'
            docker = Docker_1_1_x(logmanager)
            self.assertEquals('oh no', docker.do_build(build).next())
