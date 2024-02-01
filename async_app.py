import json
from time import time
import aiohttp
import requests as requests

from Bacnet.lib import write_json_file
from config import config
from Bacnet.bacnet import BacnetModule, BACNET_CONFIG
from queue import Queue
import asyncio

queue = Queue(maxsize=2)

bacnet_process = BacnetModule(queue)
# bacnet_process.setDaemon(True)
# bacnet_process.start()


async def post_data(session, url, post_data):
    async with session.post(url, data=post_data) as response:
        result = await response.json()
        return result


async def main():
    timer = time()
    async with aiohttp.ClientSession as session:
        task = []
        while True:
            if not queue.empty():
                data = queue.get()
                payload = {"json_string": json.dumps(data), "device_code": config.DEVICE_ID}
                task.append(asyncio.ensure_future(post_data(session, config.READ_BACNET_DATA_URL, payload)))
            if time() - timer < 1:
                received_data = asyncio.gather(*task)
                for items in received_data:
                    print(items.json())
                    if items.json().get('function') == 'get_write_commands' and items.json().get('data'):
                        for _data in items.json()['data']:
                            if bacnet_process.write_bacnet_object(_data["field_no"], _data["value"]):
                                payload = {'device_code': config.DEVICE_ID, 'field_no': _data['field_no']}
                                task.append(asyncio.ensure_future(post_data(session, config.WRITE_ACK_URL, payload)))
                                current_data = [{'field_no': _data['field_no'], 'value': _data['value']}]
                                payload = {"device_code": config.DEVICE_ID, 'json_string': json.dumps(current_data)}
                                task.append(asyncio.ensure_future(post_data(session, config.READ_BACNET_DATA_URL, payload)))
                continue
            timer = time()
            payload = {'device_code': config.DEVICE_ID}
            task.append(asyncio.ensure_future(post_data(session, config.WRITE_BACNET_DATA_URL, payload)))


if __name__ == '__main__':
    asyncio.run(main())
