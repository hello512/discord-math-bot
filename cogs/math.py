from discord.ext import commands

import discord
import logging
import string
import time
import sys

##	my own files
sys.path.append("../")
from discord_math_bot.vectormath import vectormath
from discord_math_bot.messages import MATHBOT_ERROR_MESSAGE, MATHBOTINFOEMBED, make_result_embed




def extractpoint(msg):
    """This function extracts a point from a givven message in the format: (x, y, z)
       it checks everything to make sure, that the message is valid."""
    msg = msg.replace("(", "").replace(")", "").replace(" ", "").split(",")
    print(msg)
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


def extractplane(msg):
    translated = msg.translate({ord(c): None for c in "1234567890,. *"}).translate({ord(c): "f" for c in "rstk"}).replace("-", "+")
    forms = ["x=()+f()+f()", "xyz=", "[x-()]*()="]
    if translated == forms[0]:
        translated = msg.translate({ord(c): None for c in "x=()frtsk*"}).translate({ord(c): "," for c in "+-"}).split(",")
        translated = list(map(float, translated))
        avector = vectormath.Vector(vectorlist = translated[0 : 3])
        mvector = vectormath.Vector(vectorlist = translated[3 : 6])
        vvector = vectormath.Vector(vectorlist = translated[6 : 9])
        return vectormath.PlaneEquation(avector, mvector, vvector)
    elif translated == forms[1]:
        pass
    elif translated == forms[2]:
        pass
    return "invalid format"

##	contains all the headers for the diffrent equations and the funciton names that need to be called.
EQUATION_HEADERS= {
    "G:" : extractline,
    "P:" : extractpoint,
    "E:" : extractplane,
    "help" : lambda : MATHBOTINFOEMBED
}

def makestring(contentlist):
    ##	puts the strings stored in the contentlist into one final string that gets send to the client
    ##	Not used anymore by analysemsg. Now it sends an result embed
    returnmessage = "result:\n"
    for elem in contentlist:
        returnmessage = returnmessage + str(elem) + " "
    return returnmessage


class Calculations:
    def __init__(self, classes):
        self.classes = classes
        self.returncontent = []

    def line_calculation(self, line):
        for cl2 in self.classes:
            if type(cl2).__name__ == "Point":
                if line.check_point(cl2):
                    self.returncontent.append(f"{str(cl2)} `liegt auf` {str(line)}\n")
                else:
                    self.returncontent.append(f"{str(cl2)} `liegt nicht auf` {str(line)}\n")

    def plane_calculation(self, plane):
        for cl2 in self.classes:
            if type(cl2).__name__ == "Point":
                if plane.check_point(cl2):
                    self.returncontent.append(f"{str(cl2)} `liegt auf` {str(plane)}\n")
                else:
                    self.returncontent.append(f"{str(cl2)} `liegt nicht auf` {str(plane)}\n")
            if type(cl2).__name__ == "LinearEquation":
                if plane.check_line(cl2)[0] == "equal":
                    self.returncontent.append(f"{str(cl2)} `liegt auf` {str(plane)}\n")
                if plane.check_line(cl2)[0] == "parallel":
                    self.returncontent.append(f"{str(cl2)} `ist mit einem Abstand von` {str(plane.check_line(cl2)[1])} `LE parallel zu` {str(plane)}\n")
                if plane.check_line(cl2)[0] == "point":
                    self.returncontent.append(f"{str(cl2)} `schneidet` {str(plane)} `in` {str(plane.check_line(cl2)[1])}\n")

    def do_calculations(self):
        for cl in self.classes:
            if type(cl).__name__ == "LinearEquation":
                self.line_calculation(cl)
            elif type(cl).__name__ == "PlaneEquation":
                self.plane_calculation(cl)

        return make_result_embed(self.returncontent)


def analysemathmsg(msg):#
    """this function analyses the message sennd by the user and calls the function
       that extracts the actual values of the message"""
    classes = []
    #msg = msg.split(" ")
    for index, m in enumerate(msg):
        if index % 2 == 0:
            if msg[index] not in EQUATION_HEADERS:
                return MATHBOT_ERROR_MESSAGE ## stored in messages/text_messages.py
            try:
                classes.append(EQUATION_HEADERS[msg[index]](msg[index + 1]))
            except IndexError:
                return "no arguments"


    ##	now comes the code that starts the calculations
    calc = Calculations(classes)
    return calc.do_calculations()

def check_channel(ctx):
    return ctx.channel.name == "bot-commands"

class Math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.equation_headers = {
            "G:" : extractline,
            "P:" : extractpoint,
            "E:" : extractplane,
        }

    @commands.command()
    @commands.check(check_channel)
    async def math(self, ctx, *args):
        botmessage = analysemathmsg(args)
        if type(botmessage).__name__ == "str":
            await ctx.send(botmessage)
        if type(botmessage).__name__ == "Embed":
            await ctx.send(embed = botmessage)
        print(type(botmessage).__name__)

    @commands.command(naem = "math help")
    @commands.check(check_channel)
    async def math_help(self, ctx):
        await ctx.send("help page")


def setup(bot):
    bot.add_cog(Math(bot))
