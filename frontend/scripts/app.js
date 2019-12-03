
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
      admin: false,

      loginDialog: false,
      bathroomDialog: false,
      reportDialog: false,
      filterPopup: false,
      reportPopup: false,
      helpModeDialog : false,

      pinOnMap: false, 
      pin: null, //This is the pin that the user uses to select the area of the new bathroom. 

      map: null,
      layerGroup : null,
      xCoordinate: 40.444, //Initially set the map's center on the Cathedral of Learning.
      yCoordinate: -79.953,

      bathroomViewed: null,
      bathroomsToDisplay: [],

      reportViewed: null,
      reportsToDisplay: [],
      reportText: "",

      filterOccupancy: null,
      filterGender: null, 
      filterStallRange: null,
      filterHandDrying: null,


      editingBathroom: false,
      bathroomEdited: null,

      loginCaption: "",
      cleanlinessToDisplay: null,
      privacyToDisplay: null,
      accessibilityToDisplay: null,
      atmosphereToDisplay: null,

      //String versions of the values to display. 
      occupancyToDisplay: null,
      genderToDisplay: null,
      stallNumberToDisplay: null,
      handDryingToDisplay: null,


    }),
  
    methods: {

      //Determine whether to show a user's personal ratings or the average rating for a bathroom's features.
      setRatingsToDisplay : function() {


        //If this user has rated cleanliness, display this user's rating. 
        if(this.bathroomViewed.user_ratings !== undefined && this.bathroomViewed.user_ratings.cleanliness !== null) 
          this.cleanlinessToDisplay = this.bathroomViewed.user_ratings.cleanliness;
        else if (this.bathroomViewed.avg_ratings.cleanliness !== null)
          this.cleanlinessToDisplay = this.bathroomViewed.avg_ratings.cleanliness;
        else
          this.cleanlinessToDisplay = null;

        //If this user has rated privacy, display this user's rating. 
        if(this.bathroomViewed.user_ratings !== undefined && this.bathroomViewed.user_ratings.privacy !== null)
          this.privacyToDisplay = this.bathroomViewed.user_ratings.privacy;
        else if(this.bathroomViewed.avg_ratings.privacy !== null)
          this.privacyToDisplay = this.bathroomViewed.avg_ratings.privacy;
        else
          this.privacyToDisplay = null;


          //If this user has rated accessibility, display this user's rating. 
        if(this.bathroomViewed.user_ratings !== undefined && this.bathroomViewed.user_ratings.location_accessibility !== null)
          this.accessibilityToDisplay = this.bathroomViewed.user_ratings.location_accessibility;
        else if(this.bathroomViewed.avg_ratings.location_accessibility !== null) 
          this.accessibilityToDisplay = this.bathroomViewed.avg_ratings.location_accessibility;
        else
          this.accessibilityToDisplay = null;

        //If this user has rated atmosphere, display this user's rating. 
        if(this.bathroomViewed.user_ratings !== undefined && this.bathroomViewed.user_ratings.atmosphere !== null)
          this.atmosphereToDisplay = this.bathroomViewed.user_ratings.atmosphere;
        else if(this.bathroomViewed.avg_ratings.atmosphere !== null)
          this.atmosphereToDisplay = this.bathroomViewed.avg_ratings.atmosphere;
        else
          this.atmosphereToDisplay = null;
      },

      convertCategoricalValues : function() {
        this.convertHandDryingToString();
        this.convertGenderToString();
        this.convertOccupancyToString();
        this.convertStallNumberToString();
      },

      loadBathrooms : function() {
          var min_lat, max_lat, min_lon, max_lon, o_type, hd_type, sr_type, g_type;

 
          hd_type = this.convertHandDrying(this.filterHandDrying);
          o_type = this.convertOccupancy(this.filterOccupancy);
          sr_type = this.convertStallRange(this.filterStallRange);
          g_type = this.convertGender(this.filterGender);


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
          
          var self = this;

          //Make the POST call to the backend.
           axios.post('/api/getbathrooms', {
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
                var bathArray = response.data;

                //Sort this array by average rating, descending.
                bathArray.sort((a, b) => (a.avg_overall_rating > b.avg_overall_rating) ? -1 : 1);

                for(obj of bathArray) {
                  this.bathroomsToDisplay.push(obj);
                }

                //Clear all the old markers.
                this.layerGroup.clearLayers();

                //Add a new layer group for the new markers.
                this.layerGroup = L.layerGroup().addTo(this.map);

                //Then add markers to the map for each bathroom. 
                for(bathroom of this.bathroomsToDisplay) {
                  L.marker([bathroom.latitude, bathroom.longitude], {title: bathroom.bathroom_name}).addTo(self.layerGroup).on('click', function(e) {

                    displayBathroomFromMap(this.getLatLng().lng, this.getLatLng().lat);
                  });
                }


            })
           .catch(e => {
              console.log("Failed to load bathrooms from server.");
           })
          
          
      },
      displayBathroomFromMap : function(longitude, latitude) {


        let bathroom = null;
        let i = 0;

        //Find bathroom to display from its coordinates.
        while(this.bathroomsToDisplay[i] !== undefined) {
          if(this.bathroomsToDisplay[i].latitude === latitude && this.bathroomsToDisplay[i].longitude === longitude) {
            bathroom = this.bathroomsToDisplay[i];
            break;
          }
          i++;
        }

        //Display that bathroom.
        if(bathroom !== null)
          this.displayBathroomFromList(bathroom);
      },

      displayBathroomFromList : function(bathroom) {

        this.bathroomViewed = bathroom;

        //If this is a logged in user, determine which cleanliness, privacy, etc ratings to display-
        //their own or the average for all users.
        
          this.setRatingsToDisplay();


        //Make sure that the pin used for adding a new bathroom is removed from the map. 
        if(this.pin !== null) {
          this.pin.remove();
          this.pin = null;
          this.pinOnMap = false;
        }

        //Convert categorical values from numbers to strings to display.
        this.convertCategoricalValues();


        this.bathroomDialog = true;
      },

      login : function() {
        if(this.logInUsername === "" || this.logInPass === "")
          this.loginCaption = "Make sure you enter both a username and password.";
        else {
          var self = this;

          //Make request to backend via POST. 
          axios.post('/api/authenticate', {

            username: this.logInUsername,
            password: this.logInPass

          })
          .then(function (response) {
            var json = response.data;

            self.loggedIn = true;
            self.userID = json.id;
            self.admin = json.isAdmin;
            self.loginCaption = "";
            self.logInUsername = "";
            self.registerUsername = "";
            self.logInPass = "";
            self.registerPass = "";
            self.registerPassAgain = "";

            self.setCookie();

            if(self.admin) {
              self.loadReports();
            }
            self.exitLogin();

            return;
          })
          .catch(function (error) {
            console.log(error.response);

            if(error.response) {
              console.log(error.response.data);
              console.log(error.response.status);
            }
            else
              console.log(error);

            self.loginCaption = "Login Failed- Check your password and try again";
          
          });
        }
      
      },

      dropPin : function() {
        //Let user add pin to map.

        this.pin = L.marker(this.map.getCenter(),{
          draggable: true
        }).addTo(this.map);
        
        this.pinOnMap = true;

        this.clearDisplayValues();
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

        this.bathroomViewed = null;
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
          var self = this;

          axios.post('/api/users', {
            username: this.registerUsername,
            password: this.registerPass
          })
          .then(function (response) {
            var json = response.data

            console.log("Register");

            //Clear out all the login/registration info.
            self.loginCaption = "";
            self.logInUsername = "";
            self.registerUsername = "";
            self.logInPass = "";
            self.registerPass = "";
            self.registerPassAgain = "";

            self.userID = json.id;

            
            self.loggedIn = true;

            self.setCookie();
            self.exitLogin();
            return;
          })
          .catch(function (error) {
            if(error.response) {
              console.log(error.response);

              if(error.response.data === "user already exists") {
                self.loginCaption = "A user with this name already exists.";
              }
            }
            else {
              console.log(error);

              //Show error message on screen.
              self.loginCaption = "User registration failed";
            }
          });
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

      exitReportView : function() {
        this.reportDialog = false;
      },

      exitLogin: function() {
        this.loginDialog = false;
      },

      exitHelpMode: function() {
        this.helpModeDialog = false;
      },

      //Set a cookie with the user ID.
      setCookie: function() {
        document.cookie = "id=" + this.userID;

        document.cookie = "admin=" + this.admin;
      },

      //Save either an edited bathroom or a newly created bathroom.
      saveBathroom : function() {

        //Convert features from strings to numbers amenable to the DB.
         this.bathroomEdited.hand_drying_type = this.convertHandDrying(this.handDryingToDisplay);
         this.bathroomEdited.occupancy_type = this.convertOccupancy(this.occupancyToDisplay);
         this.bathroomEdited.stall_range_type = this.convertStallRange(this.stallNumberToDisplay);
         this.bathroomEdited.gender_type = this.convertGender(this.genderToDisplay);

       

        var self = this;

        //If we're editing an existing bathroom....
        if(this.bathroomEdited.id !== -1) {
          //Send the edited bathroom to the backend.
          axios.post('api/bathrooms/' + this.bathroomEdited.id, {
            id: this.bathroomEdited.id,
            bathroom_name: this.bathroomEdited.bathroom_name,
            description: this.bathroomEdited.description,
            time_availability: this.bathroomEdited.time_availability,
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
            self.bathroomViewed = self.bathroomEdited;
            self.editingBathroom = false;

            //Find the bathroom as it's stored locally and update its ratings. 
            for(let i = 0; i < self.bathroomsToDisplay.length; i++) {
              if(self.bathroomsToDisplay[i].id === self.bathroomEdited.id) {
                self.$set(self.bathroomsToDisplay, i, self.bathroomEdited);
                break;
              }
            }

          })
          .catch(function (error)  {
            console.log(error);
          });
        }
        //If we're creating a new bathroom...
        else {
          //Send the newly-created bathroom to the backend.
          axios.post('api/bathrooms', {
            bathroom_name: this.bathroomEdited.bathroom_name,
            description: this.bathroomEdited.description,
            time_availability: this.bathroomEdited.time_availability,
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

            var newlyCreatedBathroom = response.data;


            //Add the newly created bathroom to the local list.
            this.bathroomsToDisplay.push(newlyCreatedBathroom);

            //Add the newly created bathroom to the map. 
            L.marker([newlyCreatedBathroom.latitude, newlyCreatedBathroom.longitude], {title: newlyCreatedBathroom.bathroom_name}).addTo(self.layerGroup).on('click', function(e) {
              displayBathroomFromMap(this.getLatLng().lng, this.getLatLng().lat);
            });


            //Update the displayed bathroom for when we return to the 'view bathroom' view.
            self.bathroomViewed = newlyCreatedBathroom;


            //Show the correct ratings based on the bathroom to display. 
            self.setRatingsToDisplay();

            //Update the categorical valaues based on the bathroom to display. 
            self.convertCategoricalValues();

            self.editingBathroom = false;

          })
          .catch(function (error)  {
            console.log(error);
          });
        }
        
      },

      clearDisplayValues: function() {
        //Clear the selection values.
        this.genderToDisplay = '';
        this.occupancyToDisplay = '';
        this.stallNumberToDisplay = '';
        this.handDryingToDisplay = '';
      },

      logout: function() {
        //Clear the id cookie by setting all cookies to expire.
        document.cookie.split(";").forEach(function(c) { 
            document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
        });

        //Navigate to /api/logout to clear the session cookie.
        window.location.replace("/api/logout");
      },

      deleteFromReport: function () {
        //Delete bathroom from DB.
        this.deleteBathroom();

        //Resolve report.
        this.resolveReport();
      },

      editFromReport: function() {
        //Save bathroom changes.
        this.saveBathroom();

        //Resolve report.
        this.resolveReport();
      },

      deleteBathroom: function() {

        let self = this;

        //Delete the bathroom viewed from the database. 
        axios.post('/api/delete/bathroom', {
          id: this.bathroomViewed.id
        })
        .then(response => {

          //Delete the bathroom from the local list, if it's there.
          for(let i = 0; i < self.bathroomsToDisplay.length; i++) {
            if(self.bathroomsToDisplay[i].id === self.bathroomViewed.id) {
              //Splice out bathroom.
              self.bathroomsToDisplay.splice(i, 1);
              break;
            }
          }

          //Replace bathroomViewed, now that it's deleted.
          self.bathroomViewed = null;

          //Close view dialog.
          self.bathroomDialog = false;
        })
        .catch(e => {
          console.log("Failed to delete bathroom.");
        });

      },

      reportBathroom: function() {
        //Generate a report for the bathroom viewed. 

        let self = this;
        axios.post('/api/reports', {
          bathroom_id: this.bathroomViewed.id,
          description: this.reportText
        })
        .then(response => {
          //Close report popup.
          self.reportPopup = false;
        })
        .catch(e => {
          console.log("Failed to report bathroom.");
        });

      },

      loadReports: function() {
        //Make axios HTTP call to get reports.

        let self = this;

        //Get the bathroom associated with the report.
        axios.get('/api/reports')
        .then(response => {
            //Store list of reports.
            self.reportsToDisplay = response.data;
          })
        .catch(e => {
            console.log("Failed to load reports from server.");
        });

      },

      displayReport: function(report) {
        
        this.reportViewed = report;
        this.reportText = report.description;
        let self = this;

        //Get the bathroom associated with the report.
        axios.get('/api/bathrooms/' + report.bathroom_id)
        .then(response => {
          self.bathroomViewed = response.data;
          self.bathroomEdited = response.data;

          //Open up the Report Dialog
          self.reportDialog = true;

        })
        .catch(function (error)  {
          console.log(error);
        });
      },

      resolveReport: function() {

        let self = this;
        
        //Resolve report HTTP call.
        axios.post('/api/delete/report', {
          id: this.reportViewed.id
        })
        .then(response => {
          //Delete report from local list.
          for(let i = 0; i < self.reportsToDisplay.length; i++) {
            if(self.reportsToDisplay[i].id === self.reportViewed.id) {
              self.reportsToDisplay.splice(i, 1);
              break;
            }
          }

          //Close report view.
          self.reportDialog = false;
        })
        .catch(e => {
            console.log("Failed to resolve report.");
        });
        
      },

      rateBathroom : function(featureRated) {

        var feature, value;

        if(this.bathroomViewed.user_ratings === undefined) {
          console.log("No user ratings object was found.");
          this.bathroomViewed.user_ratings = {};
        }

        //Store the information of the feature that was rated.
        switch(featureRated) {
          case 'privacy':
            feature = 1;
            this.bathroomViewed.user_ratings.privacy = this.privacyToDisplay;
            value = this.privacyToDisplay;
            break;
          case 'accessibility':
            feature = 3;
            this.bathroomViewed.user_ratings.location_accessibility = this.accessibilityToDisplay;
            value = this.accessibilityToDisplay;
            break;
          case 'atmosphere':
            feature = 2;
            this.bathroomViewed.user_ratings.atmosphere = this.atmosphereToDisplay;
            value = this.atmosphereToDisplay;
            break;
          case 'cleanliness':
            feature = 0;
            this.bathroomViewed.user_ratings.cleanliness = this.cleanlinessToDisplay;
            value = this.cleanlinessToDisplay;
            break;
        }

        var self = this;
        //Send rating to backend.
        axios.post('/api/users/' + this.userID + '/ratings/', {
            rating_type: feature,
        
            rating: value,
            bathroom_id : this.bathroomViewed.id,

          })
          .then(response => {
            //Find the bathroom as it's stored locally and update its ratings. 
            for(let i = 0; i < self.bathroomsToDisplay.length; i++) {
              if(self.bathroomsToDisplay[i].id === self.bathroomViewed.id) {
                self.$set(self.bathroomsToDisplay, i, self.bathroomViewed);
                break;
              }
            }


          })
          .catch(function (error)  {
            console.log(error);
          });
        
      },

      convertHandDrying : function(hd_string) {
        switch(hd_string) {
          case "Paper Towels":
            return 0;
          case "Electric Hand Dryer":
            return 1;
          case "Electric Hand Dryer AND Paper Towels":
            return 2;
          case "None available":
            return 3;
          case "Other":
            return 4;
          default:
            return null;  
        }
      },

      convertHandDryingToString : function() {
        
        switch(this.bathroomViewed.hand_drying_type) {
          case 0:
            this.handDryingToDisplay = 'Paper Towels';
            break;
          case 1:
            this.handDryingToDisplay = 'Electric Hand Dryer';
            break;
          case 2:
            this.handDryingToDisplay = 'Electric Hand Dryer AND Paper Towels';
            break;
          case 3:
            this.handDryingToDisplay = 'None available';
            break;
          case 4:
            this.handDryingToDisplay = 'Other';
            break;
          default:
            this.handDryingToDisplay = '';  

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

      convertOccupancyToString : function() {

        switch(this.bathroomViewed.occupancy_type) {
          case 0:
            this.occupancyToDisplay = 'Single Occupancy';
            break;
          case 1:
            this.occupancyToDisplay = 'Multiple Occupancy';
            break;
          case 2:
            this.occupancyToDisplay = 'Other';
            break;
          default:
            this.occupancyToDisplay = '';  
        }
      },
      convertStallRange : function(sr_string) {
        switch(sr_string) {
          case "One Stall / Single Occupancy":
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
      convertStallNumberToString : function() {

        switch(this.bathroomViewed.stall_range_type) {
          case 0:
            this.stallNumberToDisplay = 'One Stall';
            break;
          case 1:
            this.stallNumberToDisplay = '2-3 Stalls';
            break;
          case 2:
            this.stallNumberToDisplay = '4-7 Stalls';
            break;
          case 3:
            this.stallNumberToDisplay = '8+ Stalls';
            break;
          default:
            this.stallNumberToDisplay = '';  
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

      convertGenderToString : function() {

        switch(this.bathroomViewed.gender_type) {
          case 0:
            this.genderToDisplay = 'Gender Agnostic';
            break;
          case 1:
            this.genderToDisplay = 'Men';
            break;
          case 2:
            this.genderToDisplay = 'Women';
            break;
          case 3:
            this.genderToDisplay = 'Other';
            break;
          default:
            this.genderToDisplay = ''; 
        }
      },
    },
    created: function () {
      //Vue's list component likes to be edgy and uses the length of the array in data to determine the max #
      //items to display in a list, so this is a way of getting around that for the moment.
      this.bathroomsToDisplay = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
      {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}];

      this.reportsToDisplay = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
        {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}];

      window.loadBathrooms = this.loadBathrooms;
      window.displayBathroomFromMap = this.displayBathroomFromMap;
      window.loadReports = this.loadReports;
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


      var x = document.cookie;
      var cookieTokens = x.split('=');

      //Check if the user is already logged in.
      for(let i = 0; i < cookieTokens.length; i++) {
        if(cookieTokens[i] === 'id') {
          this.userID = cookieTokens[i + 1];
          this.loggedIn = true;
        }
        // else if (cookieTokens[i] === 'admin'){
        //   this.admin = cookieTokens[i + 1];
        //   this.loadReports();
        // }
      }

      this.loadReports();

      this.layerGroup = L.layerGroup().addTo(this.map);

      this.loadBathrooms(0, 0 ,0 , 0, null, null, null, null);

      //Whenever the map moves, reload the bathrooms. 
      this.map.on('moveend', function(e) {
        loadBathrooms();
      });

      //Whenever the map's zoom changes, reload the bathrooms. 
      this.map.on('resize', function(e) {
        loadBathrooms();
      });
    }
})