#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pizza Project - main.py - started on 8 November 2021
# Written by Garret Stand licensed under a MIT license for academic use.
# This file contains the main executable code and serves as the entry point for the program.
# Please read the readme if you wish to execute this program locally. Developed on Python 3.10.0

#region import statements and variable initalization and generic pre-program tasks
import json
import sys
import os
import random
import uuid
import platform
import argparse
# DEVNOTE: import all external libraries/dependencies above this line, and all internal libraries/dependencies below this line, makes sure all related dependencies including the ones used in the libraries are loaded before the libraries themselves are loaded to avoid initalization errors and the likes
import dataDriver
import orders
import out

parser = argparse.ArgumentParser(prog='python3 main.py', description='APCSP Pizza Project - Interface with the Pizza Ordering System.', epilog='Written by Garret Stand licensed under a MIT license for academic use. See the readme for more information. Enjoy :)')
parser.add_argument('-c', '--configure', dest='configFlag', action='store_true', help='Configure the prefrences that are used in the program. (see data/config.json)')
parser.add_argument('-r', '--reset', dest='resetFlag', action='store_true', help='Reset the order database.')
parser.add_argument('-d', '--debug', dest='debugFlag', action='store_true', help='Enables debug messages and features.')

args = parser.parse_args()

if args.configFlag == True:
    dataDriver.configWizard()

if args.resetFlag == True:
    dataDriver.reset()

if args.debugFlag == True:
    out.printNotice("Debug mode enabled.")

configData = dataDriver.loadConfig()
orderData = dataDriver.loadOrders()

dataDriver.validateOrders()

try:
    parlorName == configData['parlorName']
except:
    out.printError("No parlor name found in config.json. Dropping to configuration.")
    dataDriver.configure()
#endregion

print(out.bold + "Welcome to " + parlorName + "!" + out.reset)
print("Would you like to start an order?" + out.dim + " (Y/n)" + out.reset + ": ", end='') # ask user whether to start or not
go = str(input()).lower()
print(end='')
if go == "n" :
    exit()
if not go:
    None
elif go != "y" or go != "n": # fallback just in case the user doesnt understand the prompt
    print("Not y or n, assuming yes...")

def mainMenu():
    out.clear()
    print("Welcome to the " + parlorName + " Ordering System!")
    print("Please choose from the following:")
    print("1. Create a new order")
    print("2. View and modify existing orders")
    print("3. Exit")
    print("4. Debug options") if args.debugFlag == True else None
    choice = int(input("Enter your choice: "))
    if choice == 1:
        orders.newOrder()
    elif choice == 2:
        orders.viewOrders()
    elif choice == 3:
        exit()
    elif choice == 4 and debugFlag == True:
        debugOptions()
    else:
        print("Invalid choice. Please try again.")
        mainMenu()