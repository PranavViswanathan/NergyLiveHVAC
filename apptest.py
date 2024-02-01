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
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import quote

#url = "https://www.dashboard.nergylive.com/Api/add_data"
#url = "http://iot.inometrics.com/Api/add_data"
print(BACNET_CONFIG)
url = "http://dashboard.nergylive.com/Api/add_data"
payload = {"json_string": BACNET_CONFIG, "device_code":'DC30721093'}

# Define retry strategy
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

try:
    response = session.post(url, data=payload)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)
    # Process the response...
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
