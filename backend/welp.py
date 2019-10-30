from model import db, User, Bathroom, Rating
#from app import db

class WelpApp:
	def __init__(self):
		#also do error checking in here
		return
	


	# Takes in a BathroomQuery dictionary and User (database) object (for calculating user ratings)
	# on success, will return the pair (True, <arr>) where arr is an array of BathroomResponse dictionaries (may be an empty array if no bathrooms are found matching those parameters)
	# on failure, will return the pair (False, msg), where msg describes what the problem is.
	def get_bathrooms_based_on_params(self, params, user):
		return
	
	# Takes in the id (as an integer) of the bathroom to get (Bathroom must already exist), and a User (database) object
	# which is required for getting the user's ratings and including them
	# On success, will return a pair (True, <bathroom>) where bathroom is a BathroomResponse dictionary
	# on failure, will return a pair (False, msg) where msg is a message describing the problem
	def get_bathroom_by_id(self, id, user):
		#Bathroom.que
		return
	
	# Takes in the id (as an integer) of the bathroom to set (Bathroom must already exist), and a CreateBathroomRequest dictionary (with no user ratings in there)
	# will update the existing bathroom to have all the attributes as the bathroom passed in.  No checking will occur
	# missing attributes in the dictionary will cause a failure
	# On success, will return the pair (True, <bathroom>) where bathroom is the Bathroom object connected to the database that represents
	# the bathroom that was updated (containing its new values)
	def set_bathroom_by_id(self, id, bathroom):
		return

	#Takes in a CreateBathroomRequest dictionary and User (database) object, creates a Bathroom database object, and adds it to the database
	# missing attributes in the dictionary will cause a failure
	# On success, will return the triple (True, <bathroom_response>, <bathroom>) where bathroom_response is a BathroomResponse dictionary
	# and bathroom is the newly-created Bathroom (database) object.
	# On failure, will return the triple (False, msg, None) where msg is a message describing what went wrong.
	def create_bathroom(self, bathroom, user):
		return
	
	# takes AuthenticationRequest dictionary as a request to create a user
	# On success, will return the pair (True, <user>) where User is the newly created User object
	# On failure (e.g., username already exists), will return the pair (False, msg) where msg is a string message 
	# describing the problem
	def create_user(self, user):
		return
	
	# id is an integer, should return a User object
	# Will return None if a user with that ID is not found
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
		existing_rating = Rating.query.filter_by(user_id=user.id).filter_by(bathroom_id=b.id).filter_by(rating_type=rating["rating_type"]).first()
		if existing_rating:
			existing_rating.rating = rating["rating"]
		else:
			db.session.add(r)
		db.session.commit()
		return
	
	#takes AuthenticationRequest dictionary as a request to authenticate a user
	# on success, returns pair (True, <User>) where User is an actual User object linked to the database of the authenticated user
	# on failure, returns pair (False, msg) where msg is a message describing the reason the user isn't able to be authenticated.
	def authenticate_user(self, authentication_request):
		return

	####### UTILITY METHODS BEGIN HERE #######

	# takes a Bathroom (database) object in and converts all attributes into a dictionary, similar to the BathroomResponse dictionary
	# however, this does not calculate the ratings of a user, therefore that operation must be done separately
	#on success, returns a dictionary representing the bathroom
	# on failure, (which is unlikely) will return None
	def convert_bathroom_object_to_dictionary(self, bathroom):
		return

	# bathroom is a Bathroom database object, user is a User database object, dict is a partially-completed BathroomResponse dictionary.
	# this function will calculate the user ratings and add them to the dictionary.
	# on success, returns the dictionary
	# on failure, returns None
	def add_ratings_to_bathroom_dictionary(self, bathroom, user, dict):
		return

	# bathroom is a Bathroom database object, user is a User database object, dict is a BathroomCreateResquest dictionary with user ratings in it
	# this function will create and add the needed Rating objects to the database
	# on success, returns True
	# on failure, returns False
	def perform_ratings_from_dictionary(self, bathroom, user, dict):
		return
