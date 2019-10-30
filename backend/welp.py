from model import db, User, Bathroom, Rating
#from app import db

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
	
	# id is an integer, should return a User object
	def get_user_by_id(self, id):
		u = User.query.filter_by(id=id).first()
		if u:
			return u
		else:
			return None
		
	# rating is a RatingRequestResponse from types.ts as a dictionary
	# returns a pair (result <boolean>, msg <string>) where result is true with success, false with failure, and msg is a string describing the error
	def set_user_bathroom_rating(self, user, rating):
		r = Rating(rating["rating_type"], rating["rating"])
		r.user = user
		b = Bathroom.query.filter_by(id=rating["bathroom_id"]).first()
		if not b:
			return (False, "bathroom with id %d not found" % rating["bathroom_id"])
		r.bathroom = b
		# need to check if rating already exists
		existing_rating = Rating.query.filter_by(user_id=user.id).filter_by(bathroom_id=b.id)
		db.session.add(r)
		db.session.commit()
		return
	
	#takes auth req obj, returns user or failure
	def authenticate_user(self, authentication_request):
		return

