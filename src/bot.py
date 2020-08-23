import datetime
import discord
import string
import time

##	my own files
import src.vectormath


"""The general information embed for the mathbot. Triggered by typing in ".math info" or ".math help".
   It contains all the important information on how to use the mathbot.
   It will also be send if someone types in a command that the program can not recognize, assuming the
   user does not now how to use the mathbot."""
MATHBOTINFOEMBED = discord.Embed(
	title = "Discord Mathe Bot Information / Hilfe",
	description = "Hier findest du alle wichtigen Informationen und Befehle um den Mathe Bot benutzen zu können.",
	#timestamp = datetime.datetime.fromtimestamp(time.time(), tz = None),
	url = "",
	colour =16312092,
	)

MATHBOTINFOEMBED.set_footer(text = "math-bot created by @0x5f_", icon_url = "https://cdn.discordapp.com/embed/avatars/1.png")
MATHBOTINFOEMBED.set_author(name = "math-bot", icon_url = "https://cdn.discordapp.com/embed/avatars/1.png" )
MATHBOTINFOEMBED.add_field(
	name = "Generell",
	value = "Sende Punkte, Gradengleichungen und Ebenengleichung an den mathe bot und er wird herausfinden ob die Punkte auf den Graden oder den Ebenen liegen. Bitte beachte, dass keine Leerzeichen in den Gleichungen stehen dürfen und die Zahlen mit Punken statt Kommas geschrieben werden müssen.\n",
	inline = "False"
	)
MATHBOTINFOEMBED.add_field(
	name = "Punkte:",
	value =	"Punkte müssen in einem bestimmten Vormat gesendet werden, um von dem Bot als Punkt wahrgenommen zu werden.```P: (x,y,z)```Sollte es sich um einen zwei dimensionalen Punkt handeln, muss für z null eingesetzt werden. Außerdem darf der Name des Punktes (P:) nicht verändert werden.\n",
	inline = False
	)
MATHBOTINFOEMBED.add_field(
	name = "Gradengleichungen:",
	value = "Für Gradengleichungen gelten die selben Regeln wie für Punkte.```G: x=(x,y,z)+r*(x,y,z)``` Es ist wichtig zu beachten, dass der Buchstabe des faktors r nicht verändert werden darf. Sonst erkennt der Bot die Gradengleichung nicht.\n",
	inline = False
	)
MATHBOTINFOEMBED.add_field(
	name = "Ebenengleichung:",
	value = "Für Ebenengleichungen gelten die selben Regeln wie für Gradengleichungen. Auch hier darf nichts außer den werten der variablen verändert werden.```E: x=(x,y,z)+r*(x,y,z)+s*(x,y,z)```\n",
	inline = False
	)
MATHBOTINFOEMBED.add_field(
	name = "Beispiele:",
	value = "```.math G: x=(4,-6,-1)+r(1,1,2) P: (5,-5,1)```Output:```(5.0, -5.0, 1.0) liegt auf G: x = (4.0, -6.0, -1.0) + r * (1.0, 1.0, 2.0),```\n\n",
	inline = False
	)

def extractpoint(msg):
	"""This function extracts a point from a givven message in the format: (x, y, z)
	   it checks everything to make sure, that the message is valid."""
	msg = msg.replace("(", "").replace(")", "").replace(" ", "").split(",")
	msg = list(map(float, msg))
	for p in msg:
		##	maybe change this in the future so that it also takes vars not just ints
		if type(p).__name__ != "int" and type(p).__name__ != "float":
			return "invalid type of number"
	return src.vectormath.Point(msg[0], msg[1], msg[2])


def extractline(msg):
	##	this function extracts the mathematical values send by the user and puts them into a LinearEquation
	if msg.translate({ord(c): None for c in "1234567890,. -*"}) != "x=()+r()":
		return "invalid format"
	msg = msg.translate({ord(c): None for c in "x=()+*() "}).replace("r", ",")
	msg = list(map(float, msg.split(",")))
	avector = src.vectormath.Vector(msg[0], msg[1], msg[2])
	mvector = src.vectormath.Vector(msg[3], msg[4], msg[5])
	return src.vectormath.LinearEquation(avector, mvector)


def extractplane():
	if msg.translate({ord(c): None for c in "1234567890,. -*"}) != "x=()+r()+s()":
		return 

##	contains all the headers for the diffrent equations and the funciton names that need to be called.
EQUATION_HEADERS= {
	"G:" : extractline,
	"P:" : extractpoint,
	"E:" : extractplane,
	#"info" : lambda a = 0: MATHBOTINFOEMBED,
	#"help" : lambda a = 0: MATHBOTINFOEMBED
}

def makestring(contentlist):
	##	puts the strings stored in the contentlist into one final string that gets send to the client
	returnmessage = "result:\n"
	for elem in contentlist:
		returnmessage = returnmessage + str(elem) + " "
	return returnmessage

def analysemathmsg(msg):#
	"""this function analyses the message sennd by the user and calls the function
	   that extracts the actual values of the message"""
	classes = []
	msg = msg.split(" ")
	for index, m in enumerate(msg):
		if index % 2 != 0:
			if msg[index] not in EQUATION_HEADERS:
				return MATHBOTINFOEMBED
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
						returncontent.append(f"{str(p)} `liegt auf` {str(cl)},\n")
					else:
						returncontent.append(f"{str(p)} `liegt nicht auf` {str(cl)},\n")

	return makestring(returncontent)



class MathBot(discord.Client):
	async def on_ready(self):
		print("logged in as bot")

	#if message posted
	async def on_message(self, message):
		if str(message.author) == "test_bot#3640":
			return

		if message.channel.name != "bot-commands":
			return

		if message.content.startswith(".math info") or message.content.startswith(".math help"):
			await message.channel.send(embed = MATHBOTINFOEMBED)
			return

		if message.content.startswith(".math"):
			botmessage = analysemathmsg(message.content)
			if type(botmessage).__name__ == "str":
				await message.channel.send(botmessage)
			if type(botmessage).__name__ == "Embed":
				await message.channel.send(embed = botmessage)

		if message.content.startswith(".?") or message.content.startswith(".help"):
			##	sends an info embed back to the user
			return 