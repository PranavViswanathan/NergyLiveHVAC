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
headers = {"Content-Type": "application/json", "charset=ISO-8859-1"'Authorization': 'Bearer YOUR_API_KEY_OR_TOKEN' , 
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                  'Accept-Language': 'en-US,en;q=0.5'}

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
            api_host = config.HOSTNAME
            api_path = config.READ_BACNET_DATA_URL

            try:
                if is_valid_url(url=config.READ_BACNET_DATA_URL):
                    print(f'inside the api try')
                    print(data)
                    data = json.dumps(payload,ensure_ascii=False).encode('ISO-8859-1')
                    request = urllib.request.Request(api_path, data=data, headers=headers, method='POST')
                    with urllib.request.urlopen(request) as response:
                    # Check the response status
                        if response.getcode() == 200:
                            print("JSON data sent successfully to the API endpoint.")
                            print(response)
                        else:
                            print(f"Failed to send JSON data. Status code: {response.getcode()}")
            except Exception as e:
                print(f"An error occurred: {e}")
        if time() - timer < 1:
            continue
        timer = time()
        payload2 = {'device_code': config.DEVICE_ID}
        print(f'API 2 Request - {payload2}')
        ACKRES = {'is_offline': True}

        if is_valid_url(url=config.WRITE_BACNET_DATA_URL):
            try:
                api_path = config.WRITE_BACNET_DATA_URL
                data = json.dumps(payload2, ensure_ascii=False).encode('ISO-8859-1')
                request2 = urllib.request.Request(api_path, data=data, headers=headers, method='POST')
                with urllib.request.urlopen(request2) as response:
                    # Check the response status
                    if response.getcode() == 200:
                        print("JSON data sent successfully to the API endpoint.WRITE_BACNET_DATA_URL")
                        print(response)
                        response_data = response.read().decode('ISO-8859-1')
                        ACKRES = json.loads(response_data)
                        print(ACKRES)
                    else:
                        print(f"Failed to send JSON data. Status code: {response.getcode()}")
            except Exception as e:
                print(f"An error occurred: {e}")
                print(f'inside the api try2')
        else:
            sleep(180)
            timer = time()
            continue

        print(ACKRES)

        if ACKRES.get('is_offline'):
            print(f"[2]  -->  {ACKRES.get('is_offline')}")
            connection_check_counter += 1
            if connection_check_counter > 20:
                print(f"[3]  -->  {ACKRES.get('is_offline')}")
                bacnet_process.reconnect()
                connection_check_counter = 0
                sleep(2)
            if not bacnet_process.check_connectivity():
                print('not connected')
        else:
            connection_check_counter = 0
            print('not offline')

        if ACKRES.get('data'):
         for item in ACKRES['data']:
          print(f'{item}')
        if bacnet_process.write_bacnet_object(item["field_no"], item["value"]):
            payload = {'device_code': config.DEVICE_ID, 'field_no': item['field_no']}
            api_path2 = config.WRITE_ACK_URL
            data = json.dumps(payload, ensure_ascii=False).encode('ISO-8859-1')
            
            try:
                request2 = urllib.request.Request(api_path2, data=data, headers=headers, method='POST')
                with urllib.request.urlopen(request2) as response:
                    # Check the response status
                    if response.getcode() == 200:
                        print("JSON data sent successfully to the API3 endpoint.WRITE_ACK_URL")
                        print(response)
                        response_data = response.read().decode('ISO-8859-1')
                    else:
                        print(f"Failed to send JSON data. Status code: {response.getcode()}")
            except Exception as e:
                print(f"An error occurred during API3 request: {e}")
        sleep(1)
