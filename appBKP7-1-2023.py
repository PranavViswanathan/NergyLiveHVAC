import json
from time import time, sleep
import socket
import requests as requests

from Bacnet.lib import write_json_file, post_api,is_valid_url
from config import config
from Bacnet.bacnet import BacnetModule, BACNET_CONFIG
from queue import Queue
from Bacnet.lib import is_connected
import asyncio
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import quote
import urllib3
from urllib import request, parse
import urllib.request
import http.client

queue = Queue(maxsize=10)

bacnet_process = BacnetModule(queue)
sleep(2)
# bacnet_process.setDaemon(True)
# bacnet_process.start()

if __name__ == '__main__':
    timer = time()
    connection_check_counter = 0
    while True:
        if not bacnet_process.check_thread_status():
            bacnet_process = None
            bacnet_process = BacnetModule(queue)
            sleep(2)

        if not is_valid_url(url=config.READ_BACNET_DATA_URL):
            print(f"Connection Failed! Waiting to re-establish connection")
            sleep(60)
            timer = time()
            continue
        if not queue.empty():
            data = queue.get()
            payload = {"json_string": json.dumps(data), "device_code": config.DEVICE_ID}
            
            print(f"printing payload before POST request")
            print(payload)
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504],
            )

            # Apply retry strategy to the HTTP adapter
            adapter = HTTPAdapter(max_retries=retry_strategy)

            # Create a session with the retry-enabled adapter
            session = requests.Session()
            session.mount("https://", adapter)
            api_host = "dashboard.nergylive.com/Api/add_data"
            api_path = "https://dashboard.nergylive.com/Api/add_data"

            try:
                if is_valid_url(url=config.READ_BACNET_DATA_URL):
                    #print(f'inside the api try'-{payload})
                    print(f'inside the api try')
                    #api_1_response = post_api(_url=config.READ_BACNET_DATA_URL, payload=payload)
                    url = "http://dashboard.nergylive.com/Api/add_data"
                    #url = 'http://iot.inometrics.com.com/Api/add_data/'
                    # api_1_response = post_api(_url=config.READ_BACNET_DATA_URL, payload=payload)
                    #api_1_response = requests.post(url=url, data=payload)
                    headers = {"Content-Type": "application/json", "charset=ISO-8859-1"'Authorization': 'Bearer YOUR_API_KEY_OR_TOKEN' , 
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5'}
                    #api_1_response = requets.post(url, data=payload, headers)
                    #api_1_response = requests.post(url, data=json.dumps(payload), headers=headers)
                    #data = {"key1": "value1", "key2": "value2"}
                    #data = {"device_code": "DC30721093", "json_string": "value2"}
                    #data = json.dumps(payload).encode("utf-8")  # Encode JSON data as bytes
                    #chunksize = 1024
                    #for i in range(0, len(data), chunksize):
                    #    chunk = data[i:i+chunksize]
                    #chunk_list =list(chunk)# Either encode manually
                    #data = json.dumps(payload).encode("utf-8")

# Or use json=data directly
                    #response = requests.post(url, json=payload, headers=headers, verify=True)


                    print(data)
                    #response = requests.post(url, json = payload, headers = headers)
                    #request = urllib.request.Request(url, data, headers)
                    #response = urllib.request.urlopen(request)

                    #response_data = response.read().decode("utf-8")  # Decode response as text
                    #print("Response:", response_data)
                    #print("Response ::", response.json())
                    #response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
                    #Assuming the server responds with JSON, you can print or process the JSON content
                    #connection = http.client.HTTPSConnection(api_host)

                    # Make a POST request to the API endpoint with the JSON data
                    #connection.request('POST', api_path, body=json.dumps(payload), headers=headers)
                     # Get the response from the server
                    #response = connection.getresponse()
                    #data = json.dumps(payload).encode('utf-8')
                    data = json.dumps(payload,ensure_ascii=False).encode('ISO-8859-1')
                    request = urllib.request.Request(api_path, data=data, headers=headers, method='POST')

                    # Check the response status
                   
                    with urllib.request.urlopen(request) as response:
                    # Check the response status
                        if response.getcode() == 200:
                            print("JSON data sent successfully to the API endpoint.")
                            print(response)
                            #print(response.read().decode('utf-8'))
                        else:
                            print(f"Failed to send JSON data. Status code: {response.getcode()}")
                        print(response.read().decode('utf-8'))

                    # Process the response...
                #else:
                #    print(f'inside the api try and not connected' - {payload})
                #    sleep(180)
                #    timer = time()
                #    continue


            #except requests.exceptions.RequestException as e:
            #    print("API 1 Response - Server Error::::: - Json Not received.")
            #    print(f"Error: {e}")
            # write_json_file('data2.json', payload)
            #except requests.exceptions.HTTPError as errh:
            #    print(f"HTTP Error: {errh}")
            #except requests.exceptions.ConnectionError as errc:
            #    print(f"Error Connecting: {errc}")
            #except requests.exceptions.Timeout as errt: 
            #    print(f"Timeout Error: {errt}")
            #except requests.exceptions.RequestException as err:
            #    print(f"Request Error: {err}")
            #except json.JSONDecodeError as json_err:
            #    print(f"JSON Decode Error: {json_err}")

            except Exception as e:
                print(f"An error occurred: {e}")
        if time() - timer < 1:
            continue
        timer = time()
        payload = {'device_code': config.DEVICE_ID}
        print(f'API 2 Request - {payload}')

        # if is_connected(url=config.HOSTNAME, port=80):
        #     api_2_response = post_api(_url=config.WRITE_BACNET_DATA_URL, payload=payload)
        # else:
        #     sleep(180)
        #     timer = time()
        #     continue
        # try:
        #     print(api_2_response)
        #     print(f"[1]  -->  {api_2_response.json().get('is_offline')}")
        #     # TODO Code for reconnecting devices. TEST in PROGRESS
        #     # TODO Issue BACNET_RECONNECT on TESTING.
        #     if api_2_response.json().get('is_offline'):
        #         print(f"[2]  -->  {api_2_response.json().get('is_offline')}")
        #         connection_check_counter += 1
        #         if connection_check_counter > 20:
        #             print(f"[3]  -->  {api_2_response.json().get('is_offline')}")
        #             bacnet_process.reconnect()
        #             connection_check_counter = 0
        #             sleep(2)
        #         if not bacnet_process.check_connectivity():
        #             print('not connected')
        #     else:
        #         connection_check_counter = 0
        #
        #     if api_2_response.json().get('data'):
        #         for item in api_2_response.json()['data']:
        #             # print(f'{item["field_no"]}->{type(item["field_no"])}\t{item["value"]}->{type(item["value"])}')
        #             if bacnet_process.write_bacnet_object(item["field_no"], item["value"]):
        #                 payload = {'device_code': config.DEVICE_ID, 'field_no': item['field_no']}
        #                 api_3_response = post_api(_url=config.WRITE_ACK_URL, payload=payload)
        #                 print(api_3_response.json())
        #                 # send the data back
        #                 # data = [{'field_no': item['field_no'], 'value': item['value']}]
        #                 # payload = {"device_code": config.DEVICE_ID, 'json_string': json.dumps(data)}
        #                 # api_1_response = post_api(_url=config.READ_BACNET_DATA_URL, payload=payload)
        #                 # print(api_1_response.json())
        #     sleep(1)
        # except Exception as e:
        #     print(f"API 2 response Error - {e}")
