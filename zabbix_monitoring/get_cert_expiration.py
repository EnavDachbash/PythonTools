#!/usr/bin/env python3

__author__ = 'Enav Hidekel <enav.hidekel@gmail.com>'
__creation_date__ = '12/05/19'

""" This script will list all certificates in a Palo Alto FW. """
import requests
import xml.etree.ElementTree as ElementTree
import urllib3
import json

# Disable cert verification:
urllib3.disable_warnings()

# ================== END GLOBAL ================== #


def calc_days2expiration(expiration):
    future = datetime.strptime(expiration, '%b %d %H:%M:%S %Y %Z').date()
    now = date.today()
    diff = future - now
    return diff.days


def main(host, cert):
    key = "LUFRPT1aRTZ2VHFQamI0bDRWdEpQWnYwbEdWQzZWTTQ9YzEzT0hkdENlM1IvWDd1eHZBbHgrTWZuVTJJYS9qY04xcXJDZTZiRmI0WT0="
    xml_result = requests.get(
        "https://{}/api/?type=op&cmd=<show><config><merged></merged></config></show>&key={}".format(host, key),
        verify=False)
    crt_xml_ob = ElementTree.fromstring(xml_result.content)
    entry = crt_xml_ob.find(".//certificate/entry[@name='{}']/not-valid-after".format(cert))
    if entry.text:
        expiration = entry.text
        return calc_days2expiration(expiration)
    else:
        print("something went wrong - no such certificate found")
        return 1


if __name__ == '__main__':
    main()
