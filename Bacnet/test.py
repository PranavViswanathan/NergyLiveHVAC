import requests
import json


with open('data.json', 'r') as f:
	data = json.load(f)


# print(json.dumps(data))

url = 'http://iot.inometrics.com/Api/add_data/'

payload = {'json_string': json.dumps(data), 'device_id': 1233}


response = requests.post(url, data=payload)


print(response.json())