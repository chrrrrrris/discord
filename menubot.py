#Note this is setup for Python 3.4 to refactor for Python 3.5
#replace @asyncio.coroutine with async and yield from with await

import discord
from discord.ext import commands
from discord import Server
import urllib
from bs4 import BeautifulSoup
import random
import asyncio
from lxml import html, etree
import requests
import requests

bot = commands.Bot(command_prefix='>')
global foodPrices
foodPrices = []
global foodItems
foodItems = []

def formatPrice(preList):
    formattedList = []
    for element in preList:
        if element.isspace() is not True:
            formattedList.append(element.strip().replace("\n","").replace(" ",""))
    return formattedList

def formatList(preList):
    formattedList = []
    for element in preList:
        if element.isspace() is not True:
            formattedList.append(element.strip())
    return formattedList

def getMenu(url):
    print(url)
    page = requests.get('https://www.menulog.com.au/rang-mahal-epping')
    tree = html.fromstring(page.content)
    #tree = html.fromstring(page)
    items = tree.xpath('//div[@class= "foodItemInfo"]/h4/text()')
    global foodItems
    foodItems = formatList(items)
    prices = tree.xpath('//div[contains(@class, "varieties")]')
    addString = False
    foodPrices2 = []
    global foodPrices
    for price in prices:
        foodPrices.append(str(price.text_content()))
    foodPrices = formatPrice(foodPrices)
    msg = ""
    for item in foodItems:
        if len(msg) >= 2000:
            return msg
        msg += "Item: "+ item + " Price: " + foodPrices[foodItems.index(item)] + " "
    return msg


#print('Food Item: ', foodItems)
#print('Prices: ', foodPrices)

def searchByItem(item):
    for i in foodItems:
        if item in i.lower():
            ind = foodItems.index(i)
            print("Food Item ", i)
            print("Price :", foodPrices[ind])

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def getmenu(*args):
    url = args[0]
    print(len(args))
    page = requests.get(url)
    tree = html.fromstring(page.content)
    items = tree.xpath('//div[@class= "foodItemInfo"]/h4/text()')
    global foodItems
    foodItems = formatList(items)
    prices = tree.xpath('//div[contains(@class, "varieties")]')
    global foodPrices
    foodPrices = []
    for price in prices:
        foodPrices.append(str(price.text_content()))
    foodPrices = formatPrice(foodPrices)
    msg = ""
    if len(args)==1:
        for item in foodItems:
            if len(msg) >= 1000:
                await bot.say(msg)
                return
            msg += "Item: "+ item + " Price: " + foodPrices[foodItems.index(item)] + " "
    if len(args)==2:
        for item in foodItems:
            if args[1] in item.lower():
                print("wat")
                if len(msg) >= 1000:
                    await bot.say(msg)
                    return
                msg += "Item: "+ item + " Price: " + foodPrices[foodItems.index(item)] + " "
        await bot.say(msg)

bot.run('token')
