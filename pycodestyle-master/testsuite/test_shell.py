# -*- coding: utf-8 -*-
import os.path
import sys
import unittest

import pycodestyle
from testsuite.support import ROOT_DIR, PseudoFile


class ShellTestCase(unittest.TestCase):
    """Test the usual CLI options and output."""

    def setUp(self):
        self._saved_argv = sys.argv
        self._saved_stdout = sys.stdout
        self._saved_stderr = sys.stderr
        self._saved_pconfig = pycodestyle.PROJECT_CONFIG
        self._saved_cpread = pycodestyle.RawConfigParser._read
        self._saved_stdin_get_value = pycodestyle.stdin_get_value
        self._config_filenames = []
        self.stdin = ''
        sys.argv = ['pycodestyle']
        sys.stdout = PseudoFile()
        sys.stderr = PseudoFile()

        def fake_config_parser_read(cp, fp, filename):
            self._config_filenames.append(filename)
        pycodestyle.RawConfigParser._read = fake_config_parser_read
        pycodestyle.stdin_get_value = self.stdin_get_value

    def tearDown(self):
        sys.argv = self._saved_argv
        sys.stdout = self._saved_stdout
        sys.stderr = self._saved_stderr
        pycodestyle.PROJECT_CONFIG = self._saved_pconfig
        pycodestyle.RawConfigParser._read = self._saved_cpread
        pycodestyle.stdin_get_value = self._saved_stdin_get_value

    def stdin_get_value(self):
        return self.stdin

    def pycodestyle(self, *args):
        del sys.stdout[:], sys.stderr[:]
        sys.argv[1:] = args
        try:
            pycodestyle._main()
            errorcode = None
        except SystemExit:
            errorcode = sys.exc_info()[1].code
        return sys.stdout.getvalue(), sys.stderr.getvalue(), errorcode

    def test_print_usage(self):
        stdout, stderr, errcode = self.pycodestyle('--help')
        self.assertFalse(errcode)
        self.assertFalse(stderr)
        self.assertTrue(stdout.startswith(
            "Usage: pycodestyle [options] input"
        ))

        stdout, stderr, errcode = self.pycodestyle('--version')
        self.assertFalse(errcode)
        self.assertFalse(stderr)
        self.assertEqual(stdout.count('\n'), 1)

        stdout, stderr, errcode = self.pycodestyle('--obfuscated')
        self.assertEqual(errcode, 2)
        self.assertEqual(stderr.splitlines(),
                         ["Usage: pycodestyle [options] input ...", "",
                          "pycodestyle: error: no such option: --obfuscated"])
        self.assertFalse(stdout)

        self.assertFalse(self._config_filenames)

    def test_check_simple(self):
        E11 = os.path.join(ROOT_DIR, 'testsuite', 'E11.py')
        stdout, stderr, errcode = self.pycodestyle(E11)
        stdout = stdout.splitlines()
        self.assertEqual(errcode, 1)
        self.assertFalse(stderr)
        self.assertEqual(len(stdout), 24)
        for line, num, col in zip(stdout, (3, 6, 6, 9, 12), (3, 6, 6, 1, 5)):
            path, x, y, msg = line.split(':')
            self.assertTrue(path.endswith(E11))
            self.assertEqual(x, str(num))
            self.assertEqual(y, str(col))
            self.assertTrue(msg.startswith(' E11'))
        # Config file read from the pycodestyle's setup.cfg
        config_filenames = [os.path.basename(p)
                            for p in self._config_filenames]
        self.assertTrue('setup.cfg' in config_filenames)

    def test_check_stdin(self):
        pycodestyle.PROJECT_CONFIG = ()
        stdout, stderr, errcode = self.pycodestyle('-')
        self.assertFalse(errcode)
        self.assertFalse(stderr)
        self.assertFalse(stdout)

        self.stdin = 'import os, sys\n'
        stdout, stderr, errcode = self.pycodestyle('-')
        stdout = stdout.splitlines()
        self.assertEqual(errcode, 1)
        self.assertFalse(stderr)
        self.assertEqual(stdout,
                         ['stdin:1:10: E401 multiple imports on one line'])

    def test_check_non_existent(self):
        self.stdin = 'import os, sys\n'
        stdout, stderr, errcode = self.pycodestyle('fictitious.py')
        self.assertEqual(errcode, 1)
        self.assertFalse(stderr)
        self.assertTrue(stdout.startswith('fictitious.py:1:1: E902 '))

    def test_check_noarg(self):
        # issue #170: do not read stdin by default
        pycodestyle.PROJECT_CONFIG = ()
        stdout, stderr, errcode = self.pycodestyle()
        self.assertEqual(errcode, 2)
        self.assertEqual(stderr.splitlines(),
                         ["Usage: pycodestyle [options] input ...", "",
                          "pycodestyle: error: input not specified"])
        self.assertFalse(self._config_filenames)