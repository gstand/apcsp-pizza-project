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
import out

config = dataDriver.loadConfig()

smallPizza = "{:.2f}".format(config['sizeCosts']['small'])
smallAlign = ""
smallAlignN = 8-len(str(smallPizza))
for i in range(smallAlignN):
    smallAlign = smallAlign + " "
mediumPizza = "{:.2f}".format(config['sizeCosts']['medium'])
mediumAlign = ""
mediumAlignN = 7-len(str(mediumPizza))
for i in range(mediumAlignN):
    mediumAlign = mediumAlign + " "
largePizza = "{:.2f}".format(config['sizeCosts']['large'])
largeAlign = ""
largeAlignN = 8-len(str(largePizza))
for i in range(largeAlignN):
    largeAlign = largeAlign + " "
top3 = "{:.2f}".format(config['toppings<=3'])
top4 = "{:.2f}".format(config['toppings>=4'])
taxRate = str(config['taxRate']) + "%"
taxRateAlign = ""
taxRateAlignN = 18-len(taxRate)
for i in range(taxRateAlignN):
    taxRateAlign = taxRateAlign + " "
deliveryFee = "{:.2f}".format(config['deliveryFee'])
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