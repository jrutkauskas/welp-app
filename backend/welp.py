from model import User, Bathroom, Rating
from app import db

class WelpApp:
	def __init__(self):
		#also do error checking in here
		return
	
	def get_bathrooms_based_on_params(self, params, user):
		return
	
	def get_bathroom_by_id(self, id, user):
		#Bathroom.que
		return
	
	def set_bathroom_by_id(self, id, bathroom):
		return
	
	def create_user(self, user):
		return
	
	def get_user_by_id(self, id):
		u = User.query.filter_by(id=id).first()
		if u:
			return u
		else:
			return None
		
	
	def set_user_bathroom_rating(self, user, rating):
		return
	

