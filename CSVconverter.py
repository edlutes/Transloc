import csv
import json

file = '../GeoLite2-City-CSV_20190521/GeoLite2-City-Blocks-IPv4-smallest-test.csv'
json_file = './parsedCSV.json'
# Only care about Lat/Long for this
present_headers = ['network','geoname_id','registered_geoname_id','represented_country_geoname_id','is_anonymous_proxy','is_satellite_provider','postal_code','latitude','longitude','accuracy_radius']
headers = ['longitude', 'latitude']
unwanted_keys=['network','geoname_id','registered_geoname_id','represented_country_geoname_id','is_anonymous_proxy','is_satellite_provider','postal_code','accuracy_radius']



csv_rows = []
with open(file) as rf:
    reader = csv.DictReader(rf)
    title = reader.fieldnames
    for row in reader:
        for i in range(len(title)):
            if title[i] in headers:
               csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
    with open(json_file, 'w') as wf:    
        wf.write(json.dumps(csv_rows, sort_keys=False, indent=4, separators=(',', ': '),encoding="utf-8",ensure_ascii=False))


        
