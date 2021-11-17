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
# DEVNOTE: import all external libraries/dependencies above this line, and all internal libraries/dependencies below this line
import orders
import out

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("This is a library. This was probably ran accidentally.\nPlease execute the pizza program from the \"main.py\" program contained in the root of the project (" + dir_path + ") by running \"python3 main.py\", or open it in a text editor/IDE to see its contents and use in the program.")
    exit(1)

dir_path = os.path.dirname(os.path.realpath(__file__)) # get canonical path to python file, which is coincides with the project root, used for relative paths to data files and et cetera
indent = u'\U00000009' # unicode tabulation charecter, for use in printing data structures in debug subroutines and raw data writes when necessary (yes i use tabs)

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
        print(order + " contains: ")
        print(indent + "Incrementor: " + orders[str(order)]["incrementor"])
        print(indent + "Name: " + orders[str(order)]["name"])
        print(indent + "Pizzas: ")
        for pizza in orders[str(order)]["pizzas"]:
            print(indent+ indent + "Pizza: " + pizza)
            print(indent + indent + "Size: " + orders[str(order)]["pizzas"][pizza]["size"])
            print(indent + indent + "Toppings: ")
            for topping in orders[str(order)]["pizzas"][pizza]["toppings"]:
                print(indent + indent + indent + topping)
        print(indent + "Delivery?: " + str(orders[str(order)]["delivered"]))
        print(indent + "Delivery tip: " + str(orders[str(order)]["deliveryTip"])) if orders[str(order)]["deliveryTip"] != None and orders[str(order)]["delivered"] == True else None
        if "_comment" in orders[str(order)]: # if the order has a comment, print it
            print(indent + "Comment: " + orders[str(order)]["_comment"])

def generatePizzaObject(size, toppings):
    """
    This function generates a pizza object.
    """
    pizza = {}
    pizza["size"] = size
    pizza["toppings"] = toppings
    return pizza

def generatePizzaListObject(*arg):
    pizzas = {}
    incrementor = 0
    for pizza in arg:
        incrementor += 1
        pizzas[str(incrementor)] = pizza
    return pizzas

def generateOrderObject(name, pizzas):
    """
    This function generates an order object. (used for unit tests and debugging)
    """
    order = {}
    order["name"] = name
    order["pizzas"] = pizzas
    return order

def writeOrder(orders, name, pizzas, delivery=False, deliveryTip=None, comment=None):
    """
    This function writes the order to the orders list.
    """
    newIncrementor = len(orders) + 1 # increment the prexisting incrementor by calculating the amount of orders present in the data +1, this is one of the two dynamically generated data fields
    orderUUID = str(uuid.uuid4()) # generate a random uuid for the order, serves as an identifier for the order and as the name of the sublist that contains said order
    order = {orderUUID: {}} # create a new sublist for the order
    order[orderUUID]["incrementor"] = str(newIncrementor)
    order[orderUUID]["name"] = name
    order[orderUUID]["pizzas"] = pizzas
    order[orderUUID]["delivered"] = delivery
    if deliveryTip >= 0 and delivery == True:
        order[orderUUID]["deliveryTip"] = deliveryTip
    else:
         order[orderUUID]["deliveryTip"] = None
    order[orderUUID]["_comment"] = comment
    orders.update(order) # update the orders list with the new order
    ordersTBW = json.dump(orders, indent=4) # convert from dictionary to JSON

    with open(dir_path + '/data/orders.json', 'w') as f: f.write(ordersTBW) # write the new orders list to the orders.json file

def validateOrders():
    """
    This function validates the order database just in case an irregularity appears in the database. Provides some form of self-repair.
    """
    out.printDebug("Database Validation: Validating orders...")

    orders = loadOrders()
    config = loadConfig()

    if orders == {}:
        out.printNotice("Database Validation: No orders present in database.")
        return
    for order in orders:
        if not "incrementor" in order:
            out.printError("Database Validation: Order has no internal incrementor (in order ID %s)." % order, True)
            newIncrementor = len(orders) + 1
            orders[order]["incrementor"] = str(newIncrementor)
            out.printNotice("Database Validation: Order has been given a new incrementor %s (in order ID %s)." % (newIncrementor, order), True)
            ordersTainted = True
        if not "name" in order:
            out.printNotice("Database Validation: Name cannot be empty (in order ID %s)." % order, True)
            orders[order]["name"] = "John Doe"
            out.printNotice("Database Validation: Name set to fallback default 'John Doe' (in order ID %s)." % order, True)
            ordersTainted = True
        if not pizzas in order:
            out.printNotice("Database Validation: No pizzas present (in order ID %s)." % order, True)
            del orders[order]
            out.printNotice("Database Validation: Order deleted. This is an irrecoverable error." % order, True)
            ordersTainted = True
            break
        for pizza in pizzas:
            if not "size" in pizza or pizza["size"] != ["small", "medium", "large"]:
                out.printNotice("Database Validation: Pizza size malformed or missing (in order ID %s, pizza num %s)." % (order, pizza), True)
                pizza["size"] = "small"
                out.printNotice("Database Validation: Pizza size set to fallback default 'small' (in order ID %s, pizza num %s)." % (order, pizza), True)
                ordersTainted = True
            if not "toppings" in pizza or pizza["toppings"] != config["toppings"]:
                out.printNotice("Database Validation: Pizza toppings malformed or missing (in order ID %s, pizza num %s)." % (order, pizza), True)
                pizza["toppings"] = ["cheese"]
                out.printNotice("Database Validation: Pizza toppings set to fallback default ['cheese'] (in order ID %s, pizza num %s)." % (order, pizza), True)
                ordersTainted = True
        if not "delivered" in order:
            out.printNotice("Database Validation: Delivery was not specified (in order ID %s)." % order, True)
            orders[order]["delivered"] = False
            out.printNotice("Database Validation: Delivery set to fallback default 'False' (in order ID %s)." % order, True)
            ordersTainted = True
        if not "deliveryTip" in order and orders["delivered"] == True:
            out.printNotice("Database Validation: Delivery tip was not specified (in order ID %s)." % order, True)
            orders[order]["deliveryTip"] = 0
            out.printNotice("Database Validation: Delivery tip set to fallback default '0' (in order ID %s)." % order, True)
            ordersTainted = True
        if order["deliveryTip"] != None and order["delivered"] == False:
            out.printNotice("Database Validation: Delivery tip specified but order was not marked as delivery (in order ID %s)." % order, True)
            orders[order]["deliveryTip"] = None
            out.printNotice("Database Validation: Delivery tip set to logical fallback None (in order ID %s)." % order, True)
            ordersTainted = True
    if ordersTainted == True:
        with open(dir_path + '/data/orders.json', 'w') as f: f.write(json.dumps(orders, indent=4))
        out.printNotice("Database Validation: Errors were found in the order database, however, they were repaired.")
    elif ordersTainted == False:
        out.printDebug("Database Validation: No issues found.", True)

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
            configFile.write(json.dumps(config))
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
