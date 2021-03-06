// Store our API endpoint inside queryUrl
//  collect data each day (24 hours)
var queryUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=" +
  "2014-01-07&maxlongitude=-69.52148437&minlongitude=-123.83789062&maxlatitude=48.74894534&minlatitude=25.16517337";

// Perform a GET request to the query URL
d3.json(queryUrl, function(data) {
  // Once we get a response, send the data.features object to the createFeatures function
  createFeatures(data.features);
});

function createFeatures(earthquakeData) {
  // Sending our earthquakes layer to the createMap function
  var myMap = createMap();

  // Define a function we want to run once for each feature in the features array
  // Give each feature a popup describing the place and time of the earthquake
  function onEachFeature(feature, layer) {
    console.log(feature.geometry.coordinates[0], feature.geometry.coordinates[1]);

    var color, fillColor;
    if (feature.properties.mag > 3) {

      color = 'red';
      fillColor = '#ff0000';
    } else if (feature.properties.mag > 2) {
      color = 'yellow';
      fillColor = '#ffff00';
    } else {
      color = 'green';
      fillColor = '#00ff00';
    }

    L.circle([feature.geometry.coordinates[1], feature.geometry.coordinates[0]], {
      color: color,
      fillColor: fillColor,
      fillOpacity: 0.5,
      radius: 10000 * feature.properties.mag
    }).bindPopup("<h3>" + feature.properties.title + "</h3><hr><p>" + new Date(feature.properties.time) + "</p>").addTo(myMap);
  
  //  layer.bindPopup("<h3>" + feature.properties.place +
  //      "</h3><hr><p>" + new Date(feature.properties.time) + "</p>");
  }

  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array
  // feature is in joson file 
  var earthquakes = L.geoJSON(earthquakeData, {
    onEachFeature: onEachFeature
  });
}

function createMap() {

  // Define streetmap and darkmap layers
  var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
  });

  var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.dark",
    accessToken: API_KEY
  });

  // Define a baseMaps object to hold our base layers
  var baseMaps = {
    "Street Map": streetmap,
    "Dark Map": darkmap
  };

  // Create overlay object to hold our overlay layer
  var overlayMaps = {
  //  Earthquakes: earthquakes
  };

  // Create our map, giving it the streetmap and earthquakes layers to display on load
  var myMap = L.map("map", {
    center: [
      37.09, -95.71
    ],
    zoom: 5,
    layers: [streetmap]
  //  layers: [streetmap, earthquakes]
  });

  // Create a layer control
  // Pass in our baseMaps and overlayMaps
  // Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(myMap);

  return myMap;
}

/// how to make the circles appear on an overlay layer???

