from flask import Flask, request, session, render_template, abort, url_for, redirect, flash, Response, jsonify
import datetime
import json

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

import secrets
import time

from model import db, User, Bathroom, Rating
from welp import WelpApp
from tests import WelpTester

app = Flask(__name__,
			static_url_path='', 
            static_folder='../frontend')

"""Start App Config"""
import json
with open('settings.json') as json_file:
	data = json.load(json_file)
	app.secret_key = data["secret_key"]
	app.config["SQLALCHEMY_DATABASE_URI"] = data["db_uri"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1



db.init_app(app)

""" Routes """
@app.route("/")
def home():
	session["started"] = True
	#return "Server Works!"
	return app.send_static_file('index.html')

@app.route("/api/bathrooms")
def get_all_bathrooms():
	return "Not implemented, would return bathrooms based on GET params", 404

@app.route("/api/bathrooms/<id>", methods=["GET","POST"])
def get_or_set_specific_bathroom():
	""" NEEDS to also do all the ratings averaging AND return whether a user rated a bathroom or not"""
	return "Not implemented, would return bathroom with id or allow modification", 404


@app.route("/api/users", methods=["POST"])
def add_user():
	return "Not implemented.  Would return user id of new user or errors for why they can't sign up", 404

@app.route("/api/users/<id>")
def get_specific_user(id):
	return f"Not implemented; id is {id}", 404

@app.route("/api/users/<user_id>/ratings/", methods=["GET","POST"])
def get_user_bathroom_ratings(user_id):
	return "Not implemented, would return or set bathroom ratings for a specific user based on GET params", 404

@app.route("/api/authenticate", methods=["POST"])
def authenticate():
	return "Not implemented, should be passed username and password and will return whether authenticated", 404





if __name__ == "__main__":
	app.run(threaded=True)



# CLI Commands
@app.cli.command("initdb")
def init_db():
	"""Initializes database and any model objects necessary"""
	db.drop_all()
	db.create_all()

	print("Initialized Database.")
	return

@app.cli.command("test")
def test_app():
	"""Runs test commands here"""
	t = WelpTester(db)
	t.runTests()
	return