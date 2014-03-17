import re
import os
import sys
import subprocess
import textwrap
import decimal
from . import constants
from . import utils
from . import argparse_utils


def load_command(args):
    patterns = []
    for name in args.pool_names:
        context = vars(args)
        context['pool_name'] = name
        context['prefix'] %= context
        context['postfix'] %= context
        patterns.append(constants.IMAGE_NAME_RE % context)

    pattern = re.compile('(%s)' % '|'.join(patterns))
    full_path = os.path.abspath(os.path.expanduser(args.image_directory))
    for path, dirs, files in os.walk(full_path):
        for file_ in files:
            match = pattern.match(file_)
            if not match:
                continue
            try:
                context['name'] = os.path.join(path, file_)
                utils.execute( context, constants.ZPOOL_ATTACH_IMAGE_COMMAND)
            except subprocess.CalledProcessError:
                print 'Unable to attach image'
                sys.exit(1)

    for name in args.pool_names:
        context = vars(args)
        context['pool_name'] = name

        try:
            utils.execute( context, constants.ZPOOL_IMPORT_COMMAND)
        except subprocess.CalledProcessError:
            print 'Unable to import zpool'
            sys.exit(1)


def get_parser(subparsers):
    load = subparsers.add_parser('load', help='load (import) the zpools')
    load.add_argument('pool_names', help='The name of the pool to import',
                       nargs='+')
    load.add_argument(
        '-d', '--image-directory', default='~/zfs/',
        help='File name pattern to store the images (default: %(default)s)')
    load.add_argument(
        '-p', '--prefix', default='%(pool_name)s_',
        help='File name prefix for the images (default: %(default)s)')
    load.add_argument(
        '--postfix', default='',
        help='File name postfix for the images (default: %(default)s)')
    load.add_argument(
        '-n', '--no-op', '--dry-run', action='store_true',
        help='Show what will be done but dont execute')
    load.set_defaults(func=load_command)


