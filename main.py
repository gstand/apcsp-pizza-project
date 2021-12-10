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
import fpdf
import time
import subprocess
# DEVNOTE: import all external libraries/dependencies above this line, and all internal libraries/dependencies below this line, makes sure all related dependencies including the ones used in the libraries are loaded before the libraries themselves are loaded to avoid initalization errors and the likes
import argparsing
import dataDriver
import orders
import out

args = argparsing.returnArgs()

if args.configFlag == True:
    dataDriver.configWizard()

if args.resetFlag == True:
    dataDriver.reset()

if args.debugFlag == True:
    out.printNotice("Debug mode enabled.")

dataDriver.validateConfig()
dataDriver.validateOrders()

configData = dataDriver.loadConfig()
orderData = dataDriver.loadOrders()

try:
    parlorName = configData['parlorName']
except:
    out.printError("No parlor name found in config.json. Dropping to configuration.")
    dataDriver.configWizard()
    configData = dataDriver.loadConfig()
    parlorName = configData['parlorName']
#endregion

#region function definitions
def debugOptions():
    out.clear()
    print("Debug options:")
    print("1. List orders with details " + out.dim + "<internal routine dataDriver.__listOrders()>" + out.reset)
    print("2. Load custom order database " + out.dim + "(main routine context only, replace named database with custom database for global scope)" + out.reset)
    print("3. Load custom configuration store " + out.dim + "(main routine context only, replace named configuration store with custom configuration store for global scope)" + out.reset)
    print("4. Configuration wizard")
    print("5. Reset orders")
    print("6. Reset configuration to hardcoded defaults")
    print("7. Manually verify and reload orders")
    print("8. Manually verify and reload configuration")
    print("9. Hot-reload program")
    print("10. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a valid choice. " + out.dim + "Press enter to continue." + out.reset, end='')
        input()
        debugOptions()
    if choice == 1:
        out.clear()
        dataDriver.__listOrders(dataDriver.loadOrders())
        print(out.dim + "Press enter to continue." + out.reset, end='')
        input()
        debugOptions()
    elif choice == 2:
        customOrders = input("Please enter the absoulute path to the custom order database: ")
        with open(customOrders, 'r') as f: orderData = json.load(f)
        input("Loaded new database at " + customOrders + ". Press enter to continue.")
        debugOptions()
    elif choice == 3:
        customConfig = input("Please enter the absoulute path to the custom configuration store: ")
        with open(customConfig, 'r') as f: configData = json.load(f)
        input("Loaded new configuration store at " + customConfig + ". Press enter to continue.")
        debugOptions()
    elif choice == 4:
        dataDriver.configWizard()
        debugOptions()
    elif choice == 5:
        dataDriver.reset()
        debugOptions()
    elif choice == 6:
        dataDriver.__resetConfig()
        debugOptions()
    elif choice == 7:
        dataDriver.validateOrders()
        orderData = dataDriver.loadOrders()
        input("Verified and reloaded orders. Press enter to continue.")
        debugOptions()
    elif choice == 8:
        dataDriver.validateConfig()
        configData = dataDriver.loadConfig()
        input("Verified and reloaded configuration. Press enter to continue.")
        debugOptions()
    elif choice == 9:
        out.printDebug("Hot reloading entire program in subshell...")
        print("--")
        exe = [sys.executable]
        for arg in sys.argv:
            exe.append(arg)
        retcode = subprocess.call(exe)
        exit(retcode)
    elif choice == 10:
        return
    else:
        print("Invalid choice. Please enter a valid choice. " + out.dim + "Press enter to continue." + out.reset, end='')
        input()
        debugOptions()

def mainMenu():
    out.clear()
    print("Welcome to the " + out.bold + parlorName + " Ordering System!" + out.reset)
    print(out.underlined + "Please choose from the following" + out.reset)
    print("1. Create a new order")
    print("2. View and modify existing orders")
    print("3. Debug options") if args.debugFlag == True else None
    print("4. Exit") if args.debugFlag == True else print("3. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a valid choice. " + out.dim + "Press enter to continue." + out.reset, end='')
        input()
        mainMenu()
    if choice == 1:
        orders.newOrder()
        dataDriver.validateOrders()
        orderData = dataDriver.loadOrders()
        input("Press enter to continue if acknowleged any errors above...") if args.debugFlag == True else None
        mainMenu()
    elif choice == 2:
        orders.viewOrders()
        mainMenu()
    elif choice == 3 and args.debugFlag == False or choice == 4 and args.debugFlag == True: 
        exit()
    elif choice == 3 and args.debugFlag == True:
        debugOptions()
        mainMenu()
    else:
        print("Invalid choice. Please enter a valid choice. " + out.dim + "Press enter to continue." + out.reset, end='')
        input()
        mainMenu()
#endregion


#region program entry point
def main():
    print(out.bold + "Welcome to " + parlorName + "!" + out.reset)
    print("Would you like to start an order?" + out.dim + " (Y/n)" + out.reset + ": ", end='') # ask user whether to start or not
    go = str(input()).lower()

    if go == "n" :
        exit()
    if not go or go == "y":
        mainMenu()
    elif go != "y" or go != "n": # fallback just in case the user doesnt understand the prompt
        print("Not y or n, assuming yes...")
        mainMenu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        out.printError("Interrupt/Ctrl-C caught, closing databases cleanly, goodbye")
        dataDriver.validateConfig()
        dataDriver.validateOrders()
        raise Exception("Debug mode enabled, raising exception for backtrace information...") if args.debugFlag == True else exit(130)
    except EOFError:
        print()
        out.printError("EOF/Ctrl-D caught, closing databases cleanly, goodbye")
        dataDriver.validateConfig()
        dataDriver.validateOrders()
        raise Exception("Debug mode enabled, raising exception for backtrace information...") if args.debugFlag == True else exit(130)
#endregion