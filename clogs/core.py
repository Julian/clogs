import errno
import shutil
import json
import os.path
import time

from coverage.report import Reporter
from coverage.control import coverage  # I was warned. This might break.


DEFAULT_DIR = "clogs"
JSON_CLOGS_FILE = "clogs.json.js"
JSON_CLOGS_TEMPLATE = "var json_clogs = {clogs};"


class ClogReporter(Reporter):
    """
    A reporter that incrementally updates a JSON file, storing coverage data.

    """

    STATIC_DIR = "report/static"

    def __init__(self, coverage, clogger, ignore_errors=False):
        super(ClogReporter, self).__init__(coverage, ignore_errors)

        coverage.load()

        self.clogger = clogger
        self.directory = self.clogger.directory

        self.clogs = self._load_clogs()
        self.branches = coverage.data.has_arcs()

    def coverage_info(self, cu):
        analysis = self.coverage._analyze(cu)

        info = {"numbers" : analysis.numbers,
                "name" : cu.name,
                "percent_coverage" : analysis.numbers.pc_covered_str,
                "statements" : analysis.numbers.n_statements,
                "missing" : analysis.numbers.n_missing,}

        if self.branches:
            info.update(branches=analysis.numbers.n_branches,
                        missing_branches=analysis.numbers.n_missing_branches)

        return info

    def report(self, morfs, config=None):
        self.find_code_units(morfs, config)
        coverage = [self.coverage_info(cu) for cu in self.code_units]

        # Using the time of coverage, not report time, so look at modify time
        coverage_date = os.path.getmtime(self.coverage.data.filename)

        metadata = {"date" : int(coverage_date * 1000),  # js needs miliseconds
                    "coverage" : coverage,
                    "total" : len(coverage),}

        return metadata

    def _load_clogs(self):
        try:
            with open(os.path.join(self.directory, JSON_CLOGS_FILE)) as clogs:
                js_clogs = clogs.read()
        except IOError as e:
            if e.errno == errno.ENOENT:
                return []
            raise
        else:
            lstrip, clogs, rstrip = js_clogs.partition("{clogs}")
            self.clogs = json.loads(clogs.lstrip(lstrip).rstrip(rstrip))

    def _write_clogs(self):
        with open(os.path.join(self.directory, JSON_CLOGS_FILE), "w") as f:
            f.write(JSON_CLOGS_TEMPLATE.format(clogs=json.dumps(self.clogs)))

    def init(self):
        """
        Initialize a clogs directory if one does not exist.

        """

    def write(self):
        static = os.path.join(self.directory, "static")
        shutil.copytree(self.STATIC_DIR, static)
        self._write_clogs()
