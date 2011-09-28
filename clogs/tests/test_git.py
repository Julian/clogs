from __future__ import absolute_import
import unittest

from git import Repo
import mock

from clogs import git


class TestGitClogger(unittest.TestCase):
    def setUp(self):
        super(TestGitClogger, self).setUp()

        with mock.patch("clogs.git.git.Repo", mock.Mock(spec=Repo)):
            self.g = git.GitClogger(directory="foo")
            self.repo = self.g.repo

    def test_init(self):
        self.assertEqual(self.g.directory, "foo")

    def test_commit_id(self):
        self.assertEqual(self.g.commit_id, self.repo.head.commit.hexsha)
