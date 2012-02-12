clogs
=====

*clogs make coverage logs*

``clogs`` is a tool to help log code coverage over time using Ned Batchelder's
fabulous `coverage.py <http://nedbatchelder.com/code/coverage>`_.


Installation
------------

Install ``clogs`` either via ``pip``::

    pip install clogs

or just with ``distribute`` alone::

    python setup.py install


Usage
-----


Requirements
------------

``git`` and ``hg`` are optional external dependencies that can be used to track
coverage within VCS repositories. The ``hg`` binary is directly invoked by
clogs.  ``git`` repository access is provided by ``GitPython``, which should be
installed by pip by default.


License
-------

``clogs`` is licensed under the MIT License (found in this directory).

``flot`` is copyright (c) 2007-2009 IOLA and Ole Laursen under the same license.
