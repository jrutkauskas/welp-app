
new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: () => ({
      logInUsername: "",
      logInPass: "",
      registerUsername: "",
      registerPass: "",
      registerPassAgain: "",

      loggedIn: false,
      userID: -1,

      loginDialog: false,
      bathroomDialog: false,
      filterPopup: false,

      pinOnMap: false, 
      pin: null, //This is the pin that the user uses to select the area of the new bathroom. 

      map: null,
      layerGroup : null,
      xCoordinate: 40.444, //Initially set the map's center on the Cathedral of Learning.
      yCoordinate: -79.953,

      bathroomViewed: null,
      bathroomsToDisplay: [],


      editingBathroom: false,
      bathroomEdited: null,

      loginCaption: "",
      cleanlinessToDisplay: null,
      privacyToDisplay: null,
      accessibilityToDisplay: null,
      atmosphereToDisplay: null,

    }),
    computed: {
      genderCaption: function () {
        switch(this.bathroomViewed.gender_type) {
          case 0:
            return "Gender Agnostic";
          case 1:
            return "Men";
          case 2:
            return "Women";
          case 3:
            return "Other";
          default:
            return "";  
        }
      },
      occupancyCaption: function () {
        switch(this.bathroomViewed.occupancy_type) {
          case 0:
            return "Single Occupancy";
          case 1:
            return "Multiple Occupancy";
          case 2:
            return "Other";
          default:
              return "";  
        }
      },
      stallNumberCaption: function () {
        switch(this.bathroomViewed.stall_range_type) {
          case 0:
            return "One Stall";
          case 1:
            return "2-3 Stalls";
          case 2:
            return "4-7 Stalls";
          case 3:
            return "8+ Stalls";
          default:
            return "";  
        }
      },
      handDryingCaption: function () {
        switch(this.bathroomViewed.hand_drying_type) {
          case 0:
            return "Paper Towels";
          case 1:
            return "Electric Hand Dryer";
          case 2:
            return "Electric Hand Dryer AND Paper Towels";
          case 3:
            return "None Available";
          case 4:
            return "Other";
          default:
              return "";  
        }
      }
    },

    methods: {

      //Determine whether to show a user's personal ratings or the average rating for a bathroom's features.
      setRatingsToDisplay : function() {
        //If this user has rated cleanliness, display this user's rating. 
        if(this.bathroomViewed.user_ratings.cleanliness !== null)
          this.cleanlinessToDisplay = this.bathroomViewed.user_ratings.cleanliness;
        else
          this.cleanlinessToDisplay = this.bathroomViewed.avg_ratings.cleanliness;
        
        //If this user has rated privacy, display this user's rating. 
        if(this.bathroomViewed.user_ratings.privacy !== null)
          this.privacyToDisplay = this.bathroomViewed.user_ratings.privacy;
        else
          this.privacyToDisplay = this.bathroomViewed.avg_ratings.privacy;

          //If this user has rated accessibility, display this user's rating. 
        if(this.bathroomViewed.user_ratings.accessibility !== null)
          this.accessibilityToDisplay = this.bathroomViewed.user_ratings.accessibility;
        else
          this.acessibilityToDisplay = this.bathroomViewed.avg_ratings.accessibility;

        //If this user has rated atmosphere, display this user's rating. 
        if(this.bathroomViewed.user_ratings.atmosphere !== null)
          this.atmosphereToDisplay = this.bathroomViewed.user_ratings.atmosphere;
        else
          this.atmosphereToDisplay = this.bathroomViewed.avg_ratings.atmosphere;
      },
      loadBathrooms : function() {
          var min_lat, max_lat, min_lon, max_lon, o_type, hd_type, sr_type, g_type;

          //Convert strings for each search criteria back into numbers.
          if(this.bathroomViewed !== null) {
            hd_type = this.convertHandDrying(this.bathroomViewed.hand_drying_type);
            o_type = this.convertOccupancy(this.bathroomViewed.occupancy_type);
            sr_type = this.convertStallRange(this.bathroomViewed.stall_range_type);
            g_type = this.convertGender(this.bathroomViewed.gender_type);
          //If this is the initial load, then all of the search criteria should be null.
          } else {
            hd_type = null;
            o_type = null;
            sr_type = null;
            g_type = null;
          }

          //Get min and max for latitude and longitude.
          min_lat = this.map.getBounds().getSouth();
          max_lat = this.map.getBounds().getNorth();
          min_lon = this.map.getBounds().getWest();
          max_lon = this.map.getBounds().getEast();


          //If this is a single-occupancy bathroom, then there's only one stall.
          if(o_type === 0)
            sr_type = 0;

          //In case this was a search from the user filter, make sure to close that popup.
          this.filterPopup = false;

          //Clear the list of bathrooms before repopulating it.
          this.bathroomsToDisplay = [];
          

          //Make the POST call to the backend.
          //  axios.post('/api/getbathrooms', {
          //       min_latitude: min_lat,
          //       max_latitude: max_lat,
          //       min_longitude: min_lon,
          //       max_longitude: max_lon,
            
          //       occupancy_type: o_type,
          //       hand_drying_type: hd_type,
          //       stall_range_type: sr_type,
          //       gender_type: g_type,
          //  })
          //  .then(response => {
          //       //Convert JSON to object array.
          //       var bathArray = JSON.parse(response);

          //       //Sort this array by average rating, descending.
          //       bathArray.sort((a, b) => (a.avg_overall_rating > b.avg_overall_rating) ? -1 : 1);

          //       for(obj of bathArray) {
          //         this.bathroomsToDisplay.push(obj);
          //       }

          //       //Clear all the old markers.
          //       this.layerGroup.clearLayers();

          //       //Then add markers on the map for each bathroom. 
          //       for(bathroom of this.bathroomsToDisplay) {
          //         L.marker([bathroom.longitude, bathroom.latitude], {title: bathroom.bathroom_name}).addTo(this.layerGroup).on('click', function(e) {
          //           //If possible, open dialog directly.
          //         });
          //       }
          //   })
          //  .catch(e => {
          //     console.log("Failed to load bathrooms from server.");
          //  })
          
           //Test bathrooms
          var bathArray = [{bathroom_name: "no", longitude: 40.445, latitude: -79.957, avg_overall_rating: 3,
            user_ratings: {
              cleanliness: null,
              privacy: null,
              atmosphere: null,
              location_accessibility: null,
            },
            avg_ratings: {
              cleanliness: null, // Will be a float 1.0-5.0 inclusive or null if no ratings have been provided
              privacy: null, 
              atmosphere: null,
              location_accessibility: null, 
            }
          }, {bathroom_name: "2", id: 1, longitude: 40.449, latitude: -79.951, avg_overall_rating: 5,
            user_ratings: {
              cleanliness: null,
              privacy: null,
              atmosphere: null,
              location_accessibility: null,
            },
            avg_ratings: {
              cleanliness: null, // Will be a float 1.0-5.0 inclusive or null if no ratings have been provided
              privacy: null, 
              atmosphere: null,
              location_accessibility: null, 
            }
          }, {bathroom_name: "3", longitude: 40.447, latitude: -79.963, avg_overall_rating: 4.5,
            user_ratings: {
              cleanliness: null,
              privacy: null,
              atmosphere: null,
              location_accessibility: null,
            },
            avg_ratings: {
              cleanliness: null, // Will be a float 1.0-5.0 inclusive or null if no ratings have been provided
              privacy: null, 
              atmosphere: null,
              location_accessibility: null, 
            }
          }, {bathroom_name: "8", longitude: 40.447, latitude: -79.963, avg_overall_rating: 4.5,
          user_ratings: {
            cleanliness: null,
            privacy: null,
            atmosphere: null,
            location_accessibility: null,
          },
          avg_ratings: {
            cleanliness: null, // Will be a float 1.0-5.0 inclusive or null if no ratings have been provided
            privacy: null, 
            atmosphere: null,
            location_accessibility: null, 
          }
        }, {bathroom_name: "7", longitude: 40.447, latitude: -79.963, avg_overall_rating: 4.5,
        user_ratings: {
          cleanliness: null,
          privacy: null,
          atmosphere: null,
          location_accessibility: null,
        },
        avg_ratings: {
          cleanliness: null, // Will be a float 1.0-5.0 inclusive or null if no ratings have been provided
          privacy: null, 
          atmosphere: null,
          location_accessibility: null, 
        }
      }, {bathroom_name: "28,000,000", longitude: 40.447, latitude: -79.963, avg_overall_rating: 4.5,
          user_ratings: {
            cleanliness: null,
            privacy: null,
            atmosphere: null,
            location_accessibility: null,
          },
          avg_ratings: {
            cleanliness: null, // Will be a float 1.0-5.0 inclusive or null if no ratings have been provided
            privacy: null, 
            atmosphere: null,
            location_accessibility: null, 
          }
        }, {bathroom_name: "helloooo", longitude: 40.447, latitude: -79.963, avg_overall_rating: 4.5,
        user_ratings: {
          cleanliness: null,
          privacy: null,
          atmosphere: null,
          location_accessibility: null,
        },
        avg_ratings: {
          cleanliness: null, // Will be a float 1.0-5.0 inclusive or null if no ratings have been provided
          privacy: null, 
          atmosphere: null,
          location_accessibility: null, 
        }

          }];

          for(obj of bathArray) {
            this.bathroomsToDisplay.push(obj);
          }

          //Clear all the old markers.
          this.layerGroup.clearLayers();

          //Then add markers on the map for each bathroom. 
          for(bathroom of this.bathroomsToDisplay) {
            L.marker([bathroom.longitude, bathroom.latitude], {title: bathroom.bathroom_name}).addTo(this.layerGroup).on('click', function(e) {
              //If possible, open dialog directly.
            });
          }

          
      },
      displayBathroomFromList : function(bathroom) {

        this.bathroomViewed = bathroom;

        //If this is a logged in user, determine which cleanliness, privacy, etc ratings to display-
        //their own or the average for all users.
        if(this.loggedIn)
          this.setRatingsToDisplay();

        //Make sure that the pin used for adding a new bathroom is removed from the map. 
        if(this.pin !== null) {
          this.pin.remove();
          this.pin = null;
          this.pinOnMap = false;
        }

        this.bathroomDialog = true;
      },

      login : function() {
        if(this.logInUsername === "" || this.logInPass === "")
          this.loginCaption = "Make sure you enter both a username and password.";
        else {
          //Make request to backend via POST. 
          axios.post('/api/authenticate', {

            username: this.logInUsername,
            password: this.logInPass

          })
          .then(function (response) {
            var json = JSON.parse(response);

            this.loggedIn = true;
            this.loginCaption = "";
            this.logInUsername = "";
            this.registerUsername = "";
            this.logInPass = "";
            this.registerPass = "";
            this.registerPassAgain = "";

            this.loginDialog = false;
            this.userID = json.id;
            return;
          })
          .catch(function (error) {
            console.log(error);
            

          });

          this.loginCaption = "Login Failed- Check your password and try again";
        }
      
      },

      dropPin : function() {
        //Let user add pin to map.

        this.pin = L.marker(this.map.getCenter(),{
          draggable: true
        }).addTo(this.map);
        
        this.pinOnMap = true;
      },

      addBathroom : function() {
        
        this.pinOnMap = false;

        //Save pin's coordinates to new bathroom obj. 
        if(this.pin !== null)
          var latlon = this.pin.getLatLng();

        var newBathroom = {

          id: -1,
          bathroom_name: "",
          description: "",
          time_availability: "",
          notes: "",

          latitude: latlon.lat,
          longitude: latlon.lng,

	        occupancy_type: null,
          hand_drying_type: null,
          stall_range_type: null,
          gender_type: null,

          // Custom ratings given by users.  (If they rate them whle creating a new bathroom).  Don't use this if you're updating a bathroom
          user_ratings: {
            cleanliness: null,
            privacy: null,
            atmosphere: null,
            location_accessibility: null,
          }
        };

        this.bathroomEdited = newBathroom;

        //Remove pin from map. 
        this.pin.remove();
        this.pin = null;

        this.editingBathroom = true;
        this.bathroomDialog = true;
      },

      registerUser : function(user, pass, passAgain) {

        //Ensure the user has entered both a username and password.
        if(this.registerUsername === "" || this.registerPass === "")
          this.loginCaption = "Make sure you enter both a username and password.";
        //Ensure the user has entered matching passwords.
        else if(this.registerPass !== this.registerPassAgain)
          this.loginCaption = "Make sure your passwords match.";

        //Try to register this user.
        else {
          axios.post('/api/users', {

            username: this.registerUsername,
            password: this.registerPass
          })
          .then(function (response) {
            var json = JSON.parse(response);

            //Clear out all the login/registration info.
            this.loginCaption = "";
            this.logInUsername = "";
            this.registerUsername = "";
            this.logInPass = "";
            this.registerPass = "";
            this.registerPassAgain = "";

            this.loggedIn = true;
            this.loginDialog = false;
            this.userID = json.id;
            return;
          })
          .catch(function (error) {
            console.log(error);

  
          });

          //Show error message on screen.
          this.loginCaption = "User registration failed";
        }
        
      },

      //Switch the view bathroom dialog to the edit bathroom dialog.
      editBathroom : function() {
        this.bathroomEdited = this.bathroomViewed;
        this.editingBathroom = true;
      },

      //Exit the edit or view bathroom dialogs.
      exitBathroom: function() {
        this.editingBathroom = false;
        this.bathroomDialog = false;
      },

      //Save either an edited bathroom or a newly created bathroom.
      saveBathroom : function() {

        //Convert features from strings to numbers amenable to the DB.
        this.bathroomEdited.hand_drying_type = this.convertHandDrying(this.bathroomEdited.hand_drying_type);
        this.bathroomEdited.occupancy_type = this.convertOccupancy(this.bathroomEdited.occupancy_type);
        this.bathroomEdited.stall_range_type = this.convertStallRange(this.bathroomEdited.stall_range_type);
        this.bathroomEdited.gender_type = this.convertGender(this.bathroomEdited.gender_type);

        //If we're editing an existing bathroom....
        if(this.bathroomEdited.id !== -1) {
          //Send the edited bathroom to the backend.
          axios.post('api/bathrooms/' + this.bathroomEdited.id, {
            id: this.bathroomEdited.id,
            bathroom_name: this.bathroomEdited.bathroom_name,
            description: this.bathroomEdited.description,
            time_availability: this.bathroomEdited,
            notes: this.bathroomEdited.notes,

            latitude: this.bathroomEdited.latitude,
            longitude: this.bathroomEdited.longitude,

            occupancy_type: this.bathroomEdited.occupancy_type,
            hand_drying_type: this.bathroomEdited.hand_drying_type,
            stall_range_type: this.bathroomEdited.stall_range_type,
            gender_type: this.bathroomEdited.gender_type
          })
          .then(response => {

            //Update the displayed bathroom for when we return to the 'view bathroom' view.
            this.bathroomViewed = this.bathroomEdited;
            this.editingBathroom = false;

            
            //Find the bathroom as it's stored locally and update its ratings. 
            for(let i = 0; i < this.bathroomsToDisplay.length; i++) {
              if(this.bathroomsToDisplay[i].id === this.bathroomEdited.id) {
                this.bathroomsToDisplay.$set(i, this.bathroomEdited);
                break;
              }
            }

          })
          .catch(e => {
            this.errors.push(e)
          });
        }
        //If we're creating a new bathroom...
        else {
          //Send the newly-created bathroom to the backend.
          axios.post('api/bathrooms', {
            bathroom_name: this.bathroomEdited.bathroom_name,
            description: this.bathroomEdited.description,
            time_availability: this.bathroomEdited,
            notes: this.bathroomEdited.notes,

            latitude: this.bathroomEdited.latitude,
            longitude: this.bathroomEdited.longitude,

            occupancy_type: this.bathroomEdited.occupancy_type,
            hand_drying_type: this.bathroomEdited.hand_drying_type,
            stall_range_type: this.bathroomEdited.stall_range_type,
            gender_type: this.bathroomEdited.gender_type,

            user_ratings: {
              cleanliness: null,
              privacy: null,
              atmosphere: null,
              location_accessibility: null,
            }
          })
          .then(response => {

            var newlyCreatedBathroom = JSON.parse(response);

            //Add the newly created bathroom to the local list.
            this.bathroomsToDisplay.push(newlyCreatedBathroom);

            //Update the displayed bathroom for when we return to the 'view bathroom' view.
            this.bathroomViewed = newlyCreatedBathroom;
            this.editingBathroom = false;

          })
          .catch(e => {
            this.errors.push(e)
          });
        }
        
      },

      rateBathroom : function(featureRated) {

        var feature, value;

        //Store the information of the feature that was rated.
        switch(featureRated) {
          case "privacy":
            feature = 1;
            this.bathroomViewed.user_ratings.privacy = this.privacyToDisplay;
            value = this.privacyToDisplay;
            break;
          case "accessibility":
            feature = 3;
            this.bathroomViewed.user_ratings.accessibility = this.accessibilityToDisplay;
            value = this.accessibilityToDisplay;
            break;
          case "atmosphere":
            feature = 2;
            this.bathroomViewed.user_ratings.atmosphere = this.atmosphereToDisplay;
            value = this.atmosphereToDisplay;
            break;
          case "cleanliness":
            feature = 0;
            this.bathroomViewed.user_ratings.cleanliness = this.cleanlinessToDisplay;
            value = this.cleanlinessToDisplay;
            break;
        }

        //Send rating to backend.
        axios.post('/api/users/' + this.userID + '/ratings', {
            rating_type: feature,
        
            rating: value,
            bathroom_id : this.bathroomViewed.id,

          })
          .then(response => {
              //Find the bathroom as it's stored locally and update its ratings. 
              for(let i = 0; i < this.bathroomsToDisplay.length; i++) {
                if(this.bathroomsToDisplay[i].id === this.bathroomViewed.id) {
                  this.bathroomsToDisplay.$set(i, this.bathroomViewed);
                  break;
                }
              }
          })
          .catch(e => {
            this.errors.push(e)
          });
        
      },

      convertHandDrying : function(hd_string) {
        switch(this.bathroomViewed.hand_drying_type) {
          case "Paper Towels":
            return 0;
          case "Electric Hand Dryer":
            return 1;
          case "Electric Hand Dryer AND Paper Towels":
            return 2;
          case "None Available":
            return 3;
          case "Other":
            return 4;
          default:
            return null;  
        }
      },

      convertOccupancy : function(o_string) {
        switch(o_string) {
          case "Single Occupancy":
            return 0;
          case "Multiple Occupancy":
            return 1;
          case "Other":
            return 2;
          default:
            return null;  
        }
      },

      convertStallRange : function(sr_string) {
        switch(sr_string) {
          case "One Stall":
              return 0;
          case "2-3 Stalls":
            return 1;
          case "4-7 Stalls":
            return 2;
          case "8+ Stalls":
            return 3;
          default:
            return null;  
        }
      },

      convertGender : function(g_string) {
        switch(g_string) {
          case "Gender Agnostic":
            return 0;
          case "Men":
            return 1;
          case "Women":
            return 2;
          case "Other":
            return 3;
          default:
            return null;   
        }
      },
    },
    created: function () {
      //Vue's list component likes to be edgy and uses the length of the array in data to determine the max #
      //items to display in a list, so this is a way of getting around that for the moment.
      this.bathroomsToDisplay = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
      {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}];
    },
    mounted: function () {

      var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';	
      var token = 'pk.eyJ1IjoiY3MxNTMwcHJvamVjdCIsImEiOiJjazJ0bGFzMGEweDhyM25sNzg5NzBpcnc4In0.qxgLkFpT71tMYMTN57ZffA';
      var mapboxUrl = 'https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/{z}/{x}/{y}@2x?access_token=' + token;

      var osm = new L.TileLayer(osmUrl, {
          attribution: 'Map data © <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
          detectRetina: true
      });

      var mapbox = new L.TileLayer(mapboxUrl, {
          attribution: 'Map data © <a href="http://osm.org/copyright">OpenStreetMap</a> contributors. Tiles from <a href="https://www.mapbox.com">Mapbox</a>.',
          tileSize: 512,
          zoomOffset: -1
      });

      this.map = new L.Map('map', {
          layers: [mapbox],
          center: [this.xCoordinate, this.yCoordinate],
          zoom: 16,
          zoomControl: true
      });

      // add location control so the user can lock on to their own location. 
      L.control.locate().addTo(this.map);

      this.layerGroup = L.layerGroup().addTo(this.map);

      this.loadBathrooms(0, 0 ,0 , 0, null, null, null, null);

    }
})