#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

from clogs import __version__

# TODO: man page

long_description = (
"""clogs is a lightweight way to track code coverage over time using Ned
Bachelder's fabulous coverage.py."""
)

setup(
    name="clogs",
    version = __version__,
    author = "Julian Berman",
    author_email = "Julian+Clogs@GrayVines.com",
    description = "clogs make coverage logs",
    license = "MIT/X",
    url = "http://github.com/Julian/clogs",
    long_description = long_description,
    packages = ["clogs", "clogs.tests"],
    scripts = ["bin/clogs"],
    install_requires = [
        "coverage",
        "GitPython",
    ],
)
