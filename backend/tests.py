from model import User, Bathroom, Rating
from app import db

class WelpTester:
	def __init__(self):
		return
	
	def bootstrapDB(self):
		#db = self.db
		#should fill the database with a smattering of test data for the frontend tests, for example.
		#including a handful of bathrooms, a handful of users, and a handful of ratings
		u1 = User("user1","password")

		b1 = Bathroom()
		b1.bathroom_name = "Test Bathroom"
		b1.description = "A sample test bathroom"
		b1.time_availability = "M-F 9am-5pm"
		b1.how_to_find_it = "6th Floor Sennott Sq."
		b1.notes = "It's gross"
		b1.latitude = 40.441513
		b1.longitude =  -79.956492
		b1.occupancy_type = 0
		b1.hand_drying_type = 3
		b1.stall_range_type = 1
		b1.gender_type = 0
		
		cleanliness = Rating(0,1)
		cleanliness.user = u1
		cleanliness.bathroom = b1

		privacy = Rating(1,3)
		privacy.user = u1
		privacy.bathroom = b1

		db.session.add(u1)
		db.session.add(b1)
		db.session.add(cleanliness)
		db.session.add(privacy)
		db.session.commit()
		return
	def runTests(self):
		#should run all tests
		return

	# define tests here