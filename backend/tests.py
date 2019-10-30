from model import db, User, Bathroom, Rating
#from welp import WelpApp
import unittest
#from app import db


# to test, run `flask test` in your command line
class WelpTester(unittest.TestCase):
	
	
	def bootstrapDB(self):
		#should fill the database with a smattering of test data for the frontend tests, for example.
		#including a handful of bathrooms, a handful of users, and a handful of ratings

		db.drop_all()
		db.create_all()

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
		unittest.main()
		return

	# define tests here.  This is a sample test.  It has the correct format but is actually a bad test from a design perspective
	# use this as an example of the format only
	# see https://docs.python.org/3/library/unittest.html for docs on how to write more test cases
	def test_user(self):
		self.bootstrapDB()
		u = User.query.filter_by(username="user1").first()
		self.assertEqual(u.username, 'user1')

if __name__ == '__main__':
    unittest.main()