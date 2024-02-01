BACNET_PORT = 0xBAC0

IP_ADDRESS = "10.0.220.249/24"
# HOSTNAME = 'iot.inometrics.com'
HOSTNAME = 'dashboard.nergylive.com'



READ_BACNET_DATA_URL = f'https://{HOSTNAME}/Api/add_data'
WRITE_BACNET_DATA_URL = f'https://{HOSTNAME}/Api/get_write_commands'
WRITE_ACK_URL = f'https://{HOSTNAME}/Api/send_write_ack'

DEVICE_ID = "DC30721093"