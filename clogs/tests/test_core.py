import errno
import unittest

from coverage.codeunit import CodeUnit
import mock

from clogs import core as c


class TestCore(unittest.TestCase):
    def setUp(self):
        super(TestCore, self).setUp()

        self.coverage = mock.Mock()
        self.clogger = mock.Mock()
        self.r = c.ClogReporter(coverage=self.coverage, clogger=self.clogger)

    def test_init(self):
        self.coverage.data.has_arcs.return_value = True
        self.assertTrue(self.r.branches)

        self.coverage.data.has_arcs.return_value = False
        r = c.ClogReporter(coverage=self.coverage, clogger=self.clogger)
        self.assertFalse(r.branches)

        self.assertIs(r.clogger, self.clogger)

    def test_crinit(self):
        IGNORES = "*.coffee",

        with mock.patch("clogs.core.shutil") as shutil:
            self.r.init()

        shutil.ignore_patterns.assert_called_once_with(*IGNORES)
        self.assertTrue(shutil.copytree.called)

    def test_load_clogs(self):
        with mock.patch("clogs.core.os.path.join") as join:

            with mock.patch("clogs.core.open", create=True) as mock_open:
                sample_json = "var json_clogs = '[[]]';\n"

                mock_open.return_value = f = mock.MagicMock(spec=file)
                f.__enter__.return_value.read.return_value = sample_json

                clogs = self.r.load_clogs()

                mock_open.assert_called_once_with(join.return_value)
                self.assertEqual(clogs, [[]])

            with mock.patch("clogs.core.open", create=True) as mock_open:
                whoops_doesnt_exist = IOError()
                whoops_doesnt_exist.errno = errno.ENOENT

                mock_open.side_effect = whoops_doesnt_exist

                clogs = self.r.load_clogs()
                mock_open.assert_called_once_with(join.return_value)

                self.assertEqual(clogs, [])

                with self.assertRaises(IOError):
                    mock_open.side_effect = IOError()
                    self.r.load_clogs()
