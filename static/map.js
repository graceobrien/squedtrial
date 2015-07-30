var latitude=0;
var longitude=0;
var map = null;
var on = false;

function getUserLocation() {
//check if the geolocation object is supported, if so get position
if (navigator.geolocation){
	var currentlocation = navigator.geolocation.getCurrentPosition(displayLocation, displayError);

}
else {
	document.getElementById("locationData").innerHTML = "Sorry - your browser doesn't support geolocation!";
}
}

function displayError(error) {

//get a reference to the HTML element for writing result
var locationElement = document.getElementById("locationData");

//find out which error we have, output message accordingly
switch(error.code) {
case error.PERMISSION_DENIED:
	locationElement.innerHTML = "Permission was denied";
	break;
case error.POSITION_UNAVAILABLE:
	locationElement.innerHTML = "Location data not available";
	break;
case error.TIMEOUT:
	locationElement.innerHTML = "Location request timeout";
	break;
case error.UNKNOWN_ERROR:
	locationElement.innerHTML = "An unspecified error occurred";
	break;
default:
	locationElement.innerHTML = "Who knows what happened...";
	break;
}}

//DISPLAY THE LOCATIOn
function displayLocation(position) {

		//build text string including co-ordinate data passed in parameter
		var displayText = "User latitude is " + position.coords.latitude + " and longitude is " + position.coords.longitude;

		//display the string for demonstration
		document.getElementById("locationData").innerHTML = displayText;
		initialize (position);
}

function initialize(position) {
  if (position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
  }
  var mapCanvas = document.getElementById('map-canvas');
  var mapOptions = {
    center: new google.maps.LatLng(latitude, longitude),
    zoom: 14,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  map = new google.maps.Map(mapCanvas, mapOptions);
	google.maps.event.addListenerOnce(map, 'idle', adddots)

}
google.maps.event.addDomListener(window, 'load', function (event) { navigator.geolocation.getCurrentPosition(initialize, displayError) } );



function adddots () {
	for (i= 0; i<locations.length ; i++) {
			loc = locations[i];
						map.data.addGeoJson({
						"type": "Feature",
		 				"geometry": {
		 				"type": "Point",
		 				"coordinates": [loc.lon, loc.lat]},
		 				"properties": {
		 				"name": "Something"}
		 				 });
		 				map.data.addListener('click', function(event) {
		 						window.location = "/profile?user=" + user_entity_key_urlsafe()
				});
	   }
}

var i;

function userdot() {

	if (on == false) {
				i = map.data.addGeoJson({
			  "type": "Feature",
			  "geometry": {
			  "type": "Point",
			  "coordinates": [longitude, latitude]},
			  "properties": {
			  "name": "Something"}
			   });
				//set location in database
				map.data.addListener('click', function(event) {
				    window.location = "/profile?key=" + user_entity.key.urlsafe()
				});

			$.post('/saveloc', {latitude:latitude, longitude:longitude}, function (data){console.log(data)})
				on = true;

		}
		else {
		//set location to none
		//take them out of database
		console.log(map.data)
		map.data.remove(i[0]);
		$.post('/saveloc', {}, function (data){console.log(data)})
			 on = false;
			 //set location to none
	}
}
