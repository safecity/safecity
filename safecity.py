#!/usr/bin/python3
import argparse
from preparedataset import  prepare_dataset


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description='SafeCity')

    arg_parser.add_argument(
        '--preparedata', help='Prepare Data', action='store_true')
    arg_parser.add_argument(
        '--checkfiles', help='Check if every files are in position', action='store_true')

    args = arg_parser.parse_args()

    if args.preparedata:
        # prepare the data
        prepare_dataset()
    elif args.checkfiles:
        prepare_dataset()
    else:
        arg_parser.print_help()
