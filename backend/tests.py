from model import db, User, Bathroom, Rating
from welp import WelpApp
from app import *
import unittest
#from app import db
import logging as log

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
	
	
	def test_user_00(self):
		self.bootstrapDB() #tests often will require setting up the database in some way to ensure the data in there is as expected
		u = User.query.filter_by(username="user1").first() # this test is bad because it actually just tests the database
		self.assertEqual(u.username, 'user1') #all tests must assert something

	#login tests
	def test_user_01(self):	
	
		u = User("user1","password1")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user1",
			"password": "password"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)	
		self.assertEqual(user[0], True)


	def test_user_02(self):	
		#self.bootstrapDB()
		u = User("!@#$%^&*()","1234567890")
		db.session.add(u)
		AuthenticationRequest={
			"username": "!@#$%^&*()",
			"password": "1234567890"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)	
		self.assertEqual(user[0], True)

	def test_user_03(self):	
		#self.bootstrapDB()
		u = User("user1","pass word")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user1",
			"password": "pass word"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)	
		self.assertEqual(user[0], True)

	
	def test_user_04(self):	
		#self.bootstrapDB()
		u = User("user1","")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user1",
			"password": ""
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)	
		self.assertEqual(user[0], False)

	def test_user_05(self):	
		#self.bootstrapDB()
		u = User("user1","passwordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpassword")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user1",
			"password": "passwordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpassword"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)	
		self.assertEqual(user[0], False)
	
	def test_user_06(self):	
		#self.bootstrapDB()
		u = User("user name","password")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user name",
			"password": "password"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)	
		self.assertEqual(user[0], True)
	
	def test_user_07(self):	
		#self.bootstrapDB()
		u = User("","password")
		db.session.add(u)
		AuthenticationRequest={
			"username": "",
			"password": "password"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)	
		self.assertEqual(user[0], False)
	
	def test_user_08(self):	
		#self.bootstrapDB()
		u = User("usernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusername","password")
		db.session.add(u)
		AuthenticationRequest={
			"username": "usernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusernameusername",
			"password": "password"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)	
		self.assertEqual(user[0], False)
	
	def test_user_09(self):	
		#self.bootstrapDB()
		u = User("user name","pass word")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user name",
			"password": "pass word"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)	
		self.assertEqual(user[0], True)
	
	#Sign up
	
	#Try signing up as already created user
	def test_user_10(self):	
		#self.bootstrapDB()
		u = User("user1","password1")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user1",
			"password": "password"
		}
		w=WelpApp()
		user=w.create_user(AuthenticationRequest)	
		self.assertEqual(user[0], False)
	

		#Try signing up with new user
	def test_user_11(self):	
		#self.bootstrapDB()
		u = User("user1","password1")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user2",
			"password": "password2"
		}
		w=WelpApp()
		user=w.create_user(AuthenticationRequest)	
		self.assertEqual(user[0], True)
	
	def test_user_12(self):	
		#self.bootstrapDB()
		u = User("user6","password6")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user6",
			"password": "password6"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)
		user2=w.get_user_by_id(u.id)	
		self.assertEqual(user[1], user2)
		
	def test_user_13(self):	
		#self.bootstrapDB()
		u = User("user1","password")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user1",
			"password": "password"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)
		user2=w.get_user_by_id(12345)	
		self.assertNotEqual(user[1], user2)
	
	def test_user_14(self):	
		#self.bootstrapDB()
		u = User("user1","password")
		db.session.add(u)
		AuthenticationRequest={
			"username": "user1",
			"password": "password"
		}
		w=WelpApp()
		user=w.authenticate_user(AuthenticationRequest)
		user2=w.get_user_by_id()	
		self.assertNotEqual(user[1], user2)
	
	
	#Bathroom Tests
	
	def test_bathroom_01(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "6th Floor Sennott Men's Room",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 40.441513,
				"longitude":  -79.956492,
				"occupancy_type": 0,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)

	def test_bathroom_02(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 40.441513,
				"longitude":  -79.956492,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)


	def test_bathroom_03(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Realylongnameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 40.441513,
				"longitude":  -79.956492,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)


	def test_bathroom_04(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 40.441513,
				"longitude":  -79.956492,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)

	def test_bathroom_05(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "ReallyLongDescriptionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnReallyLongDescriptionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnReallyLongDescriptionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 40.441513,
				"longitude":  -79.956492,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)




	def test_bathroom_06(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 40.441513,
				"longitude":  -79.956492,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)

	def test_bathroom_07(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "ForeverrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrForeverrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 40.441513,
				"longitude":  -79.956492,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)



	def test_bathroom_08(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "",
				"latitude": 40.441513,
				"longitude":  -79.956492,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)


	def test_bathroom_09(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "LongNotesssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssLongNotesssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssLongNotesssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss",
				"latitude": 40.441513,
				"longitude":  -79.956492,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)


	def test_bathroom_10(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  181,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	
	
	def test_bathroom_11(self):	
		db.drop_all()
		db.create_all()
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude": "South Pole",
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	

	def test_bathroom_12(self):	
		db.drop_all()
		db.create_all()
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": "North Pole",
				"longitude":  180,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	
	
	def test_bathroom_13(self):	
		db.drop_all()
		db.create_all()
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 91,
				"longitude":  1,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)

	def test_bathroom_14(self):	
		db.drop_all()
		db.create_all()
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 200,
				"longitude":  200,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)

	
	def test_bathroom_15(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": NULL,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)

	def test_bathroom_15b(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
			"bathroom_name": "Name",
			"description": "A bathroom for CS champions",
			"time_availability": "M-F 9am-5pm",
			"how_to_find_it": "6th Floor Sennott Sq.",
			"notes": "It's gross",
			"latitude": 50.5,
			"longitude":  180,
			"occupancy_type": 0,
			"hand_drying_type": 3,
			"stall_range_type": 1,
			"gender_type": 0,
			"user_ratings":{
				"cleanliness": 1,
				"privacy": 1,
				"atmosphere": 1,
				"location_accessibility": 1
			}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)

	def test_bathroom_16(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)


	def test_bathroom_17(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)


	def test_bathroom_18(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": -1,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_19(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 3,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_20(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": "Single Occupancy",
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_21(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": NULL,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_22(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 0,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_23(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 1,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_24(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 2,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_25(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_26(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 4,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_27(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": "Paper towels",
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_28(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": -1,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_29(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 5,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_30(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": NULL,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_31(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 0,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_32(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_33(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 2,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_34(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 3,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_35(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": "One stall / Single Occupancy",
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_36(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": -1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_37(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_38(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": NULL,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_39(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_40(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 1,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_41(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 2,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_42(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 3,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], True)
	def test_bathroom_43(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": "Woman",
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_44(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": -1,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)
	def test_bathroom_45(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 4,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		self.assertEqual(bathroom[0], False)



	#Update bathroom
	def test_bathroom_46(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 1,
				"gender_type": 1,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		CreateBathroomRequest2={
				"bathroom_name": "Name",
				"description": "",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 0,
				"gender_type": 0
		}
		bathroom2=w.set_bathroom_by_id(bathroom[2].id,CreateBathroomRequest2)
		self.assertEqual(bathroom[0], True)
		self.assertEqual(bathroom2[0], True)

	#Search Tests

	def test_search_01(self):	
		db.drop_all()
		db.create_all()
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		bathroom2=w.get_bathroom_by_id(bathroom[2].id, u)
		self.assertEqual(bathroom2[1], bathroom[1])

	def test_search_02(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}
		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		bathroom2=w.get_bathroom_by_id(999, u)
		self.assertNotEqual(bathroom2[1], bathroom[1])

	def test_search_03(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		BathroomQuery={
			"min_latitude": 40,
			"max_latitude": 60,
			"min_longitude": 150,
			"max_longitude": 180,

			"occupancy_type": 2,
			"hand_drying_type": 3,
			"stall_range_type": 4,
			"gender_type": 0
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		bathroom2=w.get_bathrooms_based_on_params(BathroomQuery, u)
		
		self.assertEqual(bathroom2[1][0], bathroom[1])

	def test_search_04(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		BathroomQuery={
			"min_latitude": 40,
			"max_latitude": 60,
			"min_longitude": 0,
			"max_longitude": 180,

			"occupancy_type": 2,
			"hand_drying_type": 3,
			"stall_range_type": NULL,
			"gender_type": 0
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		bathroom2=w.get_bathrooms_based_on_params(BathroomQuery, u)
		
		self.assertEqual(bathroom2[1][0], bathroom[1])
	
	def test_search_05(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		BathroomQuery={
			"min_latitude": 70,
			"max_latitude": 80,
			"min_longitude": 0,
			"max_longitude": 180,

			"occupancy_type": 0,
			"hand_drying_type": 1,
			"stall_range_type": 2,
			"gender_type": 1
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		bathroom2=w.get_bathrooms_based_on_params(BathroomQuery, u)
		
		with self.assertRaises(IndexError):
			bathroom2[1][0]


	def test_search_06(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		BathroomQuery={
			"min_latitude": -10,
			"max_latitude": 200,
			"min_longitude": -5,
			"max_longitude": 180,

			"occupancy_type": -1,
			"hand_drying_type": 6,
			"stall_range_type": 2,
			"gender_type": 1
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		bathroom2=w.get_bathrooms_based_on_params(BathroomQuery, u)
		
		self.assertNotEqual(bathroom2[1][0], bathroom[1])

	def test_search_07(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		BathroomQuery={
			"min_latitude": NULL,
			"max_latitude": NULL,
			"min_longitude": NULL,
			"max_longitude": NULL,

			"occupancy_type": NULL,
			"hand_drying_type": NULL,
			"stall_range_type": NULL,
			"gender_type": NULL
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		bathroom2=w.get_bathrooms_based_on_params(BathroomQuery, u)
		
		self.assertEqual(bathroom2[1][0], bathroom[1])



	def test_search_08(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		u2= User("user2","password2")
		db.session.add(u2)

		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		BathroomQuery={
			"min_latitude": 60,
			"max_latitude": 40,
			"min_longitude": 150,
			"max_longitude": 180,

			"occupancy_type": 2,
			"hand_drying_type": 3,
			"stall_range_type": 4,
			"gender_type": 0
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		bathroom2=w.get_bathrooms_based_on_params(BathroomQuery, u)
		
		self.assertNotEqual(bathroom2[1][0], bathroom[1])



	
	def test_search_9(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
		
		self.assertEqual(bathroom[0], True)

	def test_search_10(self):	
		#self.bootstrapDB()
		#b= Bathroom()
		#db.session.add(b)
		u = User("user1","password")
		db.session.add(u)
		u2 = User("user2","password2")
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u2)
	
		
		self.assertEqual(bathroom[0], False)

	

	#Ratings Tests
	
	def test_Ratings_01(self):	
		db.drop_all()
		db.create_all()
		#self.bootstrapDB()
		u = User("user1","password")
		db.session.add(u)
		u2 = User("user2","password2")
		db.session.add(u2)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
	
		RatingRequestResponse={
			"rating_type": 0,
			"rating": 1,
			"bathroom_id": bathroom[2].id
		}

		test1 = w.set_user_bathroom_rating(u2, RatingRequestResponse)
		RatingRequestResponse2={
			"rating_type": 1,
			"rating": 2,
			"bathroom_id": bathroom[2].id
		}

		test1 = w.set_user_bathroom_rating(u2, RatingRequestResponse2)
		RatingRequestResponse3={
			"rating_type": 2,
			"rating": 4,
			"bathroom_id": bathroom[2].id
		}

		test3 = w.set_user_bathroom_rating(u2, RatingRequestResponse3)
		RatingRequestResponse4={
			"rating_type": 3,
			"rating": 5,
			"bathroom_id": bathroom[2].id
		}

		test4 = w.set_user_bathroom_rating(u2, RatingRequestResponse4)

		r0=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=0).first().rating
		r1=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=1).first().rating
		r2=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=2).first().rating
		r3=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=3).first().rating



		#b1= bathroom[2].query.fi
		b1=w.get_bathroom_by_id(bathroom[2].id, u)
		
		self.assertEqual(r0, 1)
		self.assertEqual(r1, 2)
		self.assertEqual(r2, 4)
		self.assertEqual(r3, 5)
	

	def test_Ratings_02(self):	
		#self.bootstrapDB()
		u = User("user1","password")
		db.session.add(u)
		u2 = User("user2","password2")
		db.session.add(u2)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
	
		RatingRequestResponse={
			"rating_type": 0,
			"rating": 8,
			"bathroom_id": bathroom[2].id
		}

		test1 = w.set_user_bathroom_rating(u2, RatingRequestResponse)
		RatingRequestResponse2={
			"rating_type": 1,
			"rating": -1,
			"bathroom_id": bathroom[2].id
		}

		test1 = w.set_user_bathroom_rating(u2, RatingRequestResponse2)
		RatingRequestResponse3={
			"rating_type": 2,
			"rating": 10,
			"bathroom_id": bathroom[2].id
		}

		test3 = w.set_user_bathroom_rating(u2, RatingRequestResponse3)
		RatingRequestResponse4={
			"rating_type": 3,
			"rating": 3,
			"bathroom_id": bathroom[2].id
		}

		test4 = w.set_user_bathroom_rating(u2, RatingRequestResponse4)

		r0=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=0).first().rating
		r1=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=1).first().rating
		r2=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=2).first().rating
		r3=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=3).first().rating



		#b1= bathroom[2].query.fi
		b1=w.get_bathroom_by_id(bathroom[2].id, u)
		
		self.assertNotEqual(r0, 1)
		self.assertNotEqual(r1, 2)
		self.assertNotEqual(r2, 4)
		self.assertNotEqual(r3, 5)

	def test_Ratings_03(self):	
		#self.bootstrapDB()
		db.drop_all()
		db.create_all()
		u = User("user1","password")
		db.session.add(u)
		u2 = User("user2","password2")
		db.session.add(u2)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
	
		RatingRequestResponse={
			"rating_type": 0,
			"rating": 1,
			"bathroom_id": bathroom[2].id
		}

		test1 = w.set_user_bathroom_rating(u2, RatingRequestResponse)
		RatingRequestResponse2={
			"rating_type": 1,
			"rating": 2,
			"bathroom_id": bathroom[2].id
		}

		test2 = w.set_user_bathroom_rating(u2, RatingRequestResponse2)
		RatingRequestResponse3={
			"rating_type": 2,
			"rating": 4,
			"bathroom_id": bathroom[2].id
		}

		test3 = w.set_user_bathroom_rating(u2, RatingRequestResponse3)
		RatingRequestResponse4={
			"rating_type": 3,
			"rating": 5,
			"bathroom_id": bathroom[2].id
		}

		test4 = w.set_user_bathroom_rating(u2, RatingRequestResponse4)

		r0=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=0).first().rating
		r1=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=1).first().rating
		r2=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=2).first().rating
		r3=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=3).first().rating



		#b1= bathroom[2].query.fi
		b1=w.get_bathroom_by_id(bathroom[2].id, u)
		
		self.assertEqual(b1[1].get("avg_ratings").get("cleanliness"), 1)
		self.assertEqual(b1[1].get("avg_ratings").get("privacy"), 1.5)
		self.assertEqual(b1[1].get("avg_ratings").get("atmosphere"), 2.5)
		self.assertEqual(b1[1].get("avg_ratings").get("location_accessibility"), 3)

	def test_Ratings_04(self):	
		#self.bootstrapDB()
		db.drop_all()
		db.create_all()
		u = User("user1","password")
		db.session.add(u)
		u2 = User("user2","password2")
		db.session.add(u2)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
	
		RatingRequestResponse={
			"rating_type": 0,
			"rating": NULL,
			"bathroom_id": bathroom[2].id
		}

		test1 = w.set_user_bathroom_rating(u2, RatingRequestResponse)
		RatingRequestResponse2={
			"rating_type": 1,
			"rating": NULL,
			"bathroom_id": bathroom[2].id
		}

		test2 = w.set_user_bathroom_rating(u2, RatingRequestResponse2)
		RatingRequestResponse3={
			"rating_type": 2,
			"rating": NULL,
			"bathroom_id": bathroom[2].id
		}

		test3 = w.set_user_bathroom_rating(u2, RatingRequestResponse3)
		RatingRequestResponse4={
			"rating_type": 3,
			"rating": NULL,
			"bathroom_id": bathroom[2].id
		}

		test4 = w.set_user_bathroom_rating(u2, RatingRequestResponse4)

		r0=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=0).first().rating
		r1=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=1).first().rating
		r2=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=2).first().rating
		r3=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=3).first().rating



		#b1= bathroom[2].query.fi
		b1=w.get_bathroom_by_id(bathroom[2].id, u)
		
		self.assertEqual(b1[1].get("avg_ratings").get("cleanliness"), 1)
		self.assertEqual(b1[1].get("avg_ratings").get("privacy"), 1)
		self.assertEqual(b1[1].get("avg_ratings").get("atmosphere"), 1)
		self.assertEqual(b1[1].get("avg_ratings").get("location_accessibility"), 1)

	
	def test_Ratings_05(self):	
		#self.bootstrapDB()
		db.drop_all()
		db.create_all()
		u = User("user1","password")
		db.session.add(u)
		u2 = User("user2","password2")
		db.session.add(u2)
		CreateBathroomRequest={
				"bathroom_name": "Name",
				"description": "A bathroom for CS champions",
				"time_availability": "M-F 9am-5pm",
				"how_to_find_it": "6th Floor Sennott Sq.",
				"notes": "It's gross",
				"latitude": 50.5,
				"longitude":  170,
				"occupancy_type": 2,
				"hand_drying_type": 3,
				"stall_range_type": 4,
				"gender_type": 0,
				"user_ratings":{
					"cleanliness": 1,
					"privacy": 1,
					"atmosphere": 1,
					"location_accessibility": 1
				}
		}

		w=WelpApp()
		bathroom=w.create_bathroom(CreateBathroomRequest, u)
	
		RatingRequestResponse={
			"rating_type": 0,
			"rating": 10,
			"bathroom_id": bathroom[2].id
		}

		test1 = w.set_user_bathroom_rating(u2, RatingRequestResponse)
		RatingRequestResponse2={
			"rating_type": 1,
			"rating": -5,
			"bathroom_id": bathroom[2].id
		}

		test2 = w.set_user_bathroom_rating(u2, RatingRequestResponse2)
		RatingRequestResponse3={
			"rating_type": 2,
			"rating": 0,
			"bathroom_id": bathroom[2].id
		}

		test3 = w.set_user_bathroom_rating(u2, RatingRequestResponse3)
		RatingRequestResponse4={
			"rating_type": 3,
			"rating": 6.5,
			"bathroom_id": bathroom[2].id
		}

		test4 = w.set_user_bathroom_rating(u2, RatingRequestResponse4)

		r0=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=0).first().rating
		r1=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=1).first().rating
		r2=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=2).first().rating
		r3=Rating.query.filter_by(user_id=u2.id, bathroom_id=bathroom[2].id, rating_type=3).first().rating



		#b1= bathroom[2].query.fi
		b1=w.get_bathroom_by_id(bathroom[2].id, u)
		
		self.assertNotEqual(b1[1].get("avg_ratings").get("cleanliness"), 5.5)
		self.assertNotEqual(b1[1].get("avg_ratings").get("privacy"), -2)
		self.assertNotEqual(b1[1].get("avg_ratings").get("atmosphere"), .5)
		self.assertNotEqual(b1[1].get("avg_ratings").get("location_accessibility"), 3.75)

	
	
	
	
if __name__ == '__main__':
    unittest.main()