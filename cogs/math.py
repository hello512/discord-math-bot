from discord.ext import commands

import discord
import logging
import string
import time
import sys

##	my own files
sys.path.append("../")
from discord_math_bot.vectormath import vectormath
from messages import MATHBOT_ERROR_MESSAGE, make_result_embed




def extractpoint(msg):
    """This function extracts a point from a givven message in the format: (x, y, z)
       it checks everything to make sure, that the message is valid."""
    msg = msg.replace("(", "").replace(")", "").replace(" ", "").split(",")
    msg = list(map(float, msg))
    for p in msg:
        ##	maybe change this in the future so that it also takes vars not just ints
        if type(p).__name__ != "int" and type(p).__name__ != "float":
            return "invalid type of number"
    return vectormath.Point(msg[0], msg[1], msg[2])


def extractline(msg):
    ##	this function extracts the mathematical values send by the user and puts them into a LinearEquation
    if msg.translate({ord(c): None for c in "1234567890,. -*"}) != "x=()+r()":
        return "invalid format"
    msg = msg.translate({ord(c): None for c in "x=()+*() "}).replace("r", ",")
    msg = list(map(float, msg.split(",")))
    avector = vectormath.Vector(msg[0], msg[1], msg[2])
    mvector = vectormath.Vector(msg[3], msg[4], msg[5])
    return vectormath.LinearEquation(avector, mvector)


def extractplane():
    if msg.translate({ord(c): None for c in "1234567890,. -*"}) != "x=()+r()+s()":
        return

##	contains all the headers for the diffrent equations and the funciton names that need to be called.
EQUATION_HEADERS= {
    "G:" : extractline,
    "P:" : extractpoint,
    "E:" : extractplane,
}

def makestring(contentlist):
    ##	puts the strings stored in the contentlist into one final string that gets send to the client
    ##	Not used anymore by analysemsg. Now it sends an result embed
    returnmessage = "result:\n"
    for elem in contentlist:
        returnmessage = returnmessage + str(elem) + " "
    return returnmessage


def analysemathmsg(msg):#
    """this function analyses the message sennd by the user and calls the function
       that extracts the actual values of the message"""
    classes = []
    #msg = msg.split(" ")
    for index, m in enumerate(msg):
        if index % 2 == 0:
            if msg[index] not in EQUATION_HEADERS:
                return '❌Run ``.math info`` or ``.math help`` to learn everything about the math bot' ## stored in messages/text_messages.py
            try:
                classes.append(EQUATION_HEADERS[msg[index]](msg[index + 1]))
            except IndexError:
                return "no arguments"


    ##	now comes the code that starts the calculations
    returncontent = []
    for cl in classes:
        if type(cl).__name__ == "LinearEquation" or type(cl).__name__ == "PlaneEquation":
            for p in classes:
                if type(p).__name__ == "Point":
                    if cl.checkpoint(p):
                        returncontent.append(f"{str(p)} `liegt auf` {str(cl)}\n")
                    else:
                        returncontent.append(f"{str(p)} `liegt nicht auf` {str(cl)}\n")

    return make_result_embed(returncontent)

class Math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.equation_headers = {
            "G:" : extractline,
            "P:" : extractpoint,
            "E:" : extractplane,
        }

    @commands.command()
    async def math(self, ctx, *args):
        botmessage = analysemathmsg(args)
        if type(botmessage).__name__ == "str":
            await ctx.send(botmessage)
        if type(botmessage).__name__ == "Embed":
            await ctx.send(embed = botmessage)
        print(type(botmessage).__name__)


def setup(bot):
    bot.add_cog(Math(bot))
