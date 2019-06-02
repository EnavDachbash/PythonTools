#!/usr/bin/env python3

__author__ = 'Enav Hidekel <enav.hidekel@gmail.com>'
__creation_date__ = '12/05/19'

""" This script will list all certificates in a Palo Alto FW. """

"""for python 2.7 support:
import datetime
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import date
from datetime import datetime
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
"""
import requests
import xml.etree.ElementTree as ElementTree
import urllib3
import json
import sys

# Disable cert verification:
urllib3.disable_warnings()
# ================== END GLOBAL ================== #

# Get key as string var:
def get_key_str(file_path):
    with open(file_path, "r") as read_file:
        data = json.load(read_file)
    keystr = data["payload"]["key"]
    return keystr


# Get cert expiration:
def calc_days2expiration(expiration):
    future = datetime.strptime(expiration, '%b %d %H:%M:%S %Y %Z').date()
    now = date.today()
    diff = future - now
    return diff.days
""" for python 2.7 support in this function:
# Get cert expiration:
def calc_days2expiration(expiration):
    future = datetime.strptime(expiration, '%b %d %H:%M:%S %Y %Z')
    now = datetime.combine(date.today(), datetime.min.time())
    diff = future - now
    return diff.days"""

def main(host, cert):
    key = get_key_str("/Users/enav.hidekel/Documents/dallas_key.json")
    xml_result = requests.get(
        "https://{}/api/?type=op&cmd=<show><config><merged></merged></config></show>&key={}".format(host, key),
        verify=False)
    crt_xml_ob = ElementTree.fromstring(xml_result.content)
    entry = crt_xml_ob.find(".//certificate/entry[@name='{}']/not-valid-after".format(cert))
    if entry.text:
        expiration = entry.text
        print(calc_days2expiration(expiration))
    else:
        print("something went wrong - no such certificate found")
        return 1


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
