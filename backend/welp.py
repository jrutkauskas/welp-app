from model import db, User, Bathroom, Rating
from werkzeug.security import generate_password_hash, check_password_hash
#from app import db

### NOTES:
# when I talk about dictionaries of a certain type, that is NOT a python type.  In python, it is a standard dictionary
# what I mean is that it is a dictionary that follows the specification in the Types.ts file in this folder.
# this is so there can be a consistent spec between the python backend and the typescript frontend,
# and these dictionaries are easily serializable.



class WelpApp:
	def __init__(self):
		#also do error checking in here
		return
	
	# Takes in a BathroomQuery dictionary and User (database) object (for calculating user ratings)
	# on success, will return the pair (True, <arr>) where arr is an array of BathroomResponse dictionaries (may be an empty array if no bathrooms are found matching those parameters)
	# on failure, will return the pair (False, msg), where msg describes what the problem is.
	def get_bathrooms_based_on_params(self, params, user):
		if not params:
			return False, "must send parameters"
		options =  Bathroom.query
		if params["min_latitude"]:
			options = options.filter(Bathroom.latitude >=params["min_latitude"])
		if params["max_latitude"]:
			options = options.filter(Bathroom.latitude <= params["max_latitude"])
		if params["min_longitude"]:
			options = options.filter(Bathroom.longitude >=params["min_longitude"])
		if params["max_longitude"]:
			options = options.filter(Bathroom.longitude <= params["max_longitude"])
		
		if params["occupancy_type"]:
			options = options.filter(Bathroom.occupancy_type == params["occupancy_type"])
		if params["hand_drying_type"]:
			options = options.filter(Bathroom.hand_drying_type == params["hand_drying_type"])
		if params["stall_range_type"]:
			options = options.filter(Bathroom.stall_range_type == params["stall_range_type"])
		if params["gender_type"]:
			options = options.filter(Bathroom.gender_type == params["gender_type"])
		
		bathrooms = options.all()
		dic_list = []
		for b in bathrooms:
			dic = self.convert_bathroom_object_to_dictionary(b)
			dic = self.add_ratings_to_bathroom_dictionary(b, user, dic)
			dic_list.append(dic)

		
		
		return True, dic_list
	
	# Takes in the id (as an integer) of the bathroom to get (Bathroom must already exist), and a User (database) object
	# which is required for getting the user's ratings and including them
	# On success, will return a pair (True, <bathroom>) where bathroom is a BathroomResponse dictionary
	# on failure, will return a pair (False, msg) where msg is a message describing the problem
	def get_bathroom_by_id(self, id, user):
		if not id:
			return False, "must send valid id"
		bath = Bathroom.query.filter_by(id=id).first()
		if not bath:
			return False, "bathroom with that id not found"
		dic = self.convert_bathroom_object_to_dictionary(bath)
		dic = self.add_ratings_to_bathroom_dictionary(bath, user, dic)
		return True, dic
	
	# Takes in the id (as an integer) of the bathroom to set (Bathroom must already exist), and a CreateBathroomRequest dictionary (with no user ratings in there)
	# will update the existing bathroom to have all the attributes as the bathroom passed in.  No checking will occur
	# missing attributes in the dictionary will cause a failure
	# On success, will return the pair (True, <bathroom>) where bathroom is the Bathroom object connected to the database that represents
	# the bathroom that was updated (containing its new values)
	# on failure, returns pair False, msg where msg is a string message explaining what went wrong
	def set_bathroom_by_id(self, id, bathroom):
		if not id or not bathroom:
			return False, "id or dictionary missing"
		b = Bathroom.query.filter_by(id=id).first()
		if not b:
			return False, "no bathroom with that id found in database"
		b = self.copy_bathroom_dict_to_database_object(b, bathroom)
		if not b:
			return False, "couldn't copy bathroom dictionary to the database object"
		db.session.commit()
		dic = self.convert_bathroom_object_to_dictionary(b)
		#dic = self.add_ratings_to_bathroom_dictionary(b, user, dic)
		if not dic:
			return False, "couldn't get the bathroom object back into response dictionary", None
		return True, dic

	#Takes in a CreateBathroomRequest dictionary and User (database) object, creates a Bathroom database object, and adds it to the database
	# missing attributes in the dictionary will cause a failure
	# On success, will return the triple (True, <bathroom_response>, <bathroom>) where bathroom_response is a BathroomResponse dictionary
	# and bathroom is the newly-created Bathroom (database) object.
	# On failure, will return the triple (False, msg, None) where msg is a message describing what went wrong.
	def create_bathroom(self, bathroom, user):
		if not bathroom or not user:
			return False, "Invalid bathroom or user access", None
		b = Bathroom()
		b = self.copy_bathroom_dict_to_database_object(b, bathroom)
		if not self.perform_ratings_from_dictionary(b, user, bathroom):
			return False, "couldn't perform user ratings", None
		db.session.add(b)
		db.session.commit()
		dic = self.convert_bathroom_object_to_dictionary(b)
		dic = self.add_ratings_to_bathroom_dictionary(b, user, dic)
		if not dic:
			return False, "couldn't get bathroom object back into response dictionary", None
		return True, dic, b
	
	# takes AuthenticationRequest dictionary as a request to create a user
	# On success, will return the pair (True, <user>) where User is the newly created User object
	# On failure (e.g., username already exists), will return the pair (False, msg) where msg is a string message 
	# describing the problem
	def create_user(self, user):
		if not user or not user["username"] or not user["password"]:
			return False, "invalid AuthenticationRequest sent"
		exists = User.query.filter_by(username=user["username"]).first()
		if exists:
			return False, "user already exists"
		u = User(user["username"], user["password"])
		db.session.add(u)
		db.session.commit()
		return True, u
	
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
		
		b = Bathroom.query.filter_by(id=rating["bathroom_id"]).first()
		if not b:
			return (False, "bathroom with id %d not found" % rating["bathroom_id"])
		
		if not (rating["rating"] > 0 and rating["rating"] <= 5):
			return (False, "invalid rating")
		# need to check if rating already exists
		existing_rating = Rating.query.filter_by(user_id=user.id).filter_by(bathroom_id=b.id).filter_by(rating_type=int(rating["rating_type"])).first()
		if existing_rating:
			existing_rating.rating = rating["rating"]
		else:
			r = Rating(rating["rating_type"], rating["rating"])
			r.user = user
			r.bathroom = b
			db.session.add(r)
		db.session.commit()
		return True, ""
	
	#takes AuthenticationRequest dictionary as a request to authenticate a user
	# on success, returns pair (True, <User>) where User is an actual User object linked to the database of the authenticated user
	# on failure, returns pair (False, msg) where msg is a message describing the reason the user isn't able to be authenticated.
	def authenticate_user(self, authentication_request):
		if not authentication_request:
			return (False, "authentication_request is not found")
		
		auth = authentication_request
		if auth["username"] and auth["password"]:
			u = User.query.filter_by(username=auth["username"]).first()
			if not u:
				return False, "user not found"
			if check_password_hash(u.password, auth["password"]):
				return True, u
			else:
				return False, "password does not match"
		else:
			return (False, "username or password must not be empty")

	####### UTILITY METHODS BEGIN HERE #######

	# takes a Bathroom (database) object in and converts all attributes into a dictionary, similar to the BathroomResponse dictionary
	# however, this does not calculate the ratings of a user, therefore that operation must be done separately
	#on success, returns a dictionary representing the bathroom
	# on failure, (which is unlikely) will return None
	def convert_bathroom_object_to_dictionary(self, bathroom):
		if not bathroom or bathroom.id == None:
			return None
		dic = {}
		dic["id"] = bathroom.id
		dic["bathroom_name"] = bathroom.bathroom_name
		dic["description"] = bathroom.description
		dic["time_availability"] = bathroom.time_availability
		dic["notes"] = bathroom.notes
		dic["latitude"] = bathroom.latitude
		dic["longitude"] = bathroom.longitude
		dic["occupancy_type"] = bathroom.occupancy_type
		dic["hand_drying_type"] = bathroom.hand_drying_type
		dic["stall_range_type"] = bathroom.stall_range_type
		dic["gender_type"] = bathroom.gender_type
		
		# no ratings in here, remember?

		return dic

	# bathroom is a Bathroom database object, user is a User database object, dic is a partially-completed BathroomResponse dictionary.
	# this function will calculate the user ratings and add them to the dictionary.
	# on success, returns the dictionary
	# on failure, returns None
	def add_ratings_to_bathroom_dictionary(self, bathroom, user, dic):
		if not bathroom or not dic:
			return None
		clean = bathroom.get_cleanliness_ratings().all() #.filter_by(user=user)
		total = 0
		count = 0
		for r in clean:
			if r.rating:
				count = count + 1
				total = total + r.rating
		if count == 0:
			count = 1
		average_clean = total / count
		if total == 0:
			average_clean = None

		priv = bathroom.get_privacy_ratings().all() #.filter_by(user=user)
		total = 0
		count = 0
		for r in priv:
			if r.rating:
				count = count + 1
				total = total + r.rating
		if count == 0:
			count = 1
		average_priv = total / count
		if total == 0:
			average_priv = None

		atm = bathroom.get_atmosphere_ratings().all() #.filter_by(user=user)
		total = 0
		count = 0
		for r in atm:
			if r.rating:
				count = count + 1
				total = total + r.rating
		if count == 0:
			count = 1
		average_atm = total / count
		if total == 0:
			average_atm = None

		loc = bathroom.get_location_accessibility_ratings().all() #.filter_by(user=user)
		total = 0
		count = 0
		for r in loc:
			if r.rating:
				count = count + 1
				total = total + r.rating
		if count == 0:
			count = 1
		average_loc = total / count
		if total == 0:
			average_loc = None

		dic["avg_ratings"] = {"cleanliness":average_clean, "privacy":average_priv, "atmosphere":average_atm, "location_accessibility":average_loc}
		
		# get overall average
		numerator = 0
		denom = 0
		overall_avg = None
		if average_clean:
			numerator = numerator + average_clean
			denom = denom + 1
		if average_priv:
			numerator = numerator + average_priv
			denom = denom + 1
		if average_atm:
			numerator = numerator + average_atm
			denom = denom + 1
		if average_loc:
			numerator = numerator + average_loc
			denom = denom + 1
		
		if denom > 0:
			overall_avg = numerator / denom
		
		dic["avg_overall_rating"] = overall_avg
		
		

		# now get user ratings
		if user:
			clean = bathroom.get_cleanliness_ratings().filter_by(user=user).first() #.filter_by(user=user)
			uclean = None
			if clean:
				uclean = clean.rating

			priv = bathroom.get_privacy_ratings().filter_by(user=user).first() #.filter_by(user=user)
			upriv = None
			if priv:
				upriv = priv.rating

			atm = bathroom.get_atmosphere_ratings().filter_by(user=user).first() #.filter_by(user=user)
			uatm = None
			if atm:
				uatm = atm.rating

			loc = bathroom.get_location_accessibility_ratings().filter_by(user=user).first() #.filter_by(user=user)
			uloc = None
			if loc:
				uloc = loc.rating

			dic["user_ratings"] = {"cleanliness":uclean, "privacy":upriv, "atmosphere":uatm, "location_accessibility":uloc}
			
		

		

		return dic

	# bathroom is a Bathroom database object, user is a User database object, dic is a CreateBathroomRequest dictionary with user ratings in it
	# this function will create and add the needed Rating objects to the database
	# on success, returns True
	# on failure, returns False
	def perform_ratings_from_dictionary(self, bathroom, user, dic):
		if "user_ratings" in dic:
			ratings = dic["user_ratings"]

			if ratings["cleanliness"] is not None:
				clean = Rating(0, ratings["cleanliness"])
				clean.user = user
				clean.bathroom = bathroom
				db.session.add(clean)
				db.session.commit()
			
			if ratings["privacy"] is not None:
				priv = Rating(1, ratings["privacy"])
				priv.user = user
				priv.bathroom = bathroom
				db.session.add(priv)
				db.session.commit()
			
			if ratings["atmosphere"] is not None:
				atm = Rating(2, ratings["atmosphere"])
				atm.user = user
				priv.bathroom = bathroom
				db.session.add(atm)
				db.session.commit()
			
			if ratings["location_accessibility"] is not None:
				loc = Rating(3, ratings["location_accessibility"])
				loc.user = user
				loc.bathroom = bathroom
				db.session.add(loc)
				db.session.commit()


		return True


	# takes in a User (database) object, and returns a UserResponse dict on success
	# on failure, returns None
	def convert_user_to_dict(self, user):
		if user is None:
			return None
		
		dic = {}
		dic["id"] = user.id
		dic["username"] = user.username
		return dic

	# takes in a CreateBathroomRequest dictionary and a bathroom (database) object, and copies the data 
	# from the dictionary to the database object (not including any user ratings, just the simple data)
	# also does not check changing ids
	# on success, returns the bathroom (database) object
	# on failure, returns None
	def copy_bathroom_dict_to_database_object(self, bathroom, dic):
		if not bathroom or not dic:
			return None
		
		bathroom.bathroom_name = dic["bathroom_name"]
		bathroom.description = dic["description"]
		bathroom.time_availability = dic["time_availability"]
		bathroom.notes = dic["notes"]

		bathroom.latitude = dic["latitude"]
		bathroom.longitude = dic["longitude"]

		bathroom.occupancy_type = dic["occupancy_type"]
		bathroom.hand_drying_type = dic["hand_drying_type"]
		bathroom.stall_range_type = dic["stall_range_type"]
		bathroom.gender_type = dic["gender_type"]
		
		return bathroom
