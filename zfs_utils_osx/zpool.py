import sys
import subprocess
import textwrap
from . import constants
from . import utils
from . import argparse_utils


def zpool_command(args):
    context = vars(args)
    effective_image_count = constants.ZPOOL_TYPES[args.type](args.count)
    context['image_size'] = args.size / effective_image_count
    context['physical_size'] = context['image_size'] * args.count
    context['effective_size'] = context['image_size'] * effective_image_count
    context['i'] = 0
    context['name'] = args.pattern % context
    context['extra_args'] = ''
    print textwrap.fill(constants.ZPOOL_CREATE_MESSAGE % context)

    devices = []
    for i in range(args.count):
        context['i'] = i
        context['name'] = args.pattern % context
        try:
            if args.overwrite:
                arg = '-ov'
            else:
                arg = ''

            utils.execute(context, constants.ZPOOL_CREATE_IMAGE_COMMAND, arg)
        except subprocess.CalledProcessError:
            print 'Unable to create a new image'
            sys.exit(1)

        try:
            device = utils.execute(context,
                                   constants.ZPOOL_ATTACH_IMAGE_COMMAND)
            if device:
                devices.append(device.strip())
        except subprocess.CalledProcessError:
            print 'Unable to attach image'
            sys.exit(1)

    if devices:
        context['devices'] = ' '.join(devices)
        context['mountpoint'] %= context
        utils.execute(context, constants.ZPOOL_CREATE_COMMAND)

def get_parser(subparsers):
    zpool = subparsers.add_parser('zpool', help='zpool creation')
    zpool.add_argument(
        '-c', '--count', default=3,
        type=lambda s: argparse_utils.greater_than(s, int, 1),
        help='The amount of images to use (default: %(default)s)')
    zpool.add_argument(
        '-s', '--size', default=10,
        type=lambda s: argparse_utils.greater_than(s, decimal.Decimal, 0),
        help='The usable size of the zpool in GiB (default: %(default)sGiB)')
    zpool.add_argument(
        '-t', '--type', choices=constants.ZPOOL_TYPES, default='raidz',
        help='The zpool type to use (default: %(default)s)')
    zpool.add_argument(
        '-n', '--no-op', '--dry-run', action='store_true',
        help='Show what will be done but dont execute')
    zpool.add_argument(
        '-m', '--mountpoint', default='~/%(pool_name)s',
        help='Where should the disk be mounted (default: %(default)s')
    zpool.add_argument(
        '-o', '--overwrite', action='store_true',
        help='Overwrite old images if they exist')
    zpool.add_argument('pool_name', help='The name of the pool to create')
    zpool.add_argument(
        '-p', '--pattern', default='%(pool_name)s_%(i)02d',
        help='File name pattern to store the images (default: %(default)s)')
    zpool.set_defaults(func=zpool_command)
