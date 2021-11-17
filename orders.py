#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pizza Project - main.py - started on 8 November 2021
# Written by Garret Stand licensed under a MIT license for academic use.
# This file contains the ordering subroutines used within the program. It is a non-executable library.
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
import out

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("This is a library. This was probably ran accidentally.\nPlease execute the pizza program from the \"main.py\" program contained in the root of the project (" + dir_path + ") by running \"python3 main.py\", or open it in a text editor/IDE to see its contents and use in the program.")
    exit(1)

def priceTable():
    configData = dataDriver.loadConfig()
    out.clear()
    smallPizza = "{:.2f}".format(configData['sizeCosts']['small'])
    smallAlign = ""
    smallAlignN = 8-len(str(smallPizza))
    for i in range(smallAlignN):
        smallAlign = smallAlign + " "
    mediumPizza = "{:.2f}".format(configData['sizeCosts']['medium'])
    mediumAlign = ""
    mediumAlignN = 7-len(str(mediumPizza))
    for i in range(mediumAlignN):
        mediumAlign = mediumAlign + " "
    largePizza = "{:.2f}".format(configData['sizeCosts']['large'])
    largeAlign = ""
    largeAlignN = 8-len(str(largePizza))
    for i in range(largeAlignN):
        largeAlign = largeAlign + " "
    top3 = "{:.2f}".format(configData['toppings<=3'])
    top4 = "{:.2f}".format(configData['toppings>=4'])
    taxRate = str(configData['taxRate']) + "%"
    taxRateAlign = ""
    taxRateAlignN = 18-len(taxRate)
    for i in range(taxRateAlignN):
        taxRateAlign = taxRateAlign + " "
    deliveryFee = "{:.2f}".format(configData['deliveryFee'])
    print('''╭───────────────────────────────────────────────────────────────────╮
│                        %s%sPizza Pricing Guide%s                        │
╰───────────────────────────────────────────────────────────────────╯
╭──────────────────╮ ╭──────────────────╮ ╭─────────────────────────╮
│   %s%sPizza Sizes:%s   │ │  %s%sTopping Costs:%s  │ │       %s%sOther fees:%s       │ 
├──────────────────┤ ├──────────────────┤ ├─────────────────────────┤ 
│ Small: $%s%s │ │ 1-3 tops.: $%s │ │ Tax: %s%s │
│ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │ │ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │ │ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │
│ Medium: $%s%s │ │ 4+ tops.: $%s  │ │ Delivery fee: $%s     │
│ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │ ╰──────────────────╯ │ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │
│ Large: $%s%s │                      │ Delivery tips accepted. │
│ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ │                      ╰─────────────────────────╯
│ All pizzas incl. │
│ cheese as a top. │
╰──────────────────╯''' % (out.green, out.bold, out.reset, out.red, out.bold, out.reset, out.red, out.bold, out.reset, out.red, out.bold, out.reset, smallPizza, smallAlign, top3, taxRate, taxRateAlign, mediumPizza, mediumAlign, top4, deliveryFee, largePizza, largeAlign))
    print(out.dim + "Press enter to return to the ordering system... " + out.reset, end='')
    input()
    out.clear()

def newOrder():
    configData = dataDriver.loadConfig()
    out.clear()
    print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
    print(out.dim + "You may type \"price\" at any time to list relevant prices for the current field" + out.reset)
    print("Please enter your name " + out.dim + "[John Doe]" + out.reset + ": ", end='')
    orderName = str(input())
    if orderName == "": orderName = "John Doe"
    incrementor = 1
    pizzas = {}
    while decision == "n" or decision == "":
        out.clear()
        print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
        print(out.dim + "You may type \"price\" at any time to list relevant prices for the current field" + out.reset)
        print(out.bold + "Pizza " + str(incrementor) + out.reset + ":")
        while selected != True:
            print("Please enter the size of the pizza " + out.dim + "[S/m/l/prices]" + out.reset + ": ", end='')
            pizzaSize = str(input()).lower()
            pizzaInput = pizzaSize
            if pizzaSize == "prices":
                priceTable()
                print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
                print(out.dim + "You may type \"price\" at any time to list relevant prices for the current field" + out.reset)
                print(out.bold + "Pizza " + str(incrementor) + out.reset + ":")
                continue
            if pizzaSize == "": 
                pizzaSize = "small"
                selected = True
            elif pizzaSize == "s" or pizzaSize == "small": 
                pizzaSize = "small"
                selected = True
            elif pizzaSize == "m" or pizzaSize == "medium": 
                pizzaSize = "medium"
                selected = True
            elif pizzaSize == "l" or pizzaSize == "large": 
                pizzaSize = "large"
                selected = True
            else:
                out.printError("Invalid input. Please select a size listed using S, M, or L. Press enter to continue.")
                input()
                out.clear()
                print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
                print(out.dim + "You may type \"price\" at any time to list relevant prices for the current field" + out.reset)
                print(out.bold + "Pizza " + str(incrementor) + out.reset + ":")
                continue
        selected = False
        while selected != True:
            print("Please enter any toppings you want, seperated by commas, or put nothing for just cheese. " + out.dim + "[" + str(configData["toppings"])[1:len(str(configData["toppings"]))-1].replace("'", "") + ", prices]" + out.reset + ": ", end='')
            toppingInput = input()
            pizzaToppings = list(map(str, toppingInput.split(', '))) 
            conflicts = list(set(pizzaToppings) - set(configData["toppings"]))
            if pizzaToppings == ['prices']:
                priceTable()
                print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
                print(out.dim + "You may type \"price\" at any time to list relevant prices for the current field" + out.reset)
                print(out.bold + "Pizza " + str(incrementor) + out.reset + ":")
                print("Please enter the size of the pizza " + out.dim + "[S/m/l/prices]" + out.reset + ": " + pizzaInput)
                continue
            if pizzaToppings == ['']: 
                pizzaToppings = "cheese"
                selected = True
            elif conflicts != ['']:
                out.printError("Invalid input. Please select toppings listed using the following: " + str(configData["toppings"])[1:len(str(configData["toppings"]))-1].replace("'", ""))
                input()
                out.clear()
                print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
                print(out.dim + "You may type \"price\" at any time to list relevant prices for the current field" + out.reset)
                print(out.bold + "Pizza " + str(incrementor) + out.reset + ":")
                print("Please enter the size of the pizza " + out.dim + "[S/m/l/prices]" + out.reset + ": " + pizzaInput)
                continue
            else:
                selected = True
        pizza = {"size": pizzaSize, "toppings": pizzaToppings}
        pizzas[str(incrementor)] = pizza
        incrementor += 1
        print("Would you like to order another pizza?" + out.dim + "[y/N]" + out.reset + ": ", end='')
        decision = str(input()).lower()
    out.clear()
    print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
    print("Would you like this order delivered? It will cost " + out.bold + "$" + str(configData["deliveryFee"]) + out.reset + "." + out.dim + "[y/N]" + out.reset + ": ", end='')
    delivery = str(input()).lower()
    if delivery == "y":
        delivery = True
    else:
        delivery = False
    if delivery == True:
        print("Would you like to give the driver a tip? " + out.dim + "[y/N]" + out.reset + ": ", end='')
        tip = str(input()).lower()
        if tip == "y":
            print("Please enter the tip amount" + out.dim + "[5.25 would be $5.25]" + out.reset + ": ", end='')
            tip = float(input())
        else:
            tip = None
    if args.debugFlag == True:
        out.clear()
        print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
        print("Debug flag enabled; would you like to make an internal comment for the order? " + out.dim + "It will be ignored on order viewing and will only be present in the JSON database. [y/N]" + out.reset + ": ", end='')
        comment = str(input()).lower()
        if comment == "y":
            print("Please enter the comment: ", end='')
            comment = str(input())
        else:
            comment = None
    dataDriver.writeOrder(dataDriver.loadOrders(), orderName, pizzas, delivery, tip, comment)
    out.clear() 
    print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
    print("Order created successfully! Summary:")
    print("Name: " + out.bold + orderName + out.reset)
    print("Pizzas:")
    for pizza in pizzas:
        print("\t" + pizza + ": " + pizzas[pizza]["size"] + " pizza with " + ", ".join(pizzas[pizza]["toppings"]))
    print("The order will" + "not" if delivery == False else "" + " be delivered.")
    if delivery == True:
        print("The driver will" + "not" if tip == None else "" + " be given a tip" + ("of $" + tip) if tip != None else "" + ".")
    if args.debugFlag == True:
        out.printDebug("Internal comment: " + comment)
        out.printDebug("Dumping internal content structures: ")
        out.printDebug(dataDriver.loadOrders())
        dataDriver.__listOrders(orders=dataDriver.loadOrders())
    print("Does this look correct to you?" + out.dim + "[Y/n]" + out.reset + ": ", end='')
    decision = str(input()).lower()
    if decision == "n":
        newOrder()
    out.clear()
    print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
    print("Checkout:")
    for pizza in pizzas:
        price = float(0)
        if pizza["size"] == "small":
            price = price + float(configData["smallPrice"])
        elif pizza["size"] == "medium":
            price = price + float(configData["mediumPrice"])
        elif pizza["size"] == "large":
            price = price + float(configData["largePrice"])
        if len(pizza["toppings"]) > 3:
            for i in range(3):
                price = price + float(configData["toppings<=3"])
            for i in range(len(pizza["toppings"]) - 3):
                price = price + float(configData["toppings>=4"])
        else:
            for i in range(len(pizza["toppings"])):
                price = price + float(configData["toppings<=3"])
        print("Pizza " + pizza + ": " + pizzas[pizza]["size"] + " pizza with " + ", ".join(pizzas[pizza]["toppings"]) + " - " + out.bold + "$" + str(price) + out.reset)
        
