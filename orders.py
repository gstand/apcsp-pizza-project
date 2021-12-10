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
import fpdf
import time
import subprocess
# DEVNOTE: import all external libraries/dependencies above this line, and all internal libraries/dependencies below this line
import argparsing
import dataDriver
import out

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("This is a library. This was probably ran accidentally.\nPlease execute the pizza program from the \"main.py\" program contained in the root of the project (" + dir_path + ") by running \"python3 main.py\", or open it in a text editor/IDE to see its contents and use in the program.")
    exit(1)

args = argparsing.returnArgs()

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
    parlorName = configData['parlorName']
    out.clear()
    print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
    print(out.dim + "You may type \"prices\" at any time to list relevant prices for the current field" + out.reset)
    print("Please enter your name " + out.dim + "[John Doe]" + out.reset + ": ", end='')
    orderName = str(input())
    if orderName == "": orderName = "John Doe"
    incrementor = 1
    pizzas = {}
    decision = "y"
    selected = False
    while decision == "y":
        out.clear()
        print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
        print(out.dim + "You may type \"prices\" at any time to list relevant prices for the current field" + out.reset)
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
            if toppingInput == ['prices']:
                priceTable()
                print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
                print(out.dim + "You may type \"price\" at any time to list relevant prices for the current field" + out.reset)
                print(out.bold + "Pizza " + str(incrementor) + out.reset + ":")
                print("Please enter the size of the pizza " + out.dim + "[S/m/l/prices]" + out.reset + ": " + pizzaInput)
                continue
            if pizzaToppings == ['']: 
                pizzaToppings = []
                selected = True
            elif conflicts != []:
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
        print("Would you like to order another pizza? " + out.dim + "[y/N]" + out.reset + ": ", end='')
        decision = str(input()).lower()
        selected = False
    out.clear()
    print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
    print("Would you like this order delivered? It will cost " + out.bold + "$" + str(configData["deliveryFee"]) + out.reset + ". " + out.dim + "[y/N]" + out.reset + ": ", end='')
    delivery = str(input()).lower()
    if delivery == "y":
        delivery = True
    else:
        delivery = False
    if delivery == True:
        print("Please enter your address " + out.dim + "[123 Main St. Anytown, CA 12345]" + out.reset + ": ", end='')
        address = str(input())
        if address == "": address = "123 Main St. Anytown, CA 12345"
        print("Would you like to give the driver a tip? " + out.dim + "[y/N]" + out.reset + ": ", end='')
        tip = str(input()).lower()
        if tip == "y":
            print("Please enter the tip amount " + out.dim + "[5.25 would be $5.25]" + out.reset + ": ", end='')
            tip = float(input())
        else:
            tip = None
    else:
        address = None
        tip = 0
    if args.debugFlag == True:
        out.clear()
        print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
        print("Debug flag enabled; would you like to make an internal comment for the order? " + out.dim + "[y/N]" + out.reset + ": ", end='')
        comment = str(input()).lower()
        if comment == "y":
            print("Please enter the comment: ", end='')
            comment = str(input())
        else:
            comment = None
    else:
        comment = None
    out.clear() 
    print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
    print("Order processed successfully! Summary:")
    print("Name: " + out.bold + orderName + out.reset)
    print("Pizzas:")
    for pizza in pizzas:
        print("\t" + pizza + ": " + pizzas[pizza]["size"] + " pizza with " + "cheese, " + str(pizzas[pizza]["toppings"])[1:len(str(pizzas[pizza]["toppings"]))-1].replace("'", "")) if pizzas[pizza]["toppings"] != [] else print("\t" + pizza + ": " + pizzas[pizza]["size"] + " pizza with cheese")
    print("The order will be delivered.") if delivery == True else print("The order will be picked up.")
    if delivery == True:
        print("The order will be delivered to " + out.bold + address + out.reset + ".")
        print("The driver will be given a tip of $" + "{:.2f}".format(tip) + ".") if tip != None else print("The driver will not be given a tip.")
    if args.debugFlag == True:
        out.printDebug("Internal comment: " + str(comment)) if comment else out.printDebug("Internal comment: None")
        out.printDebug("Dumping internal content structures: ")
        out.printDebug(str(dataDriver.loadOrders()))
        dataDriver.__listOrders(dataDriver.loadOrders())
    print("Does this look correct to you? " + out.dim + "[Y/n]" + out.reset + ": ", end='')
    decision = str(input()).lower()
    if decision == "n":
        newOrder()
        return
    out.clear()
    print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
    print(out.underlined + "Checkout:" + out.reset)
    print("Itemized total:")
    prices = {}
    subTotal = float(0)
    for pizza in pizzas:
        price = float(0)
        if pizzas[pizza]["size"] == "small":
            price = price + float(configData["sizeCosts"]["small"])
        elif pizzas[pizza]["size"] == "medium":
            price = price + float(configData["sizeCosts"]["medium"])
        elif pizzas[pizza]["size"] == "large":
            price = price + float(configData["sizeCosts"]["large"])
        if len(pizzas[pizza]["toppings"]) > 3:
            for i in range(3):
                price = price + float(configData["toppings<=3"])
            for i in range(len(pizzas[pizza]["toppings"]) - 3):
                price = price + float(configData["toppings>=4"])
        else:
            if pizzas[pizza]["toppings"] == []:
                None
            else:
                for i in range(len(pizzas[pizza]["toppings"])):
                    price = price + float(configData["toppings<=3"])
        print("\tPizza " + pizza + ": " + pizzas[pizza]["size"] + " pizza with " + "cheese, " + str(pizzas[pizza]["toppings"])[1:len(str(pizzas[pizza]["toppings"]))-1].replace("'", "") + " -- " + out.bold + "$" + "{:.2f}".format(price) + out.reset) if pizzas[pizza]["toppings"] != [] else print("\tPizza " + pizza + ": " + pizzas[pizza]["size"] + " pizza with cheese -- " + out.bold + "$" + "{:.2f}".format(price) + out.reset)
        subTotal = subTotal + price
    print()
    print("Subtotal: " + out.bold + "$" + "{:.2f}".format(subTotal) + out.reset)
    tax = subTotal * float(configData["taxRate"]/100)
    print("Tax: " + out.bold + "$" + "{:.2f}".format(tax) + out.reset)
    total = subTotal + tax
    print("Total: " + out.bold + "$" + "{:.2f}".format(total) + out.reset)
    print()
    if delivery == True:
        price = float(configData["deliveryFee"])
        print("Delivery fee: " + out.bold + "$" + "{:.2f}".format(price) + out.reset)
        if tip != None:
            price = price + tip
            print("Tip: " + out.bold + "$" + "{:.2f}".format(tip) + out.reset)
        grandTotal = total + price
    else:
        print("Delivery fee: " + out.bold + "$0.00" + out.reset)
        grandTotal = total
    print()
    print("Grand total: " + out.bold + "$" + "{:.2f}".format(grandTotal) + out.reset)
    print()
    print("Does this seem correct to you? " + out.dim + "[Y/n]" + out.reset + ": ", end='')
    decision = str(input()).lower()
    if decision == "n":
        newOrder()
        return
    orderUUID = dataDriver.writeOrder(dataDriver.loadOrders(), orderName, pizzas, delivery, address, tip, comment)
    newOrderObject = dataDriver.loadOrders()[orderUUID]
    out.clear()
    print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
    print(out.green + "Order placed!" + out.reset + " Would you like a receipt? " + out.dim + "[Y/n]" + out.reset + ": ", end='')
    decision = str(input()).lower()
    if decision == "n":
        out.clear()
        print(out.bold + "Create a new order" + out.reset + " - " + parlorName + " Ordering System")
        print(out.green + "Order placed!" + out.reset)
        print("Returning to main menu...")
        time.sleep(2)
        out.clear()
        return
    out.generateReceipt(newOrderObject)
    out.clear()

def viewOrder(order):
    out.clear()
    parlorName = dataDriver.loadConfig()["parlorName"]
    configData = dataDriver.loadConfig()
    print(out.underlined + out.bold + "Recall a previous order - Order #" + order["incrementor"] + out.reset + out.underlined + " - " + parlorName + " Ordering System" + out.reset)
    print("Information for order #" + order["incrementor"])
    print("Name: " + order["name"])
    print("Pizzas:")
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
        if order["pizzas"][pizza]["toppings"] != []:
            print("\tPizza " + pizza + ": " + order["pizzas"][pizza]["size"] + " pizza with " + "cheese, " + str(order["pizzas"][pizza]["toppings"])[1:len(str(order["pizzas"][pizza]["toppings"]))-1].replace("'", "") + " -- " + out.bold + "$" + "{:.2f}".format(price) + out.reset) 
        elif order["pizzas"][pizza]["toppings"] == []:
             print("\tPizza " + pizza + ": " + order["pizzas"][pizza]["size"] + " pizza with cheese -- " + out.bold + "$" + "{:.2f}".format(price) + out.reset)
        subTotal = subTotal + price
    print()
    print("Subtotal: " + out.bold + "$" + "{:.2f}".format(subTotal) + out.reset)
    tax = subTotal * float(configData["taxRate"]/100)
    print("Tax: " + out.bold + "$" + "{:.2f}".format(tax) + out.reset)
    total = subTotal + tax
    print("Total: " + out.bold + "$" + "{:.2f}".format(total) + out.reset)
    print()
    if order["delivered"] == True:
        price = float(configData["deliveryFee"])
        print("Delivery fee: " + out.bold + "$" + "{:.2f}".format(price) + out.reset)
        if order["deliveryTip"] != None:
            price = price + order["deliveryTip"]
            print("Tip: " + out.bold + "$" + "{:.2f}".format(order["deliveryTip"]) + out.reset)
        grandTotal = total + price
    else:
        print("Delivery fee: " + out.bold + "$0 (no delivery)" + out.reset)
        grandTotal = total
    print()
    print("Grand total: " + out.bold + "$" + "{:.2f}".format(grandTotal) + out.reset)
    if order["delivered"] == True:
        print("Delivery: Yes")
        print("Address: " + order["address"])
    else:
        print("Delivery: No")
        print("Address: 123 Parlor St. for pickup")
    print("\nComments: " + order["comments"]) if args.debugFlag == True and "comments" in order else None
    print()
    print("Type R to reprint a receipt for the order, or press any other key to return to main menu...")
    decision = str(input()).lower()
    if decision == "r":
        out.generateReceipt(order)
    out.clear()

def viewOrders():
    out.clear()
    orders = dataDriver.loadOrders()
    parlorName = dataDriver.loadConfig()["parlorName"]
    print(out.underlined + out.bold + "Recall a previous order" + out.reset + out.underlined + " - " + parlorName + " Ordering System" + out.reset)
    print(out.bold + "List of orders:" + out.reset)
    i = 0
    orderIncrementors = {}
    for order in orders: orderIncrementors[orders[order]["incrementor"]] = orders[order]
    for orderNo in sorted (orderIncrementors.keys()):
        print("\t" + out.bold + str(orderNo) + out.reset + ": Order from " + orderIncrementors[orderNo]["name"] + " @ " + time.ctime(orderIncrementors[orderNo]["time"]))
    print()
    print("Enter the number of the order you would like to view: ", end='')
    orderToLoad = input()
    if orderToLoad in orderIncrementors:
        viewOrder(orderIncrementors[orderToLoad])
    else:
        out.printError("Invalid order number. Please select a valid, listed order number. Press enter to continue...")
        input()
        viewOrders()
    