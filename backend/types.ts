// returned from GET /api/bathrooms/<id>
export class BathroomResponse {
	id: Number; //The id of the bathroom, will be an integer
	bathroom_name: String; // The string of the bathroom's name.  Max 120 characters
	description: String; // A longer description of the bathroom.  Max 600 characters
	time_availability: String; // The times when the bathroom is available for use.  Max 300 characters
	notes: String; // A place for notes about a bathroom.  Max 600 characters

	latitude: Number; // A float/double representing the latitude of a bathroom
	longitude: Number; // a float/double representing the longitude of a bathroom

	occupancy_type: Number | null; //Essentially a dropdown box/categorical-type data
	/*
	Type of occupancy in the bathroom
		NULL = Blank
		0 = Single Occupancy
		1 = Multiple Occupancy
		2 = Other
	*/
	
	hand_drying_type: Number | null;
	/*
	Type of hand-drying available in the bathroom
		NULL = Blank
		0 = Paper Towels
		1 = Electric Hand Dryer
		2 = Electric Hand Dryer AND Paper Towels
		3 = None available
		4 = Other
	*/

	stall_range_type: Number | null;
	/*
	Range type for amount of stalls available / capacity
		NULL = Blank
		0 = One Stall / Single Occupancy
		1 = 2-3 Stalls
		2 = 4-7 Stalls
		3 = 8+ Stalls
	*/

	gender_type: Number | null;
	/*
	Range type for the genders allowed to use this bathroom
		NULL = Blank
		0 = Gender Agnostic
		1 = Men
		2 = Women
		3 = Other
	*/

	// Pre-calculated averages of ratings to display/use for sorting
	avg_ratings: {
		cleanliness: Number | null; // Will be a float 1.0-5.0 inclusive or null if no ratings have been provided
		privacy: Number | null; // ^^
		atmosphere: Number | null; // ^^
		location_accessibility: Number | null; // ^^
	}
	avg_overall_rating: Number | null; // calculated as a simple mean of the above ratings (ignoring nulls).  Will be null if there are no ratings
	// A user's custom ratings will not override this average overall

	// Custom ratings given by users.  Same rules as above.  Should override the display
	user_ratings: {
		cleanliness: Number | null;
		privacy: Number | null;
		atmosphere: Number | null;
		location_accessibility: Number | null;
	}
}

// creating a bathroom; POSTed to /api/bathrooms
// Also used for updating a bathroom by POSTing to api/bathrooms/<id> (though user_ratings sub-object shouldn't be used for that)
export class CreateBathroomRequest {
	bathroom_name: String; // The string of the bathroom's name.  Max 120 characters
	description: String; // A longer description of the bathroom.  Max 600 characters
	time_availability: String; // The times when the bathroom is available for use.  Max 300 characters
	notes: String; // A place for notes about a bathroom.  Max 600 characters

	latitude: Number; // A float/double representing the latitude of a bathroom
	longitude: Number; // a float/double representing the longitude of a bathroom

	occupancy_type: Number | null; //Essentially a dropdown box/categorical-type data
	/*
	Type of occupancy in the bathroom
		NULL = Blank
		0 = Single Occupancy
		1 = Multiple Occupancy
		2 = Other
	*/
	
	hand_drying_type: Number | null;
	/*
	Type of hand-drying available in the bathroom
		NULL = Blank
		0 = Paper Towels
		1 = Electric Hand Dryer
		2 = Electric Hand Dryer AND Paper Towels
		3 = None available
		4 = Other
	*/

	stall_range_type: Number | null;
	/*
	Range type for amount of stalls available / capacity
		NULL = Blank
		0 = One Stall / Single Occupancy
		1 = 2-3 Stalls
		2 = 4-7 Stalls
		3 = 8+ Stalls
	*/

	gender_type: Number | null;
	/*
	Range type for the genders allowed to use this bathroom
		NULL = Blank
		0 = Gender Agnostic
		1 = Men
		2 = Women
		3 = Other
	*/


	// Custom ratings given by users.  (If they rate them whle creating a new bathroom).  Don't use this if you're updating a bathroom
	user_ratings: {
		cleanliness: Number | null;
		privacy: Number | null;
		atmosphere: Number | null;
		location_accessibility: Number | null;
	}
}
// Returned from /api/users/<id>
export class UserResponse {
	id: Number; //The id of the user
	username: String; // Max 50 Characters
}


// POSTed to /api/users/<id>/ratings to rate a bathroom where <id> is your current user ID
// success returns 201 Created
// failure returns 404 Not Found
export class RatingRequestResponse {
	rating_type: Number;
	/*
		The type of rating this object represents
		0 = Cleanliness
		1 = Privacy
		2 = Atmosphere
		3 = Location Accessibility
	*/
	rating: Number | null; //Must be integer 1-5 or null for clearing a rating
	bathroom_id: Number; //integer of the id of the bathroom being rated
}
// CURRENTLY WILL NOT BE IMPLEMENTED SINCE BATHROOMS ALREADY GIVE THE RATINGS:
// IGNORE: GETing /api/users/<id>/ratings?QUERY_PARAMS will return an array of RatingRequestResponses meeting the request parameters




// to authenticate:
// Post json to /api/authenticate. or /api/users to create an account
export class AuthenticationRequest {
	username: String; // Max 50 Characters
	password: String; // Will be hashed, length doesn't matter but maybe limit to a reasonable 2000 characters if possible
}
// Will either return 403 forbidden if username and password aren't found
// otherwise returns 200 OK and a UserResponse object of the user
// We may need to modify in the future to have API keys, but I was hoping that just using SESSIONs would work well enough
// So you'll need to make sure you have cookies enabled and working and you handle the cookies you receive from your api.  I think the 
// way I'm doing it will force sessions to go through the browser


// For searching for bathrooms:
// You'll need to use this in json
// POST this to /api/bathrooms, you'll get an array of BathroomResponse objects back (could be empty if no bathrooms meet response)
export class BathroomQuery {
	//rectangle of view-window
	min_latitude: Number;
	max_latitude: Number;
	min_longitude: Number;
	max_longitude: Number;

	occupancy_type: Number | null;
	hand_drying_type: Number | null;
	stall_range_type: Number | null;
	gender_type: Number | null;

}


