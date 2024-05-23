import json
import boto3
import urllib3
import datetime

# REPLACE WITH YOUR DATA FIREHOSE NAME
FIREHOSE_NAME = 'PUT-S3-N4SGy'

def lambda_handler(event, context):
    
    http = urllib3.PoolManager()
    
    r = http.request("GET", "https://archive-api.open-meteo.com/v1/archive?latitude=53.2192&longitude=6.5667&start_date=2024-03-01&end_date=2024-05-15&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,daylight_duration,sunshine_duration,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max&timezone=Europe%2FBerlin")
    
    # turn it into a dictionary
    r_dict = json.loads(r.data.decode(encoding='utf-8', errors='strict'))
    
    time_list = []
    for val in r_dict['daily']['time']:
        time_list.append(val)
    
    temp_mean_list = []
    for temp in r_dict['daily']['temperature_2m_mean']:
        temp_mean_list.append(temp)
        
    temp_max_list = []
    for temp in r_dict['daily']['temperature_2m_max']:
        temp_max_list.append(temp)
    
    temp_min_list = []
    for temp in r_dict['daily']['temperature_2m_min']:
        temp_min_list.append(temp)
    
    daylight_list = []
    for val in r_dict['daily']['daylight_duration']:
        daylight_list.append(val)
        
    sunshine_list = []
    for val in r_dict['daily']['sunshine_duration']:
        sunshine_list.append(val)
        
    precipitation_list = []
    for val in r_dict['daily']['precipitation_sum']:
        precipitation_list.append(val)
        
    wind_speed_list = []
    for val in r_dict['daily']['wind_speed_10m_max']:
        wind_speed_list.append(val)
    
    wind_gusts_list = []
    for val in r_dict['daily']['wind_gusts_10m_max']:
        wind_gusts_list.append(val)
    
    
    # extract pieces of the dictionary
    processed_dict = {}
    
    # append to string running_msg
    running_msg = ''
    for i in range(len(time_list)):
        # construct each record
        processed_dict['latitude'] = r_dict['latitude']
        processed_dict['longitude'] = r_dict['longitude']
        processed_dict['time'] = time_list[i]
        processed_dict['temp_c_mean'] = temp_mean_list[i]
        processed_dict['temp_c_max'] = temp_max_list[i]
        processed_dict['temp_c_min'] = temp_min_list[i]
        processed_dict['daylight_duration'] = daylight_list[i]
        processed_dict['sunshine_duration'] = sunshine_list[i]
        processed_dict['precipitation_sum'] = precipitation_list[i]
        processed_dict['wind_speed_max'] = wind_speed_list[i]
        processed_dict['wind_gusts_max'] = wind_gusts_list[i]
        processed_dict['row_ts'] = str(datetime.datetime.now())
    
        # add a newline to denote the end of a record
        # add each record to the running_msg
        running_msg += str(processed_dict) + '\n'
        
    # cast to string
    running_msg = str(running_msg)
    fh = boto3.client('firehose')
    
    reply = fh.put_record_batch(
        DeliveryStreamName=FIREHOSE_NAME,
        Records = [
                {'Data': running_msg}
                ]
    )

    return reply