#!/usr/bin/env python3

__author__ = 'Enav Hidekel <enav.hidekel@gmail.com>'
__creation_date__ = '11/04/19'

""" This script will list all certificates in a Palo Alto FW. """
import requests
import xml.etree.ElementTree as ElementTree
import urllib3
import json

# Disable cert verification:
urllib3.disable_warnings()

# ================== END GLOBAL ================== #


# Get key as string var
def get_key_str(file_path):
    with open(file_path, "r") as read_file:
        data = json.load(read_file)
    keystr = data["payload"]["key"]
    return keystr


# Get Hosts List + Their IP
def get_hosts_list(xml_ob):
    hosts_dict = dict()
    for entry in xml_ob.iterfind(".//hostname/.."):
        hostname = entry.find("hostname").text
        ip_addr = entry.find("ip-address").text
        hosts_dict.update({hostname: ip_addr})

    def filter_hosts_list(hosts_dict):
        hosts = dict()
        for key in hosts_dict.keys():
            if 'Dallas' in key:
                hosts.update({key: hosts_dict[key]})
        return hosts
    return filter_hosts_list(hosts_dict)


# Get Certificates List
def get_certificate_list(crt_xml_ob):
    for certificate in crt_xml_ob.iterfind(".//certificate"):
        certs_list = list()
        for entry in crt_xml_ob.iterfind(".//certificate/entry"):
            cert_name = entry.attrib['name']
            #cert_expiration = entry.find("not-valid-after").text
            certs_list.append(cert_name)
    return certs_list


def main():
    xml_hosts_result = requests.get(
        'https://pano.mhutils.com/api/?key={}&type=op&cmd=<show><devices><all></all></devices></show>'.format(
            get_key_str("/Users/enav.hidekel/Documents/panorama_key.json")),
        verify=False)
    xml_ob = ElementTree.fromstring(xml_hosts_result.content)
    hosts_dict = get_hosts_list(xml_ob)
    output_discovery = {'data': []}
    for node in hosts_dict:
        key = get_key_str("/Users/enav.hidekel/Documents/dallas_key.json")
        xml_result = requests.get("https://{}/api/?type=op&cmd=<show><config><merged></merged></config></show>&key={}".format(hosts_dict[node], key), verify=False)
        crt_xml_ob = ElementTree.fromstring(xml_result.content)
        crt_list = get_certificate_list(crt_xml_ob)
        for crt in crt_list:
            output_discovery['data'].append({'{#HOSTNAME}': node, '{#IPADDRESS}': hosts_dict[node], '{#CRTNAME}': crt})
    final_output = json.dumps(output_discovery)
    print(final_output)


if __name__ == '__main__':
    main()
