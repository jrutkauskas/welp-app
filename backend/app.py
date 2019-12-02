from flask import Flask, request, session, render_template, abort, url_for, redirect, flash, Response, jsonify
import datetime
import json

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

import time

from model import db, User, Bathroom, Rating, Report
from welp import WelpApp
import tests
from tests import WelpTester
import unittest

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

server = WelpApp()

db.init_app(app)

""" Routes """
@app.route("/")
def home():
	session["started"] = True
	#return "Server Works!"
	return app.send_static_file('index.html')

@app.route("/api/bathrooms", methods=["POST"])
def create_a_bathroom():
	user = None
	if not "user_id" in session:
		return "Not logged in!", 400

	if "user_id" in session:
		user = server.get_user_by_id(session["user_id"])
	
	data = request.get_json()
	result, bathroom, db_obj= server.create_bathroom(data, user)
	if not result:
		return bathroom, 400
	return json.dumps(bathroom)
	
	#return "Not implemented, would return bathrooms based on POSTed params", 404

@app.route("/api/getbathrooms", methods=["POST"])
def find_bathroom():
	user = None
	if "user_id" in session:
		user = server.get_user_by_id(session["user_id"])
	
	data = request.get_json()
	result, bathrooms = server.get_bathrooms_based_on_params(data,user)
	if not result:
		return bathrooms, 400
	return json.dumps(bathrooms)

@app.route("/api/bathrooms/<id>", methods=["GET","POST"])
def get_or_set_specific_bathroom(id):
	user = None
	if not "user_id" in session and request.method == "POST":
		return "Not logged in!", 400
	
	if "user_id" in session:
		user = server.get_user_by_id(session["user_id"])
	
	if request.method == "GET":
		result, bathroom = server.get_bathroom_by_id(id, user)
		if not result:
			return bathroom, 400
		return json.dumps(bathroom)
	else:
		data = request.get_json()
		result, bathroom = server.set_bathroom_by_id(id, data)
		if not result:
			return bathroom, 400
		return json.dumps(bathroom)

	

	#""" NEEDS to also do all the ratings averaging AND return whether a user rated a bathroom or not"""
	#return "Not implemented, would return bathroom with id or allow modification", 404



@app.route("/api/users/<id>")
def get_specific_user(id):
	return f"Not implemented; id is {id}", 404

@app.route("/api/users/<user_id>/ratings/", methods=["POST"])
def set_user_bathroom_ratings(user_id):
	if not "user_id" in session:
		return "Not logged in!", 400
	
	user = server.get_user_by_id(session["user_id"])
	data = request.get_json()

	result, ret = server.set_user_bathroom_rating(user, data)
	if not result:
		return ret, 400
	

	return "rating updated successfully"

@app.route("/api/users", methods=["POST"])
def add_user():
	if "user_id" in session:
		return "Already logged in", 400
	data = request.get_json()
	result, ret = server.create_user(data)
	if not result:
		return ret, 400
	
	session["user_id"] = ret.id
	
	res = server.convert_user_to_dict(ret)
	return json.dumps(res)
	#return "Not implemented.  Would return user id of new user or errors for why they can't sign up", 404

@app.route("/api/authenticate", methods=["POST"])
def authenticate():
	if "user_id" in session:
		return "Already logged in", 400
	data = request.get_json()
	if not "username" in data or not "password" in data:
		return "must send username and password", 400
	result, ret = server.authenticate_user(data)
	if not result:
		return ret, 400
	
	# save user in session
	session["user_id"] = ret.id
	
	res = server.convert_user_to_dict(ret)
	return json.dumps(res)

@app.route("/api/logout")
def logout():
	if "user_id" in session:
		del session["user_id"]
	return redirect("/")

@app.route("/api/reports", methods=["GET", "POST"])
def get_all_reports():
	if "user_id" in session:
		if request.method == "GET":
			user = server.get_user_by_id(session["user_id"])
			if user and user.isAdmin:
				reports = server.get_reports()
				return json.dumps(reports)
		else:
			data = request.get_json()
			if server.report_bathroom_by_id(data["bathroom_id"], data["description"]):
				return "Successfully reported"
			else:
				return "Could not report this bathroom", 400
	else:
		return "not allowed", 400

@app.route("/api/delete/report", methods=["POST"])
def delete_report():
	if "user_id" in session:
		if request.method == "POST":
			user = server.get_user_by_id(session["user_id"])
			if user and user.isAdmin:
				data = request.get_json()
				if server.delete_report_by_id(data["id"]):
					return "Deleted Successfully"
				else:
					return "Could not delete this report", 400
	else:
		return "not allowed", 400

@app.route("/api/delete/bathroom", methods=["POST"])
def delete_bathroom():
	if "user_id" in session:
		if request.method == "POST":
			user = server.get_user_by_id(session["user_id"])
			if user and user.isAdmin:
				data = request.get_json()
				if server.delete_bathroom_by_id(data["id"]):
					return "Deleted Successfully"
				else:
					return "Could not delete this bathroom", 400
	else:
		return "not allowed", 400

if __name__ == "__main__":
	app.run(threaded=True, host='0.0.0.0')



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
	print("testing!")
	#t = WelpTester()
	#t.runTests()
	suite = unittest.TestLoader().loadTestsFromModule(tests)
	unittest.TextTestRunner(verbosity=2).run(suite)
	return

@app.cli.command("bootstrapdb")
def bootstrap_db():
	"""Fills Database with Sample data (WARNING! THIS CLEARS OUT ALL OTHER DB DATA)"""
	db.drop_all()
	db.create_all()
	t = WelpTester()
	t.bootstrapDB()
	return

