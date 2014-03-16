ZFS Utils for OS X
==============================================================================

Introduction
------------------------------------------------------------------------------

.. image:: https://travis-ci.org/WoLpH/zfs-utils-osx.png?branch=master
    :alt: Test Status
    :target: https://travis-ci.org/WoLpH/zfs-utils-osx

.. image:: https://coveralls.io/repos/WoLpH/zfs-utils-osx/badge.png?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/r/WoLpH/zfs-utils-osx?branch=master

.. image:: https://landscape.io/github/WoLpH/django-statsd/master/landscape.png
   :target: https://landscape.io/github/WoLpH/django-statsd/master
   :alt: Code Health

.. image:: https://requires.io/github/WoLpH/zfs-utils-osx/requirements.png?branch=master
   :target: https://requires.io/github/WoLpH/zfs-utils-osx/requirements/?branch=master
   :alt: Requirements Status

A simple script to create and manage virtual ZFS images on OS X without
requiring repartitioning

Install
-------

To install simply execute run `pip install zfs-utils-osx`.

Usage
-----

To create a pool (does a dry-run with the `-n` flag):

    zfs.py zpool -n <pool_name>

