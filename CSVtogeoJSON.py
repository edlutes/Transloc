import csv, json
from geojson import Feature, FeatureCollection, Point
import pandas as pd

def convert(uploaded_file):
    # For faster testing use a smaller subset
    uploaded_file = '../GeoLite2-City-CSV_20190521/GeoLite2-City-Blocks-IPv4-medium.csv'
    lat_long_only_file = './latlong.csv'

    # Only care about Lat/Long for this, if that changes need to remove from unwanted_keys
    present_headers = ['network','geoname_id','registered_geoname_id','represented_country_geoname_id','is_anonymous_proxy','is_satellite_provider','postal_code','latitude','longitude','accuracy_radius']
    unwanted_keys=['network','geoname_id','registered_geoname_id','represented_country_geoname_id','is_anonymous_proxy','is_satellite_provider','postal_code','accuracy_radius']

    # Use Panda to pre-process CSV file and remove all columns except latitude and longitude
    # Can use the existance of the latlong.csv file as a trigger to update the main data
    df1 = pd.read_csv(uploaded_file, names = present_headers, header = 0)
    df2 = df1.drop(unwanted_keys, axis =1)
    # Needs to be in long/lat order for geoJSON
    df2 = df2[['longitude', 'latitude']]
    df2.to_csv(lat_long_only_file, index = False)

    i=0
    features = []
    with open(lat_long_only_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        #skip the header
        next(reader)
        for latitude, longitude in reader:
            i = i+1
            #print float(longitude) + float(latitude) 
            # Try to handle errors in the file
            if(latitude or longitude is None ):
                #latitude = longitude = 0
               # pass
                
                # invalid coordinates
                #StopIteration errors when over 59915 lines
                if(next(reader)is not None):
                    next(reader)
                
            try:
                latitude, longitude = map(float, (latitude, longitude))
            except ValueError:
                print "Couldn't convert this line : " , i
               # print "lat / long is : ", latitude, longitude
                #next(reader)
                pass

            features.append(
                Feature(
                    geometry = Point((longitude, latitude)),
                )
            )

    collection = FeatureCollection(features)
    print "I'm working on something!"
    #return collection
    with open("GeoObs.geojson", "w") as f:
        f.write('%s' % collection)

# for cli testing
convert('foo')