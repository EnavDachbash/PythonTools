#!/usr/bin/env python3

__author__ = 'Enav Hidekel <enav.hidekel@gmail.com>'
__creation_date__ = '20.02.19'

""" Be sure to log into vault before running this script! 
    This script will receive a variable and create a new 
    vault-mount according to it. """

import os
import sys
import hvac
import urllib3

urllib3.disable_warnings()


def get_token():
    try:
        f = open ('/Users/{0}/.vault-token'.format(os.environ['USER']))
        token = f.read().strip()
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise
    finally:
        f.close()
        return token


# Initialize the client using TLS
os.environ["VAULT_TOKEN"] = get_token()
client = hvac.Client(url='https://vault.dal.myhrtg.net:8200', token=os.environ["VAULT_TOKEN"], verify=False)

# ================== END GLOBAL ================== #


def init_destination_mount(mount_name, mount_version):
    client.sys.enable_secrets_engine(backend_type='kv', path=destination_mount, options={
        "version": mount_version
    })
    print('Destination Mount is: {}'.format(destination_mount))
    return destination_mount


def main():
    mount_name = input("Enter mount name: ")
    mount_version = input("Enter mount version: ")
    init_destination_mount(mount_name, mount_version)


if __name__ == '__main__':
    main()