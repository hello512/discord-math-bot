from discord import Embed


MATHBOTINFOEMBED = Embed(
	title = "Discord Mathe Bot Information / Hilfe",
	description = "Hier findest du alle wichtigen Informationen und Befehle um den Mathe Bot benutzen zu können.",
	url = "https://github.com/hello512/discord-math-bot",
	colour = 16312092,
	)

MATHBOTINFOEMBED.set_footer(text = "math-bot created by @0x5F_#3292", icon_url = "https://cdn.discordapp.com/embed/avatars/1.png")
MATHBOTINFOEMBED.set_author(name = "math-bot", icon_url = "https://cdn.discordapp.com/embed/avatars/1.png" )
MATHBOTINFOEMBED.add_field(
	name = "Generell",
	value = "Sende Punkte, Gradengleichungen und Ebenengleichung an den mathe bot und er wird herausfinden ob die Punkte auf den Graden oder den Ebenen liegen. Bitte beachte, dass keine Leerzeichen in den Gleichungen stehen dürfen und die Zahlen mit Punken statt Kommas geschrieben werden müssen.\n",
	inline = "False"
	)
MATHBOTINFOEMBED.add_field(
	name = "Punkte:",
	value =	"Punkte müssen in einem bestimmten Format gesendet werden, um von dem Bot als Punkt wahrgenommen zu werden.```P: (x,y,z)```Sollte es sich um einen zwei dimensionalen Punkt handeln, muss für z null eingesetzt werden. Außerdem darf der Name des Punktes (P:) nicht verändert werden.\n",
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
	value = "```.math G: x=(4,-6,-1)+r(1,1,2) P: (5,-5,1)```Output:```(5.0, -5.0, 1.0) liegt auf G: x = (4.0, -6.0, -1.0) + r * (1.0, 1.0, 2.0)```\n\n",
	inline = False
	)

"""
The general information Embed for the whole server. It contains all the available commands and bots
and shows how to access their info / help sites.
"""

GENERALINFOEMBED = Embed(
	title = "Generelle Informationen",
	description = "Eine Auflistung aller commands bzw. bots",
	url = "https://github.com/hello512/discord-math-bot",
	color = 16312092
	)

GENERALINFOEMBED.set_footer(text = "math-bot created by @0x5F_#3292", icon_url = "https://cdn.discordapp.com/embed/avatars/1.png")
GENERALINFOEMBED.set_author(name = "math-bot", icon_url = "https://cdn.discordapp.com/embed/avatars/1.png")
GENERALINFOEMBED.add_field(
	name = "mathe-bot",
	value = "Der mathe bot kann ein paar simple Rechnungen durchführen. Schreibe ``.math info`` um eine Auflistung aller Funktionen dieses bots zu sehen."
	)


##	Result Embed:

def generate_content(result_list):
	result_string = ""
	for result in result_list:
		result_string = result_string + result
	return result_string

def make_result_embed(results_list : list):
	result_embed = Embed(
	colour = 5877209,
	description = generate_content(results_list)
	)
	#result_embed.set_author(name = "math-bot", icon_url = "https://cdn.discordapp.com/embed/avatars/2.png"),
	#result_embed.set_footer(text = "math-bot created by @0x5F_#3292")
	return result_embed
