#!/usr/bin/env python
import argparse
import zpool


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        title='Subcommands',
        description='Please specify one of the following subcommands')
    zpool.get_parser(subparsers)

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

