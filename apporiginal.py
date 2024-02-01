import json
from time import time, sleep
import socket
import requests as requests

from Bacnet.lib import write_json_file, post_api
from config import config
from Bacnet.bacnet import BacnetModule, BACNET_CONFIG
from queue import Queue
from Bacnet.lib import is_connected
import asyncio

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

        if not is_connected(url=config.HOSTNAME, port=80):
            print(f"Connection Failed! Waiting to re-establish connection")
            sleep(60)
            timer = time()
            continue
        if not queue.empty():
            data = queue.get()
            payload = {"json_string": json.dumps(data), "device_code": config.DEVICE_ID}
            print(payload)
            try:
                if is_connected(url=config.HOSTNAME, port=80):
                    api_1_response = post_api(_url=config.READ_BACNET_DATA_URL, payload=payload)
                else:
                    sleep(180)
                    timer = time()
                    continue

                print(api_1_response.json())
            except Exception as e:
                print("Server Error - Json Not received.")
            # write_json_file('data2.json', payload)
        if time() - timer < 1:
            continue
        timer = time()
        payload = {'device_code': config.DEVICE_ID}
        if is_connected(url=config.HOSTNAME, port=80):
            api_2_response = post_api(_url=config.WRITE_BACNET_DATA_URL, payload=payload)
        else:
            sleep(180)
            timer = time()
            continue
        print(api_2_response.json())
        print(f"[1]  -->  {api_2_response.json().get('is_offline')}")
        # TODO Code for reconnecting devices. TEST in PROGRESS
        # TODO Issue BACNET_RECONNECT on TESTING.
        if api_2_response.json().get('is_offline'):
            print(f"[2]  -->  {api_2_response.json().get('is_offline')}")
            connection_check_counter += 1
            if connection_check_counter > 20:
                print(f"[3]  -->  {api_2_response.json().get('is_offline')}")
                bacnet_process.reconnect()
                connection_check_counter = 0
                sleep(2)
            if not bacnet_process.check_connectivity():
                print('not connected')
        else:
            connection_check_counter = 0

        if api_2_response.json().get('data'):
            for item in api_2_response.json()['data']:
                # print(f'{item["field_no"]}->{type(item["field_no"])}\t{item["value"]}->{type(item["value"])}')
                if bacnet_process.write_bacnet_object(item["field_no"], item["value"]):
                    payload = {'device_code': config.DEVICE_ID, 'field_no': item['field_no']}
                    api_3_response = post_api(_url=config.WRITE_ACK_URL, payload=payload)
                    print(api_3_response.json())
                    # send the data back
                    # data = [{'field_no': item['field_no'], 'value': item['value']}]
                    # payload = {"device_code": config.DEVICE_ID, 'json_string': json.dumps(data)}
                    # api_1_response = post_api(_url=config.READ_BACNET_DATA_URL, payload=payload)
                    # print(api_1_response.json())
        sleep(1)
