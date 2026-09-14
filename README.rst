ZFS Utils for OS X
==============================================================================

Introduction
------------------------------------------------------------------------------

.. image:: https://github.com/wolph/zfs-utils-osx/actions/workflows/tests.yml/badge.svg?branch=master
    :target: https://github.com/wolph/zfs-utils-osx/actions/workflows/tests.yml?query=branch%3Amaster
    :alt: Master test status

.. image:: https://coveralls.io/repos/github/wolph/zfs-utils-osx/badge.svg?branch=master
    :target: https://coveralls.io/github/wolph/zfs-utils-osx?branch=master
    :alt: Master test coverage

A simple script to create and manage virtual ZFS images on OS X without
requiring repartitioning

Install
------------------------------------------------------------------------------

To install simply run `pip install zfs-utils-osx`.

Example usage
------------------------------------------------------------------------------

To create a pool (does a dry-run with the `-n` flag):

    zfs.py zpool -n <pool_name>

Usage:

    usage: zfs.py [-h] {zpool} ...

    optional arguments:
      -h, --help  show this help message and exit

    Subcommands:
      Please specify one of the following subcommands

      {zpool,load}
        zpool     zpool creation
        load        load (import) the zpools

Zpool create usage:

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

Zpool import usage:

    usage: zfs.py load [-h] [-d IMAGE_DIRECTORY] [-p PREFIX] [--postfix POSTFIX]
                       [-n]
                       pool_names [pool_names ...]

    positional arguments:
      pool_names            The name of the pool to import

    optional arguments:
      -h, --help            show this help message and exit
      -d IMAGE_DIRECTORY, --image-directory IMAGE_DIRECTORY
                            File name pattern to store the images (default:
                            ~/zfs/)
      -p PREFIX, --prefix PREFIX
                            File name prefix for the images (default:
                            %(pool_name)s_)
      --postfix POSTFIX     File name postfix for the images (default: )
      -n, --no-op, --dry-run
                            Show what will be done but dont execute

Testing
------------------------------------------------------------------------------

Run the Python 2.7 tests in Docker::

    docker run --rm -v "$PWD:/work" -w /work python:2.7.18-buster \
        sh -c 'python -m pip install -r requirements.txt && python -m pytest'

The tests replace command execution and directory traversal with test doubles.
They do not create disk images or invoke ZFS. Coverage includes every package
module and requires 100 percent line and branch coverage. These tests preserve
existing behaviour, including integer division with the default size and reuse
of the first expanded prefix when loading multiple pools.
