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

        #if not is_connected(url=config.HOSTNAME, port=443):
        #    print(f"Connection Failed! Waiting to re-establish connection")
        #    sleep(60)
        #    timer = time()
        #    continue
        if not queue.empty():
            data = queue.get()
            payload = {"json_string": json.dumps(data), "device_code": config.DEVICE_ID}
            print(f"printing payload before POST request")
            # Define retry strategy
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504],
            )

            # Apply retry strategy to the HTTP adapter
            adapter = HTTPAdapter(max_retries=retry_strategy)
            print(f'strategy created')
            
            # Create a session with the retry-enabled adapter
            session = requests.Session()
            print(f'session created')
            session.mount("https://", adapter)
            print(f'session mount created')
            try:
                print(f'starting try')
                #if is_connected(url=config.HOSTNAME, port=80):
                print(f'connection success try')
                url = config.READ_BACNET_DATA_URL
                #print(payload)

                #print(payload)
                customurl = "http://dashboard.nergylive.com/Api/add_data"
                print(f'url created')
                # Use json parameter instead of data for JSON payload
                #response = session.post(url=customurl, json=payload)
                response = session.post(url=customurl, data=payload)
                print(f'request send')
                # Check if the request was successful (status code 2xx)
                if response.status_code // 100 == 2:
                    print("Request was successful!")
                    print("Response success Status Code:", response.status_code)
                    print("Response success Content:", response.text)
                else:
                    print("Response fail Status Code:", response.status_code)
                    print("Response fail Content:", response.text)
                #print(response)
                #print(f'inside the api try and not connected' - {payload})
               #else:
               #    print(f'connection fail try')
               #    print(f'inside the api try and not connected' - {payload})
               #    sleep(180)
               #    timer = time()
               #    continue
               # print(f'API 1 response {api_1_response.json()}')
            except requests.exceptions.RequestException as e:
                print("Response Content:", e)
                print("API 1 Response - Server Error - Json Not received.")
            # write_json_file('data2.json', payload)
        if time() - timer < 1:
            continue
        timer = time()
        payload = {'device_code': config.DEVICE_ID}
        print(f'API 2 Request - {payload}')

