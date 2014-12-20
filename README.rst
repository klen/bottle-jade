Bottle Jade
###########

.. _description:

Bottle Jade -- Short description.

.. _badges:

.. image:: http://img.shields.io/travis/klen/bottle-jade.svg?style=flat-square
    :target: http://travis-ci.org/klen/bottle-jade
    :alt: Build Status

.. image:: http://img.shields.io/coveralls/klen/bottle-jade.svg?style=flat-square
    :target: https://coveralls.io/r/klen/bottle-jade
    :alt: Coverals

.. image:: http://img.shields.io/pypi/v/bottle-jade.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bottle-jade

.. image:: http://img.shields.io/pypi/dm/bottle-jade.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bottle-jade

.. image:: http://img.shields.io/gratipay/klen.svg?style=flat-square
    :target: https://www.gratipay.com/klen/
    :alt: Donate

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 2.6

.. _installation:

Installation
=============

**Bottle Jade** should be installed using pip: ::

    pip install bottle-jade

.. _usage:

Usage
=====
::

    from bottle import Bottle
    from bottle_jade import JadePlugin
    from os import path as op

    app = Bottle()
    templates = op.dirname(op.abspath(__file__))
    jade = app.install(JadePlugin(template_folder=templates))

    @app.route('/')
    def index():
        context = {'var': 'value'}
        return jade.render('index.jade', **context)

    @app.route('/simple')
    @jade.view('simple.jade')
    def simple():
        context = {}
        return context


Configuration
-------------

JADE_CACHE_SIZE -- Number of templates which will be cached (200)
JADE_PRETTY -- Enable pretty output (True)
JADE_TEMPLATE_FOLDER -- Set path to templates folder (templates)
JADE_ENCODING -- Set templates' encoding (UTF-8)

.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/bottle-jade/issues

.. _contributing:

Contributing
============

Development of Bottle Jade happens at: https://github.com/klen/bottle-jade


Contributors
=============

* klen_ (Kirill Klenov)

.. _license:

License
=======

Licensed under a `BSD license`_.

.. _links:

.. _BSD license: http://www.linfo.org/bsdlicense.html
.. _klen: https://github.com/klen
