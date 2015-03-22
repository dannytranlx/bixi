from flask import Flask, render_template, Response
import json
import re
import urllib2
from flask.ext.cache import Cache
import redis
import os

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'redis'
redis_url = os.getenv('REDISTOGO_URL', 'redis://127.0.0.1:6379')
redis = redis.from_url(redis_url)
app.cache = Cache(app)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/stations")
@app.cache.cached(timeout=300, key_prefix="stations")
def api():
	data = fetch_data()
	return Response(json.dumps(data, sort_keys=True, indent=True),  mimetype='application/json')

def fetch_data():
	url_bixi = "http://montreal.bixi.com/maps/statajax"
	stations = []

	try:
		webparser = urllib2.urlopen(url_bixi).read()
	except:
		return "Error: Cannot read the feed"

	if webparser:
		data = re.findall('var station\s=\s\\{(.*?)\\}', webparser)
		for station in data:
			station_obj = {}

			attributes = station.split(',')
			for attribute in attributes:
				attr = attribute.split(':')

				attr_name = attr[0].strip()
				attr_value = attr[1].strip('"')

				if attr_name in ('id', 'name', 'lat', 'long', 'nbBikes', 'nbEmptyDocks', 'installed', 'locked', 'temporary'):
					station_obj[attr_name] = clean(attr_value)

			stations.append(station_obj)

	if stations:
		return stations

	return "No station found"

def clean(value):
	if re.match(r'^-?\d+\.\d+$', value):
		return float(value)
	elif re.match(r'^\d+$', value):
		return int(value)
	elif 'true' in value:
		return True
	elif 'false' in value:
		return False

	return value

if __name__ == "__main__":
	app.debug = True
	app.run()
