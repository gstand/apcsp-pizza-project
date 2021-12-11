#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pizza Project - dataDriver.py - started on 8 November 2021
# Written by Garret Stand licensed under a MIT license for academic use.
# This file contains the data driver/JSON schema parser used within the program. It is a non-executable library.
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
import orders
import out

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("This is a library. This was probably ran accidentally.\nPlease execute the pizza program from the \"main.py\" program contained in the root of the project (" + dir_path + ") by running \"python3 main.py\", or open it in a text editor/IDE to see its contents and use in the program.")
    exit(1)

dir_path = os.path.dirname(os.path.realpath(__file__)) # get canonical path to python file, which is coincides with the project root, used for relative paths to data files and et cetera
indent = u'\U00000009' # unicode tabulation charecter, for use in printing data structures in debug subroutines and raw data writes when necessary (yes i use tabs)
args = argparsing.returnArgs()

def loadOrders():
    """
    This function loads the orders from the JSON file present in data/ into a list.
    """
    with open(dir_path + '/data/orders.json', 'r') as f: orders = json.load(f)
    return orders

def loadConfig():
    """
    This function loads the configuration from the JSON file present in data/ into a list.
    """
    with open(dir_path + '/data/config.json', 'r') as f: config = json.load(f)
    return config

def __listOrders(orders):
    """
    This function lists all the orders in the orders list. (used for unit tests and debugging)
    """
    for order in orders:
        out.printDebug(order + " contains: ")
        out.printDebug(indent + "Incrementor: " + orders[str(order)]["incrementor"])
        out.printDebug(indent + "Name: " + orders[str(order)]["name"])
        out.printDebug(indent + "Address: " + orders[str(order)]["address"]) if orders[str(order)]["address"] != None else out.printDebug(indent + "Address: None")
        out.printDebug(indent + "Time registered: " + str(orders[str(order)]["time"]))
        out.printDebug(indent + "Pizzas: ")
        for pizza in orders[str(order)]["pizzas"]:
            out.printDebug(indent+ indent + "Pizza: " + pizza)
            out.printDebug(indent + indent + "Size: " + orders[str(order)]["pizzas"][pizza]["size"])
            out.printDebug(indent + indent + "Toppings: ")
            for topping in orders[str(order)]["pizzas"][pizza]["toppings"]:
                out.printDebug(indent + indent + indent + topping)
        out.printDebug(indent + "Delivery?: " + str(orders[str(order)]["delivered"]))
        out.printDebug(indent + "Delivery tip: " + str(orders[str(order)]["deliveryTip"])) if orders[str(order)]["deliveryTip"] != None and orders[str(order)]["delivered"] == True else None
        if "_comment" in orders[str(order)] and orders[str(order)]["_comment"] != None: # if the order has a comment, print it
            out.printDebug(indent + "Comment: " + orders[str(order)]["_comment"])

def writeOrder(orders, name, pizzas, delivery=False, address=None, deliveryTip=None, comment=None):
    """
    This function writes the order to the orders list.
    """
    timeRegistered = time.time()
    newIncrementor = len(orders) + 1 # increment the prexisting incrementor by calculating the amount of orders present in the data +1, this is one of the two dynamically generated data fields
    orderUUID = str(uuid.uuid4()) # generate a random uuid for the order, serves as an identifier for the order and as the name of the sublist that contains said order
    order = {orderUUID: {}} # create a new sublist for the order
    order[orderUUID]["incrementor"] = str(newIncrementor)
    order[orderUUID]["name"] = name
    order[orderUUID]["time"] = timeRegistered
    order[orderUUID]["pizzas"] = pizzas
    order[orderUUID]["delivered"] = delivery
    if deliveryTip != None and deliveryTip >= 0 and delivery == True:
        order[orderUUID]["deliveryTip"] = deliveryTip
    else:
         order[orderUUID]["deliveryTip"] = 0
    if address != None and delivery == True:
        order[orderUUID]["address"] = address
    else:
        order[orderUUID]["address"] = ""
    if comment != None:
        order[orderUUID]["_comment"] = comment
    else:
        order[orderUUID]["_comment"] = ""
    orders.update(order) # update the orders list with the new order
    with open(dir_path + '/data/orders.json', 'w') as f: f.write(json.dumps(orders, indent=4)) # write the new orders list to the orders.json file
    return orderUUID

def validateOrders():
    """
    This function validates the order database just in case an irregularity appears in the database. Provides some form of self-repair.
    """
    out.printDebug("Database Validation: Validating orders...")

    try:
        orders = loadOrders()
    except:
        out.printError("Database Validation: Failed to load orders database. Reconstructing from scratch...")
        orders = {}
        with open(dir_path + '/data/orders.json', 'w') as f: f.write(json.dumps(orders, indent=4))
        return

    try:
        config = loadConfig()
    except:
        out.printError("Database Validation: Failed to load configuration database. Previous validation most likely failed. Please replace the configuration database using the included example (data/config.example.json in project root) and configure from there. Fatal error, dying...")
        exit(1)

    ordersTainted = False
    i = 0

    if orders == {}:
        out.printNotice("Database Validation: No orders present in database.", True)
        return
    for order in orders:
        i += 1
        if not "incrementor" in orders[order] or int(orders[order]["incrementor"]) != i:
            out.printError("Database Validation: Order has incorrect or missing internal incrementor (in order ID %s)." % order, True)
            newIncrementor = i
            orders[order]["incrementor"] = str(newIncrementor)
            out.printNotice("Database Validation: Order has been given a new incrementor %s (in order ID %s)." % (newIncrementor, order), True)
            ordersTainted = True
        if not "name" in orders[order]:
            out.printError("Database Validation: Name cannot be empty (in order ID %s)." % order, True)
            orders[order]["name"] = "John Doe"
            out.printNotice("Database Validation: Name set to fallback default 'John Doe' (in order ID %s)." % order, True)
            ordersTainted = True
        if not "time" in orders[order]:
            out.printError("Database Validation: Time cannot be empty (in order ID %s)." % order, True)
            orders[order]["time"] = time.time()
            out.printNotice("Database Validation: Time set to fallback default current time %s (in order ID %s)." % (time.time(), order), True)
            ordersTainted = True
        if not "pizzas" in orders[order]:
            out.printError("Database Validation: No pizzas present (in order ID %s)." % order, True)
            del orders[order]
            out.printNotice("Database Validation: Order deleted. This is an irrecoverable error." % order, True)
            ordersTainted = True
            break
        for pizza in orders[order]["pizzas"]:
            if not "size" in orders[order]["pizzas"][pizza] or not orders[order]["pizzas"][pizza]["size"] in ["small", "medium", "large"]:
                out.printError("Database Validation: Pizza size malformed or missing (in order ID %s, pizza num %s)." % (order, pizza), True)
                orders[order]["pizzas"][pizza]["size"] = "small"
                out.printNotice("Database Validation: Pizza size set to fallback default 'small' (in order ID %s, pizza num %s)." % (order, pizza), True)
                ordersTainted = True
            if not "toppings" in orders[order]["pizzas"][pizza]:
                out.printError("Database Validation: Pizza toppings missing (in order ID %s, pizza num %s)." % (order, pizza), True)
                orders[order]["pizzas"][pizza]["toppings"] = []
                out.printNotice("Database Validation: Pizza toppings set to fallback default [] (in order ID %s, pizza num %s)." % (order, pizza), True)
                ordersTainted = True
            for topping in orders[order]["pizzas"][pizza]["toppings"]:
                if not topping in config["toppings"]:
                    out.printError("Database Validation: Incorrect pizza topping (in order ID %s, pizza num %s, topping %s)." % (order, pizza, topping), True)
                    orders[order]["pizzas"][pizza]["toppings"].remove(topping)
                    out.printNotice("Database Validation: Pizza topping removed (in order ID %s, pizza num %s, topping %s)." % (order, pizza, topping), True)
                    ordersTainted = True
        if not "delivered" in orders[order]:
            out.printError("Database Validation: Delivery was not specified (in order ID %s)." % order, True)
            orders[order]["delivered"] = False
            out.printNotice("Database Validation: Delivery set to fallback default 'False' (in order ID %s)." % order, True)
            ordersTainted = True
        if not "address" in orders[order] and orders[order]["delivered"] == True:
            out.printError("Database Validation: Delivery address was not specified (in order ID %s)." % order, True)
            orders[order]["address"] = "123 Main St."
            out.printNotice("Database Validation: Delivery address set to fallback default '123 Main St.' (in order ID %s)." % order, True)
            ordersTainted = True
        if not "deliveryTip" in orders[order] and orders[order]["delivered"] == True:
            out.printError("Database Validation: Delivery tip was not specified (in order ID %s)." % order, True)
            orders[order]["deliveryTip"] = 0
            out.printNotice("Database Validation: Delivery tip set to fallback default '0' (in order ID %s)." % order, True)
            ordersTainted = True
        if orders[order]["deliveryTip"] != None and orders[order]["delivered"] == False:
            out.printError("Database Validation: Delivery tip specified but order was not marked as delivery (in order ID %s)." % order, True)
            orders[order]["deliveryTip"] = None
            out.printNotice("Database Validation: Delivery tip set to logical fallback None (in order ID %s)." % order, True)
            ordersTainted = True
    if ordersTainted == True:
        with open(dir_path + '/data/orders.json', 'w') as f: f.write(json.dumps(orders, indent=4))
        out.printNotice("Database Validation: Errors were found in the order database, however, they were repaired.")
    elif ordersTainted == False:
        out.printDebug("Database Validation: No issues found.")

def validateConfig():
    """
    This function validates the configuration store just in case an irregularity appears in said store. See validateOrders(). Provides some form of self-repair.
    """
    out.printDebug("Database Validation: Validating configuration store...")

    defaultConfig = {'parlorName': 'Some Pizza Place', 'taxRate': 6.0, 'deliveryFee': 5, 'sizeCosts': {'small': 6.0, 'medium': 8.0, 'large': 10.0}, 'toppings<=3': 1.5, 'toppings>=4': 1.0, 'toppings': ['pepperoni', 'anchovies', 'sausage', 'mushrooms', 'onions', 'green peppers', 'pineapple', 'olives']}
    configTainted = False

    try:
        config = loadConfig()
    except:
        out.printError("Database Validation: Failed to load configuration database. Restoring to hardcoded defaults...")
        config = defaultConfig
        with open(dir_path + '/data/config.json', 'w') as f: f.write(json.dumps(config, indent=4))
        return
    

    if config == {}:
        out.printError("Database Validation: No config present in database. Restoring to hardcoded defaults. (see data/config.example.json)")
        config = defaultConfig
        with open(dir_path + '/data/config.json', 'w') as f: f.write(json.dumps(config, indent=4))
        return
    if not "parlorName" in config:
        out.printError("Database Validation: Parlor name missing in configuration store.")
        config["parlorName"] = defaultConfig["parlorName"]
        out.printNotice("Database Validation: Parlor name set to fallback default %s." % defaultConfig["parlorName"], True)
        configTainted = True
    if not "taxRate" in config:
        out.printError("Database Validation: Tax rate missing in configuration store.")
        config["taxRate"] = defaultConfig["taxRate"]
        out.printNotice("Database Validation: Tax rate set to fallback default %s." % defaultConfig["taxRate"], True)
        configTainted = True
    if not "deliveryFee" in config:
        out.printError("Database Validation: Delivery fee missing in configuration store.")
        config["deliveryFee"] = defaultConfig["deliveryFee"]
        out.printNotice("Database Validation: Delivery fee set to fallback default %s." % defaultConfig["deliveryFee"], True)
        configTainted = True
    if not "sizeCosts" in config:
        out.printError("Database Validation: Size costs missing in configuration store.")
        config["sizeCosts"] = defaultConfig["sizeCosts"]
        out.printNotice("Database Validation: Size costs set to fallback default %s." % defaultConfig["sizeCosts"], True)
        configTainted = True
    if not "small" in config["sizeCosts"] or type(config["sizeCosts"]["small"]) != float:
        out.printError("Database Validation: Small size cost missing in configuration store.")
        config["sizeCosts"]["small"] = defaultConfig["sizeCosts"]["small"]
        out.printNotice("Database Validation: Small size cost set to fallback default %s." % defaultConfig["sizeCosts"]["small"], True)
        configTainted = True
    if not "medium" in config["sizeCosts"] or type(config["sizeCosts"]["medium"]) != float:
        out.printError("Database Validation: Medium size cost missing in configuration store.")
        config["sizeCosts"]["medium"] = defaultConfig["sizeCosts"]["medium"]
        out.printNotice("Database Validation: Medium size cost set to fallback default %s." % defaultConfig["sizeCosts"]["medium"], True)
        configTainted = True
    if not "large" in config["sizeCosts"] or type(config["sizeCosts"]["large"]) != float:
        out.printError("Database Validation: Large size cost missing in configuration store.")
        config["sizeCosts"]["large"] = defaultConfig["sizeCosts"]["large"]
        out.printNotice("Database Validation: Large size cost set to fallback default %s." % defaultConfig["sizeCosts"]["large"], True)
        configTainted = True
    if not "toppings<=3" in config:
        out.printError("Database Validation: Toppings cost for up to 3 toppings missing in configuration store.")
        config["toppings<=3"] = defaultConfig["toppings<=3"]
        out.printNotice("Database Validation: Toppings cost for up to 3 toppings set to fallback default %s." % defaultConfig["toppings<=3"], True)
        configTainted = True
    if not "toppings>=4" in config:
        out.printError("Database Validation: Toppings cost for 4+ toppings missing in configuration store.")
        config["toppings>=4"] = defaultConfig["toppings>=4"]
        out.printNotice("Database Validation: Toppings cost for 4+ toppings set to fallback default %s." % defaultConfig["toppings>=4"], True)
        configTainted = True
    if not "toppings" in config:
        out.printError("Database Validation: No toppings present in configuration store.", True)
        config["toppings"] = defaultConfig["toppings"]
        out.printNotice("Database Validation: Toppings set to fallback default %s." % defaultConfig["toppings"], True)
        configTainted = True
    if configTainted == True:
        with open(dir_path + '/data/config.json', 'w') as f: f.write(json.dumps(config, indent=4))
        out.printNotice("Database Validation: Errors were found in the configuration store, however, they were repaired.")
    elif configTainted == False:
        out.printDebug("Database Validation: No issues found.")

def configWizard():
    '''
    This function provides the configuration wizard, enabled by entering -c on the command line.
    '''
    out.clear()
    print(out.bold + "  Pizza Ordering System configuration wizard" + out.reset + "\n══════════════════════════════════════════════")
    
    configFile = dir_path + '/data/config.json'

    try:
        config = loadConfig()
    except:
        config = {}
    
    if not "parlorName" in config:
        print("Please select a parlor name " + out.dim + "[Some Pizza Place]" + out.reset + ": ", end='')
        defaultPN = "Some Pizza Place"
    else: 
        print("Please select a parlor name " + out.dim + "[" + config["parlorName"] + "]" + out.reset + ": ", end='')
        defaultPN = config["parlorName"]
    toBePN = input()
    if not "taxRate" in config:
        print("Please select a tax rate (e.x. 2.75 would be 2.75%) " + out.dim + "[6]" + out.reset + ": ", end='')
        defaultTR = 6
    else: 
        print("Please select a tax rate (e.x. 2.75 would be 2.75%) " + out.dim + "[" + str(config["taxRate"]) + "]" + out.reset + ": ", end='')
        defaultTR = config["taxRate"]
    toBeTR = input()
    if not "deliveryFee" in config:
        print("Please select a delivery fee (e.x. 5 would be $5) " + out.dim + "[5]" + out.reset + ": ", end='')
        defaultDF = 5
    else: 
        print("Please select a delivery fee (e.x. 5 would be $5) " + out.dim + "[" + str(config["deliveryFee"]) + "]" + out.reset + ": ", end='')
        defaultDF = config["deliveryFee"]
    toBeDF = input()
    print(out.underlined + "Pizza size cost setup" + out.reset)
    if not "sizeCosts" in config:
        config["sizeCosts"] = {}
    sizeCosts = config["sizeCosts"] 
    if not "small" in sizeCosts:
        print("Please select the cost of a small pizza (e.x. 5 would be $5) " + out.dim + "[6]" + out.reset + ": ", end='')
        defaultSC = 6
    else:
        print("Please select the cost of a small pizza (e.x. 5 would be $5) " + out.dim + "[" + str(sizeCosts["small"]) + "]" + out.reset + ": ", end='')
        defaultSC = sizeCosts["small"]
    toBeSC = input()
    if not "medium" in sizeCosts:
        print("Please select the cost of a medium pizza (e.x. 5 would be $5) " + out.dim + "[8]" + out.reset + ": ", end='')
        defaultMC = 8
    else:
        print("Please select the cost of a medium pizza (e.x. 5 would be $5) " + out.dim + "[" + str(sizeCosts["medium"]) + "]" + out.reset + ": ", end='')
        defaultMC = sizeCosts["medium"]
    toBeMC = input()
    if not "large" in sizeCosts:
        print("Please select the cost of a large pizza (e.x. 5 would be $5) " + out.dim + "[10]" + out.reset + ": ", end='')
        defaultLC = 10
    else:
        print("Please select the cost of a large pizza (e.x. 5 would be $5) " + out.dim + "[" + str(sizeCosts["large"]) + "]" + out.reset + ": ", end='')
        defaultLC = sizeCosts["large"]
    toBeLC = input()
    print(out.underlined + "Pizza toppings and related cost setup" + out.reset)
    if not "toppings<=3" in config:
        print("Please select the cost of toppings up to 3 (e.x. 5 would be $5) " + out.dim + "[1.50]" + out.reset + ": ", end='')
        defaultT3 = 1.50
    else:
        print("Please select the cost of toppings up to 3 (e.x. 5 would be $5) " + out.dim + "[" + str(config["toppings<=3"]) + "]" + out.reset + ": ", end='')
        defaultT3 = config["toppings<=3"]
    toBeT3 = input()
    if not "toppings>=4" in config:
        print("Please select the cost of toppings over 3 (e.x. 5 would be $5) " + out.dim + "[1.00]" + out.reset + ": ", end='')
        defaultT4 = 1.00
    else:
        print("Please select the cost of toppings over 3 (e.x. 5 would be $5) " + out.dim + "[" + str(config["toppings>=4"]) + "]" + out.reset + ": ", end='')
        defaultT4 = config["toppings>=4"]
    toBeT4 = input()
    if not "toppings" in config or config["toppings"] == {}:
        print("Please specify a list of toppings to offer seperated by commas " + out.dim + "[pepperoni, anchovies, sausage, mushrooms, onions, green peppers, pineapple, olives]" + out.reset + ": ", end='')
        defaultT = ["pepperoni", "anchovies", "sausage", "mushrooms", "onions", "green peppers", "pineapple", "olives"]
    else:
        print("Please specify a list of toppings to offer seperated by commas " + out.dim + "[" + str(config["toppings"])[1:len(str(config["toppings"]))-1].replace("'", "") + "]" + out.reset + ": ", end='')
        defaultT = config["toppings"]
    toBeT = list(map(str, input().split(', '))) 
    print(out.blink + "Processing values..." + out.reset)
    config["parlorName"] = str(toBePN) if toBePN != "" else defaultPN
    config["taxRate"] = float(toBeTR) if toBeTR != "" else defaultTR
    config["deliveryFee"] = float(toBeDF) if toBeDF != "" else defaultDF
    config["sizeCosts"]["small"] = float(toBeSC) if toBeSC != "" else defaultSC
    config["sizeCosts"]["medium"] = float(toBeMC) if toBeMC != "" else defaultMC
    config["sizeCosts"]["large"] = float(toBeLC) if toBeLC != "" else defaultLC
    config["toppings<=3"] = float(toBeT3) if toBeT3 != "" else defaultT3
    config["toppings>=4"] = float(toBeT4) if toBeT4 != "" else defaultT4
    config["toppings"] = toBeT if toBeT != [''] else defaultT
    out.clear()
    print(out.bold + "  Pizza Ordering System configuration wizard" + out.reset + "\n══════════════════════════════════════════════")
    print(out.bold + "Final values" + out.reset)
    print(out.bold+ "Parlor name: " + out.reset + config["parlorName"])
    print(out.bold+ "Tax rate: " + out.reset + str(config["taxRate"]) + "%")
    print(out.bold+ "Delivery fee: " + out.reset + "$" + str(config["deliveryFee"]))
    print(out.bold+ "Small pizza cost: " + out.reset + "$" + str(config["sizeCosts"]["small"]))
    print(out.bold+ "Medium pizza cost: " + out.reset + "$" + str(config["sizeCosts"]["medium"]))
    print(out.bold+ "Large pizza cost: " + out.reset + "$" + str(config["sizeCosts"]["large"]))
    print(out.bold+ "Toppings up to 3 cost: " + out.reset + "$" + str(config["toppings<=3"]))
    print(out.bold+ "Toppings over 3 cost: " + out.reset + "$" + str(config["toppings>=4"]))
    print(out.bold+ "Toppings: " + out.reset + str(config["toppings"]))
    print("Is this correct? " + out.dim + "[Y/n]" + out.reset + ": ", end='')
    response = str(input())
    if response.lower() == "y" or response.lower() == "":
        print(out.blink + "Saving values..." + out.reset)
        with open(configFile, 'w') as configFile:
            configFile.write(json.dumps(config, indent=4))
        print(out.bold + "Values saved!" + out.reset)
    elif response.lower() == "n":
        print(out.bold + "Starting over..." + out.reset)
        configWizard()
    else:
        print(out.bold + "Invalid response, assuming yes..." + out.reset)
        with open(configFile, 'w') as configFile:
            configFile.write(json.dumps(config, indent=4))
        print(out.bold + "Values saved!" + out.reset)
    
def reset():
    '''
    Resets the order database and deletes all past orders.
    '''
    ordersFile = dir_path + '/data/orders.json'

    print(out.bold + "Are you sure you want to delete all orders from the order database? This action is irreversable." + out.reset + out.dim + "[y/N] ", end='')
    response = str(input())
    if response.lower() == "y":
        print(out.blink + "Resetting values..." + out.reset)
        with open(ordersFile, 'w') as configFile:
            configFile.write("{}")
        print(out.bold + "Values reset!" + out.reset)
    else:
        print(out.bold + "Aborted." + out.reset)

def __resetConfig():
    '''
    Resets the configuration store file at data/config.json to default values.
    '''
    configFile = dir_path + '/data/config.json'
    defaultConfig = {'parlorName': 'Some Pizza Place', 'taxRate': 6.0, 'deliveryFee': 5, 'sizeCosts': {'small': 6.0, 'medium': 8.0, 'large': 10.0}, 'toppings<=3': 1.5, 'toppings>=4': 1.0, 'toppings': ['pepperoni', 'anchovies', 'sausage', 'mushrooms', 'onions', 'green peppers', 'pineapple', 'olives']}
    print(out.bold + "Are you sure you want to reset the configuration store to the hardcoded defaults? This action is irreversable." + out.reset + out.dim + "[y/N] ", end='')
    response = str(input())
    if response.lower() == "y":
        print(out.blink + "Resetting values..." + out.reset)
        with open(ordersFile, 'w') as configFile:
            configFile.write(json.dumps(defaultConfig, indent=4))
        print(out.bold + "Values reset!" + out.reset)
    else:
        print(out.bold + "Aborted." + out.reset)