#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pizza Project - main.py - started on 8 November 2021
# Written by Garret Stand licensed under a MIT license for academic use.
# This file contains shell formatting and other output modification/redirections functions for the program. It is a non-executable library.
# Please read the readme if you wish to execute this program locally. Developed on Python 3.9.7

import json
import sys
import os
import random
import uuid
import platform
import argparse
# DEVNOTE: import all external libraries/dependencies above this line, and all internal libraries/dependencies below this line
import dataDriver
import orders

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("This is a library. This was probably ran accidentally.\nPlease execute the pizza program from the \"main.py\" program contained in the root of the project (" + dir_path + ") by running \"python3 main.py\", or open it in a text editor/IDE to see its contents and use in the program.")
    exit(1)

if platform.system() == 'Linux' or platform.system() == 'Darwin': # color initalization for linux/macos, wont work on windows (exceprt from my python library)
    red='\033[00;31m'
    green='\033[00;32m'
    yellow='\033[00;33m'
    blue='\033[00;34m'
    purple='\033[00;35m'
    cyan='\033[00;36m'
    lightgray='\033[00;37m'
    lred='\033[01;31m'
    lgreen='\033[01;32m'
    lyellow='\033[01;33m'
    lblue='\033[01;34m'
    lpurple='\033[01;35m'
    lcyan='\033[01;36m'
    white='\033[01;37m'
    bold='\033[01m'
    dim='\033[02m'
    blink='\033[05m' # not working/odd behaviour in some terminals but this is known
    underlined='\033[04m'
    reverse='\033[07m'
    passwordhide='\033[08m'
    reset='\033[0m'
    errorBG='\033[41;30m'
    noticeBG='\033[43;30m'
    debugBG='\033[47;30m'
else:
    red=''
    green=''
    yellow=''
    blue=''
    purple=''
    cyan=''
    lightgray=''
    lred=''
    lgreen=''
    lyellow=''
    lblue=''
    lpurple=''
    lcyan=''
    white=''
    bold=''
    dim=''
    blink=''
    underlined=''
    reverse=''
    passwordhide=''
    reset=''
    errorBG=''
    noticeBG=''

indent = u'\U00000009' # unicode tabulation charecter, for use in printing data structures in debug subroutines and raw data writes when necessary for the data driver (yes i use tabs), or other printing/layout use.

def printError(text, debug=False):
    if debug:
        print(errorBG + "[ERROR]" + reset + " " + text) if args.debugFlag else None
    else:
        print(errorBG + "[ERROR]" + reset + " " + text)

def printNotice(text, debug=False):
    if debug:
        print(noticeBG + "[NOTICE]" + reset + " " + text) if args.debugFlag else None
    else:
        print(noticeBG + "[NOTICE]" + reset + " " + text)
    
def printDebug(text):
    print(debugBG + "[DEBUG]" + reset + " " + text) if args.debugFlag else None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

