import argparse


def greater_than(string, cast, minimum):
    value = cast(string)
    if value > minimum:
        return value
    raise argparse.ArgumentTypeError('%r needs to be greater than %r' %
                                     (string, minimum))

