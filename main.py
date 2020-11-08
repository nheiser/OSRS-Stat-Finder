from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask import redirect

import json
from flask import jsonify
import requests

app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def home():

	if (request.method == "GET"):

		return render_template("index.html")

	else:
		
		content = request.json["subject"]
		
		url = "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + content
		
		response = requests.get(url, allow_redirects = False)
		
		
		if (response.status_code != 200):
			return render_template("osrs.html", stats = "Unable to load hiscores")
		
		stats = str(response.text)
		
		arrSkills = ["Attack", "Strength", "Defence", "Hitpoints", "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking", "Crafting", "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer", "Farming", "Runecraft", "Hunter", "Construction"]
		arrStats = []
		
		for i in range (0, 23):
		
			stats = stats[stats.find('\n') + 1:]
			end = stats.find('\n')
			statBar = stats[:end]
		
			#Stat Bar:
			#Rank,Level,XP
			#5000,99,13034431
		
			statBar = statBar[statBar.find(",") + 1:]
			end = statBar.rfind(",")
		
			level = statBar[0:end]
			
			arrStats.append(level)
		
		
		obj = {}
		for i in range (0, len(arrSkills)):
			obj[arrSkills[i]] = arrStats[i]
		
		return (jsonify(obj))
		
		
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

