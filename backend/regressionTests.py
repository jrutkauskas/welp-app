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

		report = Report()
		report.bathroom = b3
		report.description="This bathroom has been permanently closed; It should be deleted, please."
		report.description = "I don't remember using this bathroom. I remember walking there, and pushing open the door, and I remember leaving, but I dont remember using it. But I cant not use it. Every time I try to use a bathroom, all the stall are locked, or its closed, or locked. And every day I use this bathroom again. Atleast I think I do. Whenever I need to use a bathroom, I've run around looking. The one at my house is broken, and my landlord wont fix it. He says he came over 3 times to check it, and it worked fine every time, and you have to stop texting me your bathroom works I think you might need some help but I dont need help Im not crazy it doesnt work and the only one that works is this one but this bathroom doesnt exist. Ive asked. Noone else has ever used it. And theres not even any signs on it that is is a bathroom. Just a door, equaldistant on the left side of the floor to the right side, where the woman's bathroom is. But there is no plaque that says Mens Bathroom. No figure of a man. Just a door. Im not sure I know its a bathroom. I just enter, and leave, and I dont need to go to the bathroom anymore. But when I think about it I get   itchy.  I cant remember the inside, but when I try to think I get nothing. But my body feels things. Like you can feel the memory of pain. But it doesnt hurt. Just itches. I can feel fingers. In my hair on my stomach in my mouth. They tickle and it giggles and my eyes can feel me looking at a mirror with too many fingers with too many joins reaching from behind me where  cannot see and I cannot turn around and cannot move I cannot giggle from the tickling or it will know that I see it know that I know and then it will squeeze and then it will hurt and it reaches in in my skin and I feel it tickle inside and im laughing now im laughing now and its laughing now and I see its eyes its looming over me in the mirror and I see and it makes my eyes tickle and I have to giggle have to stratch but my hands not to it so I use its hands and I scratch and scratch and scratch and scratch and it feels good the realef so go and a laugh with too many teeth and wiggle my fingers with too many joints and look at my eyes that make the walls itch the mirror itch the sink itch the stalls itch the toilet itch and I take my hands from my eyes and I see blood. My eyes are gone now. I cant see. I was taken to the hospital. Apparently I scratched my eyes out. Theres just holes there. I cant see. Im blind. My parents are downstairs. Calling a dr. Asking whats wrong with me. Why I did this to myself. Whats wrong with him why does he only smile. He should be in pain but he smiles he said he doesnt itch anymore. Please, what should we do. He needs help. Why did he do that to his eyes. Why wont he go to the bathroom. We lead him to the bathroom but he does not use it he says hes not itchy. But I sill go. I sneak out at night. To got to this bathroom. So when anybody comes in I can scratch them scratch their itch. And they cry but im trying to help so i make them comeback when they run and make them forget so theyll come so i can scratch becuase when I look at them with i itch so they must itch so i need to help becuase i need to stop itching help me stop itching this bathroom doest exist there isnt a door there was never a door im looking at the wall with my eyes where the door should be and its gone but i itch and i need to scratch but i cant so i need it to scratch let me in I need to use this bathroom put the door back put it back put it back make the bathroom again i need it i need it it wants to help i need those fingers because mine not have enough joints cant get deep enough cant go below so let me in let me in why did you get rid of the bathroom you bastard put it back put it back put it back put it back put it back put it back put it back put it back put it back put it back put it back put it back put it back put it back"
		db.session.add(report)

		admin = User("admin", "chang")
		admin.isAdmin = True
		db.session.add(admin)
		


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
	

	###Admin Tests

	#Create New Admin
	def test_admin_01(self):	
		db.drop_all()
		db.create_all()
		 
		testAdmin = User("Joey", "Weiss")
		testAdmin.isAdmin = True
		db.session.add(testAdmin)

		w=WelpApp()		
		test = w.convert_user_to_dict(testAdmin)
		self.assertEqual(test.get("isAdmin"), True)
	
	#Create Non Admin
	def test_admin_02(self):	
		db.drop_all()
		db.create_all()
		 
		testAdmin = User("J.R.", "Rutkauskas")
		testAdmin.isAdmin = False
		db.session.add(testAdmin)

		w=WelpApp()		
		test = w.convert_user_to_dict(testAdmin)
		self.assertEqual(test.get("isAdmin"), None)


	#Turn nonAdmin into admin
	def test_admin_03(self):	
		db.drop_all()
		db.create_all()
		 
		testAdmin = User("Lena", "DeJanco")
		db.session.add(testAdmin)

		w=WelpApp()		
		test = w.convert_user_to_dict(testAdmin)
		self.assertEqual(test.get("isAdmin"), None)

		testAdmin.isAdmin = True
		test2 = w.convert_user_to_dict(testAdmin)
		self.assertEqual(test2.get("isAdmin"), True)


	#Turn admin into nonAdmin
	def test_admin_04(self):	
		db.drop_all()
		db.create_all()
		 
		testAdmin = User("Emily", "Higgs")
		testAdmin.isAdmin = True
		db.session.add(testAdmin)

		w=WelpApp()		
		test = w.convert_user_to_dict(testAdmin)
		self.assertEqual(test.get("isAdmin"), True)

		testAdmin.isAdmin = False
		test2 = w.convert_user_to_dict(testAdmin)
		self.assertEqual(test2.get("isAdmin"), None)



	###Deleting Bathroom

	#Try to delete bathroom
	def test_delete_01(self):	
		db.drop_all()
		db.create_all()
		 
		testAdmin = User("Joey", "Weiss")
		testAdmin.isAdmin = True
		db.session.add(testAdmin)

		w=WelpApp()		
		test = w.convert_user_to_dict(testAdmin)

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
		bathroom=w.create_bathroom(CreateBathroomRequest, testAdmin)
		deleted = w.delete_bathroom_by_id(bathroom[2].id)
		self.assertEqual(deleted, True)
		testDeletion = w.get_bathroom_by_id(bathroom[1].get("id"), testAdmin)
		self.assertEqual(testDeletion[0], False)

	
	#Try to delete non existant bathroom
	def test_delete_02(self):	
		
		 
		testAdmin = User("Joey", "Weiss")
		testAdmin.isAdmin = False
		db.session.add(testAdmin)

		w=WelpApp()		
		test = w.convert_user_to_dict(testAdmin)

		w=WelpApp()
		deleted = w.delete_bathroom_by_id(12345)
		self.assertEqual(deleted, False)
	
	
	###Create Report
	#For existant bathroom
	def test_report_01(self):
	


		testUser = User("Joey","Weiss")
		db.session.add(testUser)
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
		bathroom=w.create_bathroom(CreateBathroomRequest, testUser)
		report = Report()
		report.bathroom = bathroom[2]
		report.description = "This bathroom is on fire. I'm in it. Pls help."
		db.session.add(report)
		testReport= w.get_reports()

		bathroomReport = Bathroom.query.filter_by(id=bathroom[2].id).first().reports

		self.assertEqual(report, bathroomReport[0])

	
	#For nonexistant bathroom
	def test_report_02(self):
		testUser = User("Joey","Weiss")
		db.session.add(testUser)
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
		bathroom=w.create_bathroom(CreateBathroomRequest, testUser)
	
		report = Report()
		report.bathroom = None
		report.description = "This bathroom has been permanently closed; It should be deleted, please."
		db.session.add(report)
		testReport= w.get_reports()
		bathroomReport = Bathroom.query.filter_by(id=bathroom[2].id).first().reports
		with self.assertRaises(IndexError):
				self.assertEqual(bathroomReport[0], None)

	
	###Get Report
	def test_report_03(self):
		

		u = User("user2","password2")
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
	
		report = Report()
		report.bathroom = bathroom[2]
		report.description = "This bathroom is on fire. I'm in it. Pls help."
		db.session.add(report)
		testReport= w.get_reports()

		self.assertEqual(report.id, testReport[2].get("id"))

	###Delete Report

	def test_report_04(self):

		testUser = User("Joey","Weiss")
		db.session.add(testUser)
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
		bathroom=w.create_bathroom(CreateBathroomRequest, testUser)
		report = Report()
		report.bathroom = bathroom[2]
		report.description = "This bathroom is on fire. I'm in it. Pls help."
		db.session.add(report)
		testReport= w.get_reports()

		bathroomReport = Bathroom.query.filter_by(id=bathroom[2].id).first().reports

		self.assertEqual(report, bathroomReport[0])

		w.delete_report_by_id(report.id)


		bathroomReport = Bathroom.query.filter_by(id=bathroom[2].id).first().reports
		with self.assertRaises(IndexError):
				self.assertEqual(bathroomReport[0], None)

	#Try to delete non existant report
	def test_report_05(self):

		testUser = User("Joey","Weiss")
		db.session.add(testUser)
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
		bathroom=w.create_bathroom(CreateBathroomRequest, testUser)
		report = Report()
		report.bathroom = bathroom[2]
		report.description = "This bathroom is on fire. I'm in it. Pls help."
		#db.session.add(report)
		#testReport= w.get_reports()

		#bathroomReport = Bathroom.query.filter_by(id=bathroom[2].id).first().reports

		#self.assertEqual(report, bathroomReport[0])

		test = w.delete_report_by_id(report.id)


		#bathroomReport = Bathroom.query.filter_by(id=bathroom[2].id).first().reports
		
		self.assertEqual(test, False)

if __name__ == '__main__':
    unittest.main()