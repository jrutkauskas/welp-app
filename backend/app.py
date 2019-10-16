from flask import Flask, request, session, render_template, abort, url_for, redirect, flash, Response, jsonify
import datetime
import json

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

import secrets
import time

from model import db, User
app = Flask(__name__)

"""Start App Config"""
import json
with open('settings.json') as json_file:
	data = json.load(json_file)
	app.secret_key = data["secret_key"]
	app.config["SQLALCHEMY_DATABASE_URI"] = data["db_uri"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


""" Routes """
@app.route("/")
def home():
	return "Server Works!"




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