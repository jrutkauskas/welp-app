// returned from /api/bathrooms/<id>
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

	//TODO FINISH
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
// GETing /api/users/<id>/ratings?QUERY_PARAMS will return an array of RatingRequestResponses meeting the request parameters




// to authenticate:
// Post json to /api/authenticate
export class AuthenticationRequest {
	username: String; // Max 50 Characters
	password: String; // Will be hashed, length doesn't matter but maybe limit to a reasonable 2000 characters if possible
}
// Will either return 403 forbidden if username and password aren't found
// otherwise returns 200 OK and a UserResponse object of the user
// We may need to modify in the future to have API keys, but I was hoping that just using SESSIONs would work well enough
// So you'll need to make sure you have cookies enabled and working and you handle the cookies you receive from your api.  I think the 
// way I'm doing it will force sessions to go


