#!/usr/bin/env python
import sys
import argparse

from . import Lox


def get_args():
    parser = argparse.ArgumentParser(description='PyLox')
    parser.add_argument(
        'script', type=str, nargs='?',
        help='script file name')

    return parser.parse_args()

def main():
    args = get_args()

    lox = Lox()
    if args.script:
        lox.run_file(args.script)
    else:
        lox.run_prompt()

    return lox.error_code()


if __name__ == '__main__':
    sys.exit(main())
