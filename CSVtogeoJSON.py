import csv, json
from geojson import Feature, FeatureCollection, Point
import pandas as pd
import os
    

def convert(uploaded_file):

    # Deal with file paths
    print uploaded_file
    script_dir = os.path.dirname(__file__)
    upload_rel_path = "uploaded_data"
    upload_abs_path = os.path.join(script_dir, upload_rel_path)
    out_rel_path = "files"
    out_abs_path = os.path.join(script_dir, out_rel_path)

    # For faster testing use a smaller subset
    #uploaded_file = upload_abs_path+'/GeoLite2-City-Blocks-IPv4-medium.csv'
    uploaded_file = upload_abs_path +'/'+uploaded_file
    print uploaded_file
    lat_long_only_file = out_abs_path+'/latlong.csv'

    # Only care about Lat/Long for this, if that changes need to remove from unwanted_keys
    present_headers = ['network','geoname_id','registered_geoname_id','represented_country_geoname_id','is_anonymous_proxy','is_satellite_provider','postal_code','latitude','longitude','accuracy_radius']
    unwanted_keys=['network','geoname_id','registered_geoname_id','represented_country_geoname_id','is_anonymous_proxy','is_satellite_provider','postal_code','accuracy_radius']

    # Use Panda to pre-process CSV file and remove all columns except latitude and longitude
    # Can use the existance of the latlong.csv file as a trigger to update the main data
    df1 = pd.read_csv(uploaded_file, names = present_headers, header = 0)
    df2 = df1.drop(unwanted_keys, axis =1)
    # Needs to be in long/lat order for geoJSON
    df2 = df2[['longitude', 'latitude']]
    # Drop any rows with NaN values
    df3 = df2.dropna(how='any')
    df3.to_csv(lat_long_only_file, index = False, header = False)


    # j is used to track the progress and mark lines that can't be converted
    j=0
    features = []

    reader = csv.reader(open(lat_long_only_file, 'rb'))

    def chunk_generator(reader, chunksize=5000):
        chunk = []
        for i, line in enumerate(reader):
            if (i % chunksize == 0 and i>0):
                yield chunk
                del chunk[:]
            chunk.append(line)
        yield chunk

    for chunk in chunk_generator(reader):
        for latitude, longitude in chunk:
            j = j+1
            # Try to handle errors in the file
            if(latitude or longitude is None ):
                # invalid coordinates
                pass                
            try:
                latitude, longitude = map(float, (latitude, longitude))
            except ValueError:
                print "Couldn't convert this line : " , j
                #next(reader)
                pass

            features.append(
                Feature(
                    geometry = Point((longitude, latitude)),
                )
            )


    collection = FeatureCollection(features)
    print "I'm working on something!"
    
    with open("files/GeoObs.geojson", "w") as f:
        f.write('%s' % collection)

    # cleanup   -> file in use?
    #os.remove(lat_long_only_file)
    return collection

if __name__ == "__main__":

    pass

# for cli testing
#convert('foo')

