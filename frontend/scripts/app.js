
new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: () => ({
      loginDialog: false,
      bathroomDialog: false,
      filterPopup: false,
      editingBathroom: false,
      map: null,
      xCoordinate: 40.444, //Initially set the map's center on the Cathedral of Learning.
      yCoordinate: -79.953,
      userID: -1,
      loggedIn: false,
      bathroomViewed: null,
      bathroomsToDisplay: null,

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
          this.filterPopup = false,
          

          //Make the POST call to the backend.
           axios.post('/api/bathrooms/' + this.userID, {
                min_latitude: min_lat,
                max_latitude: max_lat,
                min_longitude: min_lon,
                max_longitude: max_lon,
            
                occupancy_type: o_type,
                hand_drying_type: hd_type,
                stall_range_type: sr_type,
                gender_type: g_type,
           })
           .then(response => {
                //Convert JSON to object array.
                var bathArray = JSON.parse(response);
                //Sort this array by average rating, descending.
                bathArray.sort((a, b) => (a.avg_overall_rating > b.avg_overall_rating) ? -1 : 1);

                //Set this as our new bathrooms to display.
                this.bathroomsToDisplay = bathArray;

                //Then add markers on the map for each bathroom. 
                for(bathroom in this.bathroomsToDisplay) {
                    L.marker([bathroom.longitude, bathroom.latitude]).addTo(this.map);
                }
            })
           .catch(e => {
              console.log("Failed to load bathrooms from server.");
           })
           
              //Test bathroom for test purposes.
             //this.bathroomsToDisplay = [{bathroom_name: "Test bathroom", longitude: 40.441, latitude: -79.952,
             //avg_overall_rating: 4.5, avg_ratings: {cleanliness: 3, privacy: 4.5, accessibility: 4, atmosphere: 2.5} }];

           //Then add markers on the map for each bathroom found. 
           for(bathroom of this.bathroomsToDisplay) {
              L.marker([bathroom.longitude, bathroom.latitude]).addTo(this.map).on('click', function(e) {
                this.bathroomViewed = bathroom;
              });
           }

          
      },
      displayBathroomFromList : function(bathroom) {
        if(this.loggedIn)
          this.setRatingsToDisplay();

        this.bathroomViewed = bathroom;
        this.bathroomDialog = true;
      },
      attemptLogin : function(user, pass) {

        //Make request to backend via POST. 
        axios.post('/api/authenticate', {
          params: {
            username: user,
            password: pass
          }
        })
        .then(function (response) {
          var json = JSON.parse(response);

          this.loggedIn = true;
          this.loginDialog = false;
          this.userID =json.id;
        })
        .catch(function (error) {
          console.log(error);

          //Show error message on screen.

        });


      },

      addBathroom : function(bathroomToSave) {
        //Let user add pin to map.
      },

      registerUser : function(user, pass) {
        axios.post('/api/users', {
          params: {
            username: user,
            password: pass
          }
        })
        .then(function (response) {
          var json = JSON.parse(response);

          this.loggedIn = true;
          this.loginDialog = false;
          this.userID =json.id;
        })
        .catch(function (error) {
          console.log(error);

          //Show error message on screen.

        });
      },

      editBathroom : function() {
        this.bathroomEdited = this.bathroomViewed;
        this.editingBathroom = true;
      },

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

        //Send the edited bathroom to the backend.
        axios.post('api/bathrooms/' + this.userID, {
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

            //Update the displayed bathroom. 
            this.bathroomViewed = this.bathroomEdited;

            this.editingBathroom = false;
        })
        .catch(e => {
              this.errors.push(e)
        });
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
            bathroom_id : this.bathroomToDisplay.id,

          })
          .then(response => {
              //Do nothing.
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
          zoom: 17,
          zoomControl: true
      });

      // add location control so the user can lock on to their own location. 
      L.control.locate().addTo(this.map);

      this.loadBathrooms(0, 0 ,0 , 0, null, null, null, null);

    }
})