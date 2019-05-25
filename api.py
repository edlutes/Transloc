from flask import Flask, request
from flask_pymongo import PyMongo
from CSVtogeoJSON import convert
from geojson import Feature, FeatureCollection, Point

import requests

app = Flask(__name__)

#app.config['MONGO_DBNAME'] = "First_Transloc"
app.config['MONGO_URI'] = "mongodb://testuser:Transloc@transloccluster-shard-00-00-fwvjk.mongodb.net:27017,transloccluster-shard-00-01-fwvjk.mongodb.net:27017,transloccluster-shard-00-02-fwvjk.mongodb.net:27017/test?ssl=true&replicaSet=TranslocCluster-shard-0&authSource=admin&retryWrites=true"

mongo = PyMongo(app)

@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name':'fooBar'})
    return 'Added Foo'

@app.route('/ipv4')
def ipv4():
    return "why is this working?!"

@app.route('/upload/<string:file_to_upload>', methods=['GET', 'POST'])
def uploadNewCSV(file_to_upload):
    if (request.method == 'POST'):
        geoData = convert(file_to_upload)
      
        user = mongo.db.geo
        user.insert(geoData)
        #for feature in geoData:
        #    user.insert(feature)
        # incorrect format..  1 document, added fields
        #user = mongo.db.geo
        #user.insert(geoData)
        return "I got a file named " + file_to_upload
    else:
        return "Something is wrong", 400


if __name__ == '__main__':
    app.run(debug=True)