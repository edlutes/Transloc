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


// Attempt at pulling from AWS
// console.log("wut?")
// function pull_aws() {
//     const aws = require('aws-sdk');
//     const config = require('./config.json');
//     (async function() {
//         try{
//             aws.config.setPromisesDependency();
//             aws.config.update({
//                 accessKeyId:config.aws.accessKey,
//                 secretAccessKey: config.aws.secretKey
//             });

//             const s3 = new aws.S3();
//             const response = await s3.listObjectsV2({
//                 Bucket: 'lutestransloc'
//             }).promise();

//             console.log(response);

//         } catch (e){
//             console.log('Uh oh', e);
//         }
//         debugger;
//     })();
// };


// 2nd attempt at AWS

// var AWS = require('aws-sdk');
// AWS.config.update(
//   {
//     // These will be deleted shortly
//     accessKeyId: "AKIAJESJ6AUWDUBA67JQ",
//     secretAccessKey: "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",
//     region: 'us-east-1'
//   }
// );
// var s3 = new AWS.S3();
// s3.getObject(
//   { Bucket: "lutestransloc", Key: "GeoObs.geojson" },
//   function (error, data) {
//     if (error != null) {
//       alert("Failed to retrieve an object: " + error);
//     } else {
//       alert("Loaded " + data.ContentLength + " bytes");
//       // Not sure if this works and takes forever or is completely wrong
//       console.log(huh);
//       $.getJSON("../files/GeoObs.geojson",function(data){
//         var locations = data.features.map(function(rat){
//             var location = rat.geometry.coordinates;
//             location.push(0.5);
//             return location;
//         });
    
//         var heat = L.heatLayer(locations, {radius: 35}).addTo(map);
//         heat.addTo(map)
    
//     });
//     }
//   }
// );

$.getJSON("{{ url_for(GeoObs.geojson)}}",function(data){
    var locations = data.features.map(function(rat){
        var location = rat.geometry.coordinates;
        location.push(0.5);
        return location;
    });

    var heat = L.heatLayer(locations, {radius: 35}).addTo(map);
    heat.addTo(map)

});

