
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
    longitutde = position.coords.longitude;
  }
  else {
    latitude = 0;
    longitutde = 0;
  }
          var mapCanvas = document.getElementById('map-canvas');
          var mapOptions = {
            center: new google.maps.LatLng(latitude, longitutde),
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.ROADMAP
          }
          var map = new google.maps.Map(mapCanvas, mapOptions);

          var displayjson = JSON.stringify(position);
          document.getElementById("locationData").innerHTML = displayjson;
//ADD CURRENT USERS' DOT TO THE MAP
        map.data.addGeoJson(JSON.stringify(position));

}
google.maps.event.addDomListener(window, 'load', initialize);
