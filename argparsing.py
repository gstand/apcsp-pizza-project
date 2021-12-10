#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pizza Project - main.py - started on 8 November 2021
# Written by Garret Stand licensed under a MIT license for academic use.
# This file contains argument parsing for the program as a hacky workaround so the args structure can be accessed globally before other local dependencies are initalized. It is a non-executable library.
# Please read the readme if you wish to execute this program locally. Developed on Python 3.9.7

import argparse

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("This is a library. This was probably ran accidentally.\nPlease execute the pizza program from the \"main.py\" program contained in the root of the project (" + dir_path + ") by running \"python3 main.py\", or open it in a text editor/IDE to see its contents and use in the program.")
    exit(1)

def returnArgs():
    parser = argparse.ArgumentParser(prog='python3 main.py', description='APCSP Pizza Project - Interface with the Pizza Ordering System.', epilog='Written by Garret Stand licensed under a MIT license for academic use. See the readme for more information. Enjoy :)')
    parser.add_argument('-c', '--configure', dest='configFlag', action='store_true', help='Configure the prefrences that are used in the program. (see data/config.json)')
    parser.add_argument('-r', '--reset', dest='resetFlag', action='store_true', help='Reset the order database.')
    parser.add_argument('-d', '--debug', dest='debugFlag', action='store_true', help='Enables debug messages and features.')

    args = parser.parse_args()
    return args

