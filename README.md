# Transloc

# How to use it as it stands

  "python api.py" 

  Give it a file to process:
  
  "curl -H "Content-Type: application/json" -X POST - http://127.0.0.1:5000/upload/GeoLite2-City-Blocks-IPv4.csv"
  
     Note: "curl http://127.0.0.1:5000/ipv4" will work as well if there is a file in the default location
  
     This will take ~2mins to process and will result in 2 new files being created: latlong.csv and GeoObs.geojson
  
  Rest endpoints should now be responsive  
  
  Dragging "local_index.html" into a browser window should show the heatmap of all processed coordinates

  


# REST endpoint examples:
curl http://127.0.0.1:5000/ipv4

curl http://127.0.0.1:5000/ipv4/box?coords=10.4,-12.12,19,4

curl -H "Content-Type: application/json" -X POST - http://127.0.0.1:5000/upload/<filename_to_process>

# Issues:

1) localhost:5000 can't load GeoObs.geojson which in turn leads to no heatmap
2) Heroku can't find template/index.html
3) Even if it does it'll run into the same problem as localhost
4) File sizes are large...very large 
5) AWS hosting for GeoObs.geojson doesn't seem to be working




# Output data format:

$ curl http://127.0.0.1:5000/ipv4/box?coords=10.4,-12.12,19,4
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  
  {"key": [{"latitude": -8.8368, "longitude": 13.2332}, {"latitude": 3.8667, "longitude": 11.5167}, {"latitude": -4.3, "longitude": 15.3}, {"latitude": -4.2592, "longitude": 15.2847}, {"latitude": -8.8368, "longitude": 13.2332}, {"latitude": 3.8667, "longitude": 11.5167}, {"latitude": -4.3, "longitude": 15.3},
  
  ...
  
{"latitude": -8.8368, "longitude": 13.2332}, {"latitude": -8.8368, "longitude": 13.2332}, {"latitude": -1.0, "longitude": 11.75}, {"latitude": -1.0, "longitude": 15.0}, {"latitude": -1.0, "longitude": 11.75}, {"latitude": -6.1349, "longitude": 12.3689}, {"latitude": -6.1349, "longitude": 12.3689}, {"latitude": -1.0, "longitude": 11.75}, {"latitude": -1.0, "longitude": 11.75}, {"latitude": -1.0, "longitude": 11.75}, {"latitude": -1.0, "longitude": 11.75}, {"latitude": -1.0, "longitude": 11.75}, {"latitude": -4.3, "longitude": 15.3}, {"latitude": -4.3, "longitude": 15.3}]}
