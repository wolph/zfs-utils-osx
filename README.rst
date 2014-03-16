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
------------------------------------------------------------------------------

To install simply run `pip install zfs-utils-osx`.

Example usage
------------------------------------------------------------------------------

To create a pool (does a dry-run with the `-n` flag):

    zfs.py zpool -n <pool_name>

::
    usage: zfs.py [-h] {zpool} ...

    optional arguments:
      -h, --help  show this help message and exit

    Subcommands:
      Please specify one of the following subcommands

      {zpool}
        zpool     zpool creation

::
    usage: zfs.py zpool [-h] [-c COUNT] [-s SIZE]
                        [-t {raidz1,raidz2,raidz3,mirror,raidz}] [-n]
                        [-m MOUNTPOINT] [-o] [-p PATTERN]
                        pool_name

    positional arguments:
      pool_name             The name of the pool to create

    optional arguments:
      -h, --help            show this help message and exit
      -c COUNT, --count COUNT
                            The amount of images to use (default: 3)
      -s SIZE, --size SIZE  The usable size of the zpool in GiB (default: 10GiB)
      -t {raidz1,raidz2,raidz3,mirror,raidz}, --type {raidz1,raidz2,raidz3,mirror,raidz}
                            The zpool type to use (default: raidz)
      -n, --no-op, --dry-run
                            Show what will be done but dont execute
      -m MOUNTPOINT, --mountpoint MOUNTPOINT
                            Where should the disk be mounted (default:
                            ~/%(pool_name)s
      -o, --overwrite       Overwrite old images if they exist
      -p PATTERN, --pattern PATTERN
                            File name pattern to store the images (default:
                            %(pool_name)s_%(i)02d)
