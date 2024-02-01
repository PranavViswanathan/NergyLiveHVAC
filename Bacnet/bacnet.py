import platform
from queue import Queue
from threading import Thread
from time import sleep
import os
import BAC0
import socket

from Bacnet.lib import read_json_file, is_connected
from config import config


file_path = os.path.join(os.path.dirname(__file__),  'devices.json')
BACNET_CONFIG = read_json_file(file_path)

# BACNET_OBJECT = BAC0.lite(ip=socket.gethostbyname(socket.getfqdn()))


class BacnetModule:
    def __init__(self, queue: Queue):
        super(BacnetModule).__init__()
        # Thread.__init__(self)
        # self.ip = socket.gethostbyname(socket.getfqdn())
        # BAC0.log_level('debug')
        #self.bacnet = BAC0.lite(ip=config.IP_ADDRESS)
        self.bacnet = BAC0.lite(ip=config.IP_ADDRESS)
        self.device_list = []
        self.q = queue
        self.stopped = False
        self.get_devices()
        self.task = Thread(target=self.run)
        self.task.start()

    @staticmethod
    def is_connected(_url):
        if platform.system() == 'Windows':
            count = 'n'
        else:
            count = 'c'
        return False if os.system(f'ping -{count} 1 {_url}') else True

    def get_devices(self):
        for item in BACNET_CONFIG.values():
            for module in item:
                device = {}
                device['ip'] = module["ip"]
                device['id'] = module['id']
                device['device'] = self.get_device(module["ip"], module["id"])
                device['name'] = str(device['device']).split(' ')[0]
                device['property'] = {'address': module['ip'], 'objects': {}}
                for objects in module['objectList']:
                    device['property']['objects'][f'{objects["type"]}:{objects["id"]}'] = ['presentValue']
                self.device_list.append(device)
        return self.device_list

    def get_device(self, ip: str, device_id: int):
        return BAC0.device(ip, device_id, self.bacnet, poll=3)

    def establish_connection(self):
        if self.bacnet:
            self.bacnet.disconnect()
            self.bacnet = None
            sleep(2)
        self.bacnet = BAC0.lite(ip=config.IP_ADDRESS)
        self.device_list = []
        self.stopped = True
        self.get_devices()
        self.task.start()

    def stop(self):
        print('Stopping the Bacnet read thread')
        self.stopped = True
        self.task.join()
        if self.bacnet:
            self.bacnet.disconnect()
            self.bacnet = None
        sleep(2)

    def check_thread_status(self):
        return self.task.is_alive()

    def reconnect(self):
        self.stop()
        while not self.q.empty():
            temp = self.q.get()
        self.establish_connection()
        self.task.start()

    def check_connectivity(self):
        # Check connectivity to the Devices after connecting.
        check = 0
        counter = 0
        for item in self.device_list:
            print(f"{check=}, {counter=}")
            if self.is_connected(item['ip']):
                # if 'Connected' in item['device']:
                check += 1
            else:
                check -= 1
            counter += 1
        return check == counter

    def read_property(self, device, _property):
        try:
            payload = device.read_property(_property)
        except Exception as e:
            print(e)
            print(self.bacnet)
        else:
            return payload

    def run(self):
        while True:
            payload = []
            for items in BACNET_CONFIG.values():
                for deviceList in items:
                    # device = self.get_device(deviceList["ip"], deviceList["id"])
                    device = list(filter(lambda item: item['id'] == deviceList["id"], self.device_list))[0]['device']
                    for objects in deviceList['objectList']:
                        field = {'field_no': objects['field_no']}
                        property = (objects['type'], objects['id'], 'presentValue')
                        if 'binary' in objects['type']:
                            field['value'] = 1 if self.read_property(device, property) == 'active' else 0
                        else:
                            field['value'] = self.read_property(device, property)
                        payload.append(field)

                        if self.stopped:
                            break
                    print(f'Device: {device}')
            print('Writing Data')
            self.q.put(payload)
            sleep(5)
        # sleep(3)

    def write_bacnet_object(self, field_no: int, value, priority=7):
        for items in BACNET_CONFIG.values():
            for deviceList in items:
                if list(filter(lambda item: item['field_no'] == int(field_no), deviceList['objectList'])):
                    device = list(filter(lambda item: item['id'] == deviceList["id"], self.device_list))[0]['device']
                    field = list(filter(lambda item: item['field_no'] == int(field_no), deviceList['objectList']))[0]
                else:
                    continue
                property = (field["type"], field["id"], 'presentValue')
                _value = float(value) if 'binary' not in field['type'] else 'active' if value == '1' else 'inactive'
                device.write_property(property, value=_value, priority=priority)
                if device.read_property(property) == _value:
                    return True
                else:
                    return False

    def read_single_object(self, field_no: int, value):
        pass

# output = []
# for items in device_list:
#     output.append(bacnet.readMultiple(items['ip'], request_dict=items['property']))
# for item in output:
# 	for key, value in item.items():
# 		temp = list(filter(lambda item: item
#
#       temp['field_no'] = field_no
#       temp['value'] = value[0][1]
#       field_no += 1
#       payload.append(temp)
