import discord

##	my own files
import src.vectormath


def extractpoint(msg):
	"""This function extracts a point from a givven message in the format: (x, y, z)
	   it checks everything to make sure, that the message is valid."""
	msg = msg.replace("(", "").replace(")", "").replace(" ", "").split(",")
	for p in msg:
		if type(p) != "int":
			return False
	return Point(msg[0], msg[1], msg[2])

def extractline(msg):


##	contains all the headers for the diffrent equations and the funciton names that need to be called.
EQUATIONS_HEADERS= {
	"G:" : extractline()
	"P:" : extractpoint()
	"E:" : extractplane()

}


def analysemsg(msg):#
	"""this function analyses the message sennd by the user and calls the function
	   that extracts the actual values of the message"""
	msg = msg.split(" ")
	for msgpart in msg:
		
	if msg[1] in EQUATIONS_HEADERS:
		EQUATIONS_HEADERS[msg[1]](msg[2])
	else:
		return "not found"




class MathBot(discord.Client):
	async def on_ready(self):
		print("logged in as bot")

	#if message posted
	async def on_message(self, message):
		if str(message.author) == "test_bot#3640":
			return

		if message.content.startswith(".math"):
			analysemsg(message.content)
			

