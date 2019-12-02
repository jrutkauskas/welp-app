from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False)
	password = db.Column(db.String(250), nullable=False)
	
	ratings = db.relationship("Rating", backref="user", lazy="joined")

	isAdmin = db.Column(db.Boolean)

	def __init__(self, username, password):
		self.username = username
		self.password = generate_password_hash(password)
		self.isAdmin = False

class Bathroom(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	#String attributes
	bathroom_name = db.Column(db.String(120), nullable=False)
	description = db.Column(db.String(600), nullable=True)
	time_availability = db.Column(db.String(300), nullable=True)
	how_to_find_it = db.Column(db.String(300), nullable=True)
	notes = db.Column(db.String(600), nullable=True)

	#location
	latitude = db.Column(db.Float, nullable=False)
	longitude = db.Column(db.Float, nullable=False)

	#Categorical Flag Types
	occupancy_type = db.Column(db.Integer, nullable=True)
	"""
	Type of occupancy in the bathroom
		NULL = Blank
		0 = Single Occupancy
		1 = Multiple Occupancy
		2 = Other
	"""

	hand_drying_type = db.Column(db.Integer, nullable=True)
	"""
	Type of hand-drying available in the bathroom
		NULL = Blank
		0 = Paper Towels
		1 = Electric Hand Dryer
		2 = Electric Hand Dryer AND Paper Towels
		3 = None available
		4 = Other
	"""

	stall_range_type = db.Column(db.Integer, nullable=True)
	"""
	Range type for amount of stalls available / capacity
		NULL = Blank
		0 = One Stall / Single Occupancy
		1 = 2-3 Stalls
		2 = 4-7 Stalls
		3 = 8+ Stalls
	"""

	gender_type = db.Column(db.Integer, nullable=True)
	"""
	Range type for the genders allowed to use this bathroom
		NULL = Blank
		0 = Gender Agnostic
		1 = Men
		2 = Women
		3 = Other
	"""
	# Relationship for ratings
	# Note! This is Dynamic!  It will require you to treat it like a Query object!
	ratings = db.relationship("Rating", backref="bathroom", lazy="dynamic")

	# relationship for reports
	reports = db.relationship("Report", backref="bathroom", lazy="select")

	def get_cleanliness_ratings(self):
		return self.ratings.filter_by(rating_type=0)
	cleanliness_ratings = property(fget=get_cleanliness_ratings)

	def get_privacy_ratings(self):
		return self.ratings.filter_by(rating_type=1)
	privacy_ratings = property(fget=get_privacy_ratings)

	def get_atmosphere_ratings(self):
		return self.ratings.filter_by(rating_type=2)
	atmosphere_ratings = property(fget=get_atmosphere_ratings)

	def get_location_accessibility_ratings(self):
		return self.ratings.filter_by(rating_type=3)
	location_accessibility_ratings = property(fget=get_location_accessibility_ratings)

	# may need to do something like this in the future if the lists are too slow to average
	#def get_avg_cleanliness_ratings(self):
	#	return db.session.query(func.avg(Rating.rating)).filter_by(type=0).filter_by(bathroom_id=self.id).scalar()






class Rating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rating_type = db.Column(db.Integer, nullable=False)
	"""
	The type of rating this object represents
		0 = Cleanliness
		1 = Privacy
		2 = Atmosphere
		3 = Location Accessibility
	"""
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	bathroom_id = db.Column(db.Integer, db.ForeignKey("bathroom.id"))
	rating = db.Column(db.Integer) # Must be 1-5 Inclusive

	def __init__(self, rating_type, rating):
		self.rating_type = rating_type
		self.rating = rating

class Report(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(500), nullable=False)

	bathroom_id = db.Column(db.Integer, db.ForeignKey("bathroom.id"))
