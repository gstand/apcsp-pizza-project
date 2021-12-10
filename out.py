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
import fpdf
import time
import subprocess
# DEVNOTE: import all external libraries/dependencies above this line, and all internal libraries/dependencies below this line
import argparsing
import dataDriver
import orders

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("This is a library. This was probably ran accidentally.\nPlease execute the pizza program from the \"main.py\" program contained in the root of the project (" + dir_path + ") by running \"python3 main.py\", or open it in a text editor/IDE to see its contents and use in the program.")
    exit(1)

args = argparsing.returnArgs()

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
    '''
    Prints an error to the console with an optional debug check
    '''
    if debug:
        print(errorBG + "[ERROR]" + reset + " " + text) if args.debugFlag else None
    else:
        print(errorBG + "[ERROR]" + reset + " " + text)

def printNotice(text, debug=False):
    '''
    Prints a warning to the console with an optional debug check
    '''
    if debug:
        print(noticeBG + "[NOTICE]" + reset + " " + text) if args.debugFlag else None
    else:
        print(noticeBG + "[NOTICE]" + reset + " " + text)
    
def printDebug(text):
    '''
    Prints debug text to the console if the debug flag is set
    '''
    print(debugBG + "[DEBUG]" + reset + " " + text) if args.debugFlag else None

def clear():
    '''
    Platform agnostic screen clear
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

def generateReceipt(order):
    '''
    Generates a receipt for a given order.
    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    configData = dataDriver.loadConfig()
    header = '*'
    for i in range(len(configData['parlorName'])+8):
        header += '*'
    header += '''*
*    ''' + configData['parlorName'] + '''    *
*'''
    for i in range(len(configData['parlorName'])+8):
        header += '*'
    header += '*'
    headerLines = header.splitlines() 
    receipt = fpdf.FPDF()
    receipt.add_page()
    receipt.add_font('receiptFont', '', dir_path + '/data/receiptFont.ttf', uni=True)
    receipt.set_font("receiptFont", size = 10)
    for x in headerLines:
        receipt.cell(200, 10, txt=x, ln=1, align='C')
    receipt.cell(200, 10, txt="Pizza Receipt", ln=1, align="C")
    receipt.cell(200, 10, txt="Time ordered: " + time.ctime(order["time"]), ln=1, align="C")
    receipt.cell(200, 10, txt="--", ln=1, align="C")
    receipt.cell(200, 10, txt="Order Items:", ln=1, align="C")
    subTotal = 0
    for pizza in order["pizzas"]:
        price = float(0)
        if order["pizzas"][pizza]["size"] == "small":
            price = price + float(configData["sizeCosts"]["small"])
        elif order["pizzas"][pizza]["size"] == "medium":
            price = price + float(configData["sizeCosts"]["medium"])
        elif order["pizzas"][pizza]["size"] == "large":
            price = price + float(configData["sizeCosts"]["large"])
        if len(order["pizzas"][pizza]["toppings"]) > 3:
            for i in range(3):
                price = price + float(configData["toppings<=3"])
            for i in range(len(order["pizzas"][pizza]["toppings"]) - 3):
                price = price + float(configData["toppings>=4"])
        else:
            for i in range(len(order["pizzas"][pizza]["toppings"])):
                price = price + float(configData["toppings<=3"])
        line = "   Pizza " + pizza + ": " + order["pizzas"][pizza]["size"] + " pizza with " + "cheese, " + str(order["pizzas"][pizza]["toppings"])[1:len(str(order["pizzas"][pizza]["toppings"]))-1].replace("'", "") + " | $" + "{:.2f}".format(price) if order["pizzas"][pizza]["toppings"] != [''] else "   Pizza " + pizza + ": " + order["pizzas"][pizza]["size"] + " pizza with cheese | $" + "{:.2f}".format(price)
        receipt.cell(200, 10, txt=line, ln=1, align="L")
        subTotal = subTotal + price
    receipt.cell(200, 10, txt="Subtotal: $" + str(subTotal), ln=1, align="L")
    tax = subTotal * float(configData["taxRate"]/100)
    receipt.cell(200, 10, txt="Tax: $" + "{:.2f}".format(tax), ln=1, align="L")
    total = subTotal + tax
    receipt.cell(200, 10, txt="Total: $" + "{:.2f}".format(total), ln=1, align="L")
    receipt.cell(200, 10, txt="--", ln=1, align="C")
    if order["delivered"] == True:
        price = float(configData["deliveryFee"])
        receipt.cell(200, 10, txt="Delivery Fee: $" + "{:.2f}".format(price), ln=1, align="L")
        if order["deliveryTip"] != None:
            price = price + order["deliveryTip"]
            receipt.cell(200, 10, txt="Tip: $" + "{:.2f}".format(order["deliveryTip"]), ln=1, align="L")
        grandTotal = total + price
    else:
        receipt.cell(200, 10, txt="Delivery Fee: $0.00 (not delivery)", ln=1, align="L")
        grandTotal = total
    receipt.cell(200, 10, txt="Grand Total: $" + "{:.2f}".format(grandTotal), ln=1, align="L")
    receipt.cell(200, 10, txt="--", ln=1, align="C")
    receipt.cell(200, 10, txt="Order info:", ln=1, align="C")
    receipt.cell(200, 10, txt="Name: " + order["name"], ln=1, align="L")
    if order["delivered"] == True:
        receipt.cell(200, 10, txt="Delivery: Yes", ln=1, align="L")
        receipt.cell(200, 10, txt="Address: " + order["address"], ln=1, align="L")
    else:
        receipt.cell(200, 10, txt="Delivery: No", ln=1, align="L")
        receipt.cell(200, 10, txt="Address: 123 Parlor St. for pickup", ln=1, align="L")
    receipt.cell(200, 10, txt="--", ln=1, align="C")
    receipt.cell(200, 10, txt="Thank you for your order!", ln=1, align="L")
    receipt.output("receipt.pdf")
    print("Receipt generated! Openining in system default PDF viewer...")
    input()
    subprocess.Popen(["open receipt.pdf"], shell=True) # macOS now at the moment, time constratints :/