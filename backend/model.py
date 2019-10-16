from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(250), nullable=False)
	
	key = db.Column(db.String(30), unique=True)

	#spectacles = db.relationship("Spectacle", backref="user", lazy="select")

	def __init__(self, username, password):
		self.email = email
		self.username = username
		self.password = generate_password_hash(password)