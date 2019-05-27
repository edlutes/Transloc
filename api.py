from flask import Flask, request
from flask_pymongo import PyMongo
from CSVtogeoJSON import convert, panda_processing
from geojson import Feature, FeatureCollection, Point
import pandas as pd
import os
import json

from flask_restful import reqparse

# Install Redis to help with caching?
#from flask_cache import Cache

app = Flask(__name__)


#app.config['MONGO_URI'] = "mongodb://testuser:Transloc@transloccluster-shard-00-00-fwvjk.mongodb.net:27017,transloccluster-shard-00-01-fwvjk.mongodb.net:27017,transloccluster-shard-00-02-fwvjk.mongodb.net:27017/test?ssl=true&replicaSet=TranslocCluster-shard-0&authSource=admin&retryWrites=true"
#mongo = PyMongo(app)



# if ./file/latlong.csv exists we can reuse that file jsonified
# otherwise we'll need to process the raw starting data
script_dir = os.path.dirname(__file__)
starting_data_rel_path = "uploaded_data"
starting_data_abs_path = os.path.join(script_dir, starting_data_rel_path)
starting_data_file = starting_data_abs_path+'/'+"GeoLite2-City-Blocks-IPv4.csv"
processed_data_rel_path = "files"
processed_data_abs_path = os.path.join(script_dir, processed_data_rel_path)
processed_data_file = processed_data_abs_path+'/'+"latlong.csv"

# Return all coordinates
#TODO look into returning in chunks
@app.route('/ipv4')
def ipv4():
    
    # Check if file exists first to avoid processing it again
    if (os.path.isfile(processed_data_file)):
        print ('Re-using existing file')
        #file exists, reuse it
        df = pd.read_csv(processed_data_file, names=['longitude','latitude'])
    else:    
        print ('I\'m working on something new')
        df = panda_processing(starting_data_file)
        #TODO implement caching
        # Caching at this point would be ideal
        # for now write to file to ensure we only have to do this once
        df.to_csv(processed_data_file, index = False, header = False)

    df_to_json = {
        'key':df.to_dict(orient='records')
    }
    matching_results=json.dumps(df_to_json)
    
    return matching_results, 200
    
#@app.route('/ipv4/boundary', function (req, res))
# Takes in top left and bottom right coordinates to create a box
# returns all coordinates within the created box
# Does not auto populate data
@app.route('/ipv4/box')
def box_coordinates():
    parser = reqparse.RequestParser()
    parser.add_argument('coords')

    # we now have a dict with in the form of {cords:a,b,c,d}
    args = parser.parse_args()
    # We only care about the values
    values = args.values()

    for i in values:
        i = str(i)

    coords =i.split(',')

    # Basic error handling

    # Check that we have 4 coordinates
    if (len(coords) != 4):
        return 'Four coordinates are required', 400

    # Check that we didn't get passed an empty coordinate
    for test in coords:
        if not test:
            return 'Empty coordinate found', 400

    # Make the coordinates human readable
    tl_long = float(coords[0])
    tl_lat = float(coords[1])
    br_long = float(coords[2])
    br_lat = float(coords[3])

    if ((tl_long >= br_long) or (tl_lat >= br_lat)):
        return 'Invalid boundary', 400
   
    # Coordinates are now in the order of top left longitude, top left latitude
    # bottom right longitude, bottom right latitude 

    if (os.path.isfile(processed_data_file)):
        df = pd.read_csv(processed_data_file, names=['longitude','latitude'])

        df2 = df.loc[ (df['longitude'] >= tl_long)&
                      (df['longitude'] <= br_long)&
                      (df['latitude'] >= tl_lat)&
                      (df['latitude'] <= br_lat)]

        # convert the dataframe back to a json type
        df_to_json = {
            'key':df2.to_dict(orient='records')
        }
        matching_results=json.dumps(df_to_json)
        return matching_results, 200
    else:  
        return 'Data not loaded yet', 404
 
    return 'Unexpected error', 500

# Takes approximately 2m30s to process/convert full sized (~188Mb) dataset
@app.route('/upload/<string:file_to_process>', methods=['POST'])
def uploadNewCSV(file_to_process):
    if (request.method == 'POST'):
        convert(file_to_process)

        # Below is used for creating a collection in mlab
        # geoData = convert(file_to_process)
        # Collection size is much to large for mlab
        # Need to look at GridFS
        #user = mongo.db.geo
        #user.insert(geoData)

        return "I got a file named " + file_to_process, 200
    else:
        return "upload only supports the POST method", 400


if __name__ == '__main__':
    app.run(debug=True)