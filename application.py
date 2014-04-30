from flask import Flask
from flask import render_template
import urllib2
import re

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api")
def api():
	data = fetch_data()
	return ','.join(data)

def fetch_data():
	url_bixi = "http://montreal.bixi.com/maps/statajax"

	try:
		webparser = urllib2.urlopen(url_bixi).read()
	except:
		return "Error: Cannot read the feed"

	if webparser:
		data = re.findall("var station\s=\s\\{(.*?)\\}", webparser)
		

	if data:
		return data

	return "No station found"

if __name__ == "__main__":
	app.debug = True
	app.run()
