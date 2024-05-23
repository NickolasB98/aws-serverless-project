import json
import boto3
import urllib3
import datetime

# REPLACE WITH YOUR DATA FIREHOSE NAME
FIREHOSE_NAME = 'PUT-S3-N4SGy'

def lambda_handler(event, context):
    
    http = urllib3.PoolManager()
    
    r = http.request("GET", "https://api.open-meteo.com/v1/forecast?latitude=53.2192&longitude=6.5667&current=temperature_2m,relative_humidity_2m,rain,showers,cloud_cover,wind_speed_10m&timezone=Europe%2FBerlin")
    
    # turn it into a dictionary
    r_dict = json.loads(r.data.decode(encoding='utf-8', errors='strict'))
    
    # extract pieces of the dictionary
    processed_dict = {}
    processed_dict['latitude'] = r_dict['latitude']
    processed_dict['longitude'] = r_dict['longitude']
    processed_dict['time'] = r_dict['current']['time']
    processed_dict['temp'] = r_dict['current']['temperature_2m']
    processed_dict['row_ts'] = str(datetime.datetime.now())
    processed_dict['humidity'] = r_dict['current']['relative_humidity_2m']
    processed_dict['rain'] = r_dict['current']['rain']
    processed_dict['showers'] = r_dict['current']['showers']
    processed_dict['cloud_cover'] = r_dict['current']['cloud_cover']
    processed_dict['wind_speed'] = r_dict['current']['wind_speed_10m']  
    
    # turn it into a string and add a newline
    msg = str(processed_dict) + '\n'
    
    fh = boto3.client('firehose')
    
    reply = fh.put_record(
        DeliveryStreamName=FIREHOSE_NAME,
        Record = {
                'Data': msg
                }
    )

    return reply