import discord
import string

##	my own files
import src.vectormath


def extractpoint(msg):
	"""This function extracts a point from a givven message in the format: (x, y, z)
	   it checks everything to make sure, that the message is valid."""
	msg = msg.replace("(", "").replace(")", "").replace(" ", "").split(",")
	msg = list(map(float, msg))
	for p in msg:
		##	maybe change this in the future so that it also takes vars not just ints
		if type(p).__name__ != "int" and type(p).__name__ != "float":
			print(type(p))
			return "invalid type of number"
	return src.vectormath.Point(msg[0], msg[1], msg[2])


def extractline(msg):
	##	this function extracts the mathematical values send by the user and puts them into a LinearEquation
	print(msg)
	if msg.translate({ord(c): None for c in "1234567890,. -*"}) != "x=()+r()":
		print(msg)
		return "invalid format"
	msg = msg.translate({ord(c): None for c in "x=()+*() "}).replace("r", ",")
	msg = list(map(float, msg.split(",")))
	avector = src.vectormath.Vector(msg[0], msg[1], msg[2])
	mvector = src.vectormath.Vector(msg[3], msg[4], msg[5])
	return src.vectormath.LinearEquation(avector, mvector)


def extractplane():
	pass

##	contains all the headers for the diffrent equations and the funciton names that need to be called.
EQUATIONS_HEADERS= {
	"G:" : extractline,
	"P:" : extractpoint,
	"E:" : extractplane

}


def analysemsg(msg):#
	"""this function analyses the message sennd by the user and calls the function
	   that extracts the actual values of the message"""
	classes = []
	msg = msg.split(" ")
	for index, m in enumerate(msg):
		if index % 2 != 0:
			if msg[index] not in EQUATIONS_HEADERS:
				return "not found"
			classes.append(EQUATIONS_HEADERS[msg[index]](msg[index + 1]))

	##	now comes the code that starts the actual calculations
	returncontent = []
	print(classes)
	for cl in classes:
		if type(cl).__name__ == "LinearEquation" or type(cl).__name__ == "PlaneEquation":
			for p in classes:
				if type(p).__name__ == "Point":
					if cl.checkpoint(p):
						returncontent.append(f"{str(p)} `liegt auf` {str(cl)},\n")
					else:
						returncontent.append(f"{str(p)} `liegt nicht auf` {str(cl)},\n")

	return returncontent




class MathBot(discord.Client):
	async def on_ready(self):
		print("logged in as bot")

	#if message posted
	async def on_message(self, message):
		if str(message.author) == "test_bot#3640":
			return

		if message.content.startswith(".math"):
			bot_message = "result:\n"
			newmsg = analysemsg(message.content)
			for s in newmsg:
				bot_message = bot_message + str(s) + " "
			await message.channel.send(bot_message)
