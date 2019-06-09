import json
#import requests
from botocore.vendored import requests
from datetime import datetime
from dateutil import tz
import boto3

def lambda_handler(event, context):
    
	##Get the data from the open weather API
	
    #city_id = 1274220
	## units=metric in the below line its for getting the temperature in celcius.
    url = 'http://api.openweathermap.org/data/2.5/forecast?id=<<CITYID>>&APPID=<<APPID>>&units=metric'
    response = requests.post(url)
    json_data = response.json()

    ##Extract the rain prediction data from weather report
	
    next_3_hour_data = json_data['list'][0]
    prediction = (next_3_hour_data['weather'][0]['description'])
	
	## time conversion from UTC to IST
	
    utc_time = next_3_hour_data['dt_txt']
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Kolkata')
    utc = datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S')
    ist = utc.astimezone(to_zone)

    

    ## Publish the message to SNS topic
	
	## Create SNS client
    sns = boto3.client('sns')

    ## If there is a rain prediction then publish the message 
    if "rain" in prediction:
        rain_mm = next_3_hour_data['rain']['3h']
        msg = prediction + " is predicted in " + city_name + " at " + str(ist) + " and is expected to be of mm " + str(rain_mm)
        
        ## Publish a simple message to the specified SNS topic
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:068561486628:Rain_Alert',    
            Message=msg,    
        )
