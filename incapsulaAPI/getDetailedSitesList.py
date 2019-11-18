#!/usr/bin/env python3

__author__ = 'Enav Hidekel <enav.hidekel@gmail.com>'
__creation_date__ = '28/02/19'

"""This script returns all site assosiated with the provided account"""


import os
import json
import requests


def set_script_env():
    os.environ["API_ID"] = "31143"
    os.environ["API_KEY"] = "485b35fe-0dc2-44a5-b6d7-e060ed138a5e"


def list_detailed_sites(api_endpoint):
    url = api_endpoint + 'prov/v1/sites/list'
    payload = {
        'api_id': os.environ.get('API_ID'),
        'api_key': os.environ.get('API_KEY'),
        'account': '173601',
    }
    r = requests.post(url, data=payload)
    results = json.loads(r.text)
    sites = {}
    for site in results['sites']:
        site_id = str(site['site_id'])
        sites[site_id] = site['domain']
    return sites


def main():
    set_script_env()
    sites = list_detailed_sites('https://my.incapsula.com/api/')
    print('\n'.join([' : '.join([k, v]) for k, v in sites.items()]))


if __name__ == '__main__':
    main()
