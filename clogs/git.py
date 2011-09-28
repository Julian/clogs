from __future__ import absolute_import

import git


class GitClogger(object):
    def __init__(self, directory="", repo_dir=None):
        super(GitClogger, self).__init__()

        if repo is None:
            repo = directory

        self.directory = directory
        self.repo = git.Repo(repo_dir).config_reader()  # read-only access

    @property
    def commit_id(self):
        return self.repo.head.commit.hexsha
