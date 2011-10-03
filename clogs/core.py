import errno
import shutil
import json
import os.path
import time

from coverage.report import Reporter
from coverage.control import coverage  # I was warned. This might break.


DEFAULT_DIR = "clogs"
JSON_CLOGS_FILE = "clogs.json.js"
JSON_CLOGS_TEMPLATE = "var json_clogs = '{clogs}';\n"


class ClogReporter(Reporter):
    """
    A reporter that incrementally updates a JSON file, storing coverage data.

    """

    STATIC_DIR = "static"

    def __init__(self, coverage, clogger, ignore_errors=False):
        super(ClogReporter, self).__init__(coverage, ignore_errors)

        coverage.load()

        self.clogger = clogger
        self.directory = self.clogger.directory
        self.branches = coverage.data.has_arcs()

    def coverage_info(self, cu):
        analysis = self.coverage._analyze(cu)

        info = {"name" : cu.name,
                "percent_coverage" : analysis.numbers.pc_covered_str,
                "statements" : analysis.numbers.n_statements,
                "missing" : analysis.numbers.n_missing,}

        if self.branches:
            info.update(branches=analysis.numbers.n_branches,
                        missing_branches=analysis.numbers.n_missing_branches)

        return info

    def report(self, morfs, config):
        self.find_code_units(morfs, config)
        coverage = [self.coverage_info(cu) for cu in self.code_units]

        # Using the time of coverage, not report time, so look at modify time
        coverage_date = os.path.getmtime(self.coverage.data.filename)

        new_clog = {"date" : int(coverage_date * 1000),  # js needs miliseconds
                    "coverage" : coverage,
                    "total" : len(coverage),}

        clogs = self.load_clogs()
        clogs.append(new_clog)
        self._write_clogs(clogs)

    def load_clogs(self):
        try:
            with open(os.path.join(self.directory, JSON_CLOGS_FILE)) as clogs:
                js_clogs = clogs.read()
        except IOError as e:
            if e.errno == errno.ENOENT:
                return []
            raise
        else:
            lstrip, _, rstrip = JSON_CLOGS_TEMPLATE.partition("{clogs}")
            return json.loads(js_clogs.lstrip(lstrip).rstrip(rstrip))

    def _write_clogs(self, clogs=()):
        with open(os.path.join(self.directory, JSON_CLOGS_FILE), "w") as f:
            f.write(JSON_CLOGS_TEMPLATE.format(clogs=json.dumps(clogs)))

    def init(self):
        """
        Initialize a clogs directory if one does not exist.

        """

        # all the CS files should be precompiled to JS files
        ignore = shutil.ignore_patterns("*.coffee")
        static = os.path.join(os.path.dirname(__file__), self.STATIC_DIR)
        shutil.copytree(static, self.directory, ignore=ignore)
