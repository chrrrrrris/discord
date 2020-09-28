#Note this is setup for Python 3.4 to refactor for Python 3.5
#replace @asyncio.coroutine with async and yield from with await

import discord
from discord.ext import commands
from discord import Server
import random
import asyncio

bot = commands.Bot(command_prefix='>')

optionList = []
choicesVotes = []
pollInProgress = False
pollCompleted = False

@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True, no_pm=True)
@asyncio.coroutine
def startvote(ctx, question, options):
    if(pollInProgress):
        yield from bot.say("Starting new poll")
        yield from bot.say("The last poll's results are:")
        for i in optionList:
            msg = ""
            ind = optionList.index(i.lower())
            msg += str(i)+ " has "+ str(len(choicesVotes[ind]))+" votes."
            yield from bot.say(msg)
        global optionList
        del optionList[:]
        global choicesVotes
        del choicesVotes[:]
    global pollInProgress
    pollInProgress = True
    msg = "The topic is: "+str(question)+" and the options are: "+ str(options)
    yield from bot.say(msg)
    global optionList
    optionList = get_options(options.lower())
    global choiceVotes
    for i in optionList:
        new = set()
        choicesVotes.append(new)

def get_options(message):
    options = message.split(", ")
    return options

@bot.command(pass_context=True, no_pm=True)
@asyncio.coroutine
def vote(ctx, choice):
    if (!pollInProgress):
        yield from bot.say("There isn't a poll in progress")
        return
    if (pollInProgress):
        voter = ctx.message.author
        alreadyVoted = False
        if choice.lower() not in optionList:
            yield from bot.say("That is not a valid choice.")
            return
        global choicesVotes
        for i in choicesVotes:
            if voter.id in i:
                alreadyVoted = True
        if alreadyVoted == True:
            yield from bot.say('You have already voted.')
        if alreadyVoted == False:
            ind = optionList.index(choice.lower())
            choicesVotes[ind].add(voter.id)
            yield from bot.say("You've voted for "+ str(choice))
        else:
            for i in self.choiceVotes:
                msg = str(i) + " has " + str(choiceVotes[optionList.index(i.lower())]) +" votes."
                yield from bot.say(msg)

@bot.command(pass_context=True, no_pm=True)
@asyncio.coroutine
def results(ctx):
    if (pollInProgress):
        yield from bot.say("The current results are:")
        for i in optionList:
            msg = ""
            ind = optionList.index(i.lower())
            msg += str(i)+ " has "+ str(len(choicesVotes[ind]))+" votes."
            yield from bot.say(msg)
    if pollInProgress == False and pollCompleted == True:
        yield from bot.say("The last poll's results are:")
        for i in optionList:
            msg = ""
            ind = optionList.index(i.lower())
            msg += str(i)+ " has "+ str(len(choicesVotes[ind]))+" votes."
            yield from bot.say(msg)
    if (!pollInProgress):
        yield from bot.say("There are no results.")

bot.run('token')
