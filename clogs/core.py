import shutil
import json
import os.path
import time

from coverage.report import Reporter


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

        self.clogger = clogger
        self.directory = self.clogger.directory

        self.clogs = self._load_clogs(directory)
        self.branches = coverage.data.has_arcs()

    def coverage_info(self, cu):
        analysis = self.coverage._analyze(cu)

        info = {"numbers" : analysis.numbers,
                "name" : cu.name,
                "percent_coverage" : analysis.numbers.pc_covered_str,
                "statements" : analysis.numbers.n_statements,
                "missing" : analysis.numbers.n_missing,}

        if self.branches:
            info.update(branches=nums.n_branches,
                        missing_branches=nums.n_missing_branches)

        return info

    def report(self, morfs, config=None):
        self.find_code_units(morfs, config)
        units = [self.coverage_info(cu) for cu in self.code_units]

        # XXX : Use the time of coverage, not time of the report
        metadata = {"date" : time.time() * 1000,  # javascript needs milisecs
                    "coverage" : units,
                    "total" : len(units),}

    def _load_clogs(self):
        try:
            with open(os.path.join(self.directory, JSON_CLOGS_FILE)) as clogs:
                js_clogs = clogs.read()
        except OSError as e:
            if e.errno == errno.ENOENT:
                return []
            raise
        else:
            lsplit, clogs, rsplit = js_clogs.partition("{clogs}")
            self.clogs = json.loads(clogs.lsplit(lsplit).rsplit(rsplit))

    def _write_clogs(self):
        with open(os.path.join(self.directory, JSON_CLOGS_FILE), "w") as f:
            f.write(JSON_CLOGS_TEMPLATE.format(clogs=json.dumps(self.clogs))

    def write(self):
        static = os.path.join(self.directory, "static")
        shutil.copytree(self.STATIC_DIR, static)
        self._write_clogs()
