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
		u2 = User("user2", "password")
		db.session.add(u2)
		u3 = User("user3", "password")
		db.session.add(u3)

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
		
		b2 = Bathroom()
		b2.bathroom_name = "Cathedral Ground Floor Bathroom"
		b2.description = "The bathroom in the ground floor of the Cathedral of Learning"
		b2.time_availability = "24/7"
		b2.how_to_find_it = "Enter Cathedral through bottom floor entrances; walk to the center of the building.  Follow your nose"
		b2.notes = "These bathrooms are massive!  But they really aren't that good.  Be careful."
		b2.latitude = 40.444234
		b2.longitude = -79.952981
		b2.occupancy_type = 1
		b2.hand_drying_type = 1
		b2.stall_range_type = 3
		b2.gender_type = 2
		
		db.session.add(b2)

		b3 = Bathroom()
		b3.bathroom_name = "David Lawrence Hall Basement Bathroom"
		b3.description = "Lurking in the basement of David Lawrence Hall"
		b3.time_availability = "Every day 7am to 11pm"
		b3.how_to_find_it = "Walk into DL from the main doors, walk to the staircase in the center of the main hall, go down and follow the signs"
		b3.notes = "Can be very private at off-peak hours.  Not a bad place"
		b3.latitude = 40.442361
		b3.longitude = -79.955250
		b3.occupancy_type = 1
		b3.hand_drying_type = 2
		b3.stall_range_type = 2

		db.session.add(b3)

		b4 = Bathroom()
		b4.bathroom_name = "34th Floor Cathedral Premium Bathroom"
		b4.description = "Hiding on the 34th floor of the cathedral of learning is a very special private bathroom with a view fit for a king.  Also, really great bathroom overall"
		b4.time_availability = "Every day 8am to 8pm"
		b4.how_to_find_it = "Take the cathedral elevators to the 36th floor. Walk down the stairs 2 flights, enter the hallway with the water fountain. The bathroom is on the left."
		b4.notes = "This is the best bathroom on campus!  Totally premium, single-occupancy experience"
		b4.latitude = 40.444444
		b4.longitude = -79.952900
		b4.occupancy_type = 0
		b4.hand_drying_type = 2
		b4.stall_range_type = 0
		b4.gender_type = 0

		db.session.add(b4)

		cleanliness = Rating(0,1)
		cleanliness.user = u1
		cleanliness.bathroom = b1
		
		db.session.add(cleanliness)

		cleanliness = Rating(0,3)
		cleanliness.user = u2
		cleanliness.bathroom = b1
		
		db.session.add(cleanliness)

		cleanliness = Rating(0,5)
		cleanliness.user = u3
		cleanliness.bathroom = b1
		
		db.session.add(cleanliness)

		privacy = Rating(1,3)
		privacy.user = u1
		privacy.bathroom = b1
		
		db.session.add(privacy)

		privacy = Rating(1,2)
		privacy.user = u2
		privacy.bathroom = b1
		
		db.session.add(privacy)

		privacy = Rating(1,2)
		privacy.user = u3
		privacy.bathroom = b1
		
		db.session.add(privacy)

		atm = Rating(2,4)
		atm.user = u1
		atm.bathroom = b1

		db.session.add(atm)
		atm = Rating(2,4)
		atm.user = u2
		atm.bathroom = b1

		db.session.add(atm)

		atm = Rating(2,3)
		atm.user = u3
		atm.bathroom = b1

		db.session.add(atm)

		acc = Rating(3,5)
		acc.user = u1
		acc.bathroom = b1

		db.session.add(acc)
		acc = Rating(3,5)
		acc.user = u2
		acc.bathroom = b1

		db.session.add(acc)
		acc = Rating(3,4)
		acc.user = u3
		acc.bathroom = b1

		db.session.add(acc)

		#################

		cleanliness = Rating(0,1)
		cleanliness.user = u1
		cleanliness.bathroom = b2
		
		db.session.add(cleanliness)

		cleanliness = Rating(0,2)
		cleanliness.user = u2
		cleanliness.bathroom = b2
		
		db.session.add(cleanliness)

		cleanliness = Rating(0,2)
		cleanliness.user = u3
		cleanliness.bathroom = b2
		
		db.session.add(cleanliness)

		privacy = Rating(1,1)
		privacy.user = u1
		privacy.bathroom = b2
		
		db.session.add(privacy)

		privacy = Rating(1,2)
		privacy.user = u2
		privacy.bathroom = b2
		
		db.session.add(privacy)

		privacy = Rating(1,2)
		privacy.user = u3
		privacy.bathroom = b2
		
		db.session.add(privacy)

		atm = Rating(2,2)
		atm.user = u1
		atm.bathroom = b2

		db.session.add(atm)
		atm = Rating(2,2)
		atm.user = u2
		atm.bathroom = b2

		db.session.add(atm)

		atm = Rating(2,2)
		atm.user = u3
		atm.bathroom = b2

		db.session.add(atm)

		acc = Rating(3,5)
		acc.user = u1
		acc.bathroom = b2

		db.session.add(acc)
		acc = Rating(3,5)
		acc.user = u2
		acc.bathroom = b2

		db.session.add(acc)
		acc = Rating(3,4)
		acc.user = u3
		acc.bathroom = b2

		db.session.add(acc)
		#################

		cleanliness = Rating(0,4)
		cleanliness.user = u1
		cleanliness.bathroom = b3
		
		db.session.add(cleanliness)

		cleanliness = Rating(0,4)
		cleanliness.user = u2
		cleanliness.bathroom = b3
		
		db.session.add(cleanliness)

		cleanliness = Rating(0,5)
		cleanliness.user = u3
		cleanliness.bathroom = b3
		
		db.session.add(cleanliness)

		privacy = Rating(1,4)
		privacy.user = u1
		privacy.bathroom = b3
		
		db.session.add(privacy)

		privacy = Rating(1,3)
		privacy.user = u2
		privacy.bathroom = b3
		
		db.session.add(privacy)

		privacy = Rating(1,5)
		privacy.user = u3
		privacy.bathroom = b3
		
		db.session.add(privacy)

		atm = Rating(2,4)
		atm.user = u1
		atm.bathroom = b3

		db.session.add(atm)
		atm = Rating(2,3)
		atm.user = u2
		atm.bathroom = b3

		db.session.add(atm)

		atm = Rating(2,4)
		atm.user = u3
		atm.bathroom = b3

		db.session.add(atm)

		acc = Rating(3,2)
		acc.user = u1
		acc.bathroom = b3

		db.session.add(acc)
		acc = Rating(3,4)
		acc.user = u2
		acc.bathroom = b3

		db.session.add(acc)
		acc = Rating(3,3)
		acc.user = u3
		acc.bathroom = b3

		db.session.add(acc)
		#################

		cleanliness = Rating(0,4)
		cleanliness.user = u1
		cleanliness.bathroom = b4
		
		db.session.add(cleanliness)

		cleanliness = Rating(0,4)
		cleanliness.user = u2
		cleanliness.bathroom = b4
		
		db.session.add(cleanliness)

		cleanliness = Rating(0,5)
		cleanliness.user = u3
		cleanliness.bathroom = b4
		
		db.session.add(cleanliness)

		privacy = Rating(1,5)
		privacy.user = u1
		privacy.bathroom = b4
		
		db.session.add(privacy)

		privacy = Rating(1,5)
		privacy.user = u2
		privacy.bathroom = b4
		
		db.session.add(privacy)

		privacy = Rating(1,4)
		privacy.user = u3
		privacy.bathroom = b4
		
		db.session.add(privacy)

		atm = Rating(2,5)
		atm.user = u1
		atm.bathroom = b4

		db.session.add(atm)
		atm = Rating(2,5)
		atm.user = u2
		atm.bathroom = b4

		db.session.add(atm)

		atm = Rating(2,5)
		atm.user = u3
		atm.bathroom = b4

		db.session.add(atm)

		acc = Rating(3,2)
		acc.user = u1
		acc.bathroom = b4

		db.session.add(acc)
		acc = Rating(3,4)
		acc.user = u2
		acc.bathroom = b4

		db.session.add(acc)
		acc = Rating(3,4)
		acc.user = u3
		acc.bathroom = b4

		db.session.add(acc)

		#################




		#add the new objects to the database
		db.session.add(u1)
		db.session.add(b1)

		# ADD MORE DATA HERE!

		db.session.commit() # always run this at the end
		return

	# def runTests(self):
	# 	#this will run all tests automatically as long as the functions start with the name `test_`
	# 	unittest.main()
	# 	return

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