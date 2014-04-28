from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup
import urllib2

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html', data = fetch_data())

@app.route("/api")
def api():
	data = fetch_data()
	return data

def fetch_data():
	
	return 'Aucun station trouv&eacute;e'

if __name__ == "__main__":
	app.debug = True
	app.run()
