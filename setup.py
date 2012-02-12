#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from clogs import __version__

# TODO: man page
with open("README.rst") as f:
    long_description = f.read()


setup(
    name="clogs",
    version=__version__,
    author="Julian Berman",
    author_email="Julian+Clogs@GrayVines.com",
    description="clogs make coverage logs",
    license="MIT/X",
    url="http://github.com/Julian/clogs",
    long_description=long_description,
    packages=find_packages(),
    scripts=["bin/clogs"],
    include_package_data=True,
    install_requires= ["coverage", "GitPython"],
)
