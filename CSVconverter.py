import csv
import json
import pandas as pd
import os 

# For faster testing use a smaller subset
#file = '../GeoLite2-City-CSV_20190521/GeoLite2-City-Blocks-IPv4-smallest-test.csv'
file = '../GeoLite2-City-CSV_20190521/GeoLite2-City-Blocks-IPv4.csv'
json_file = './parsedCSV.json'
lat_long_only_file = './latlong.csv'
# Only care about Lat/Long for this, if that changes need to remove from unwanted_keys
present_headers = ['network','geoname_id','registered_geoname_id','represented_country_geoname_id','is_anonymous_proxy','is_satellite_provider','postal_code','latitude','longitude','accuracy_radius']
unwanted_keys=['network','geoname_id','registered_geoname_id','represented_country_geoname_id','is_anonymous_proxy','is_satellite_provider','postal_code','accuracy_radius']

# Use Panda to pre-process CSV file and remove all columns except latitude and longitude
# Can use the existance of the latlong.csv file as a trigger to update the main data
df1 = pd.read_csv(file, names = present_headers, header = 0)
df2 = df1.drop(unwanted_keys, axis =1)
df3 = df2.to_csv(lat_long_only_file, index = False)

# Convert latlong.csv into parsedCSV.json
csv_rows = []
with open(lat_long_only_file) as rf:
    reader = csv.DictReader(rf)
    title = reader.fieldnames
    for row in reader:
        csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
    with open(json_file, 'w') as wf:    
        wf.write(json.dumps(csv_rows, sort_keys=False, indent=4, separators=(',', ': '),encoding="utf-8",ensure_ascii=False))
# remove latlong.csv file
os.remove(lat_long_only_file)



        
