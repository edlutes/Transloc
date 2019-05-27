var map = L.map('map',{
    center: [35.87,-78.84],
    zoom: 11,
    maxBounds:([[-90,-180],[90,180]]),
    worldCopyJump: true,
    style: 'mapbox://styles/mapbox/streets-v11',
});

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets',
    minZoom: 3,
    maxZoom: 12,
    radius: 1,
    accessToken: 'pk.eyJ1IjoiZWx1dGVzIiwiYSI6ImNqdnlnMWYwazAycG40YmxjYzB0bzlhZzEifQ.DXfl1jtvxEfFrmqPdn7D6Q'
}).addTo(map);

// This works locally but not through a webserver
// Need to host file somewhere....AWS S3?
// Read in the geoJSON
$.getJSON("../files/GeoObs.geojson",function(data){
    var locations = data.features.map(function(rat){
        var location = rat.geometry.coordinates;
        location.push(0.5);
        return location;
    });

    var heat = L.heatLayer(locations, {radius: 35}).addTo(map);
    heat.addTo(map)

});

// Change scale while zooming?
// map.on('zoomstart', function(notused) {
//     console.log ("zooming");
    
// })
