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
		b1.bathroom_name = "6th Floor Sennott Men's Room"
		b1.description = "A bathroom for CS champions"
		b1.time_availability = "M-F 9am-5pm"
		b1.how_to_find_it = "6th Floor Sennott Sq."
		b1.notes = "It's gross"
		b1.latitude = 40.441513
		b1.longitude =  -79.956492
		b1.occupancy_type = 1
		b1.hand_drying_type = 3
		b1.stall_range_type = 1
		b1.gender_type = 0
		
		cleanliness = Rating(0,1)
		cleanliness.user = u1
		cleanliness.bathroom = b1

		privacy = Rating(1,3)
		privacy.user = u1
		privacy.bathroom = b1

		#add the new objects to the database
		db.session.add(u1)
		db.session.add(b1)
		db.session.add(cleanliness)
		db.session.add(privacy)

		# ADD MORE DATA HERE!

		db.session.commit() # always run this at the end
		return

	def runTests(self):
		#this will run all tests automatically as long as the functions start with the name `test_`
		unittest.main()
		return

	# define tests here.  This is a sample test.  It has the correct format but is actually a bad test from a design perspective
	# use this as an example of the format only
	# see https://docs.python.org/3/library/unittest.html for docs on how to write more test cases
	# the name of the test should line up with the name of the test in the Milestone Documentation
	# another note on tests: they probably shouldn't be more than 10 lines long
	# remember, a single unit test should test a single thing (or maybe just a couple) that way, if it fails
	# you know what was the problem more quickly.
	# maybe a good idea to give the test name a number in it to link to the tables of tests in the milestone description
	# also, the tests should have a good name describing what they test because the name of the function is what
	# gets printed out if the test fails
	def test_user_0(self):
		self.bootstrapDB() #tests often will require setting up the database in some way to ensure the data in there is as expected
		u = User.query.filter_by(username="user1").first() # this test is bad because it actually just tests the database
		self.assertEqual(u.username, 'user1') #all tests must assert something

if __name__ == '__main__':
    unittest.main()