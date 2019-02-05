#!/usr/bin/env python3

__author__ = 'Enav Hidekel <enav.hidekel@gmail.com>'
__creation_date__ = '31/01/19'

""" Be sure to log into vault before running this script!
    This script will list all secrets in a certain mount. """

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


# This function will determine the mount's version.
def get_mount_version(mount):
    secret_backend_config=client.sys.read_mount_configuration(mount)
    if 'options' in secret_backend_config.keys():
        print('mount version is 2')
        secret_version='v2'
    else:
        secret_version='v1'
        print('mount version is 1')
    return secret_version


# This function will list all secrets in mount.
def list_secrets_in_path(mount_version, mount, dir_in_mount, final_secrets_list):
    if '1' in mount_version:
        objects_in_path = client.secrets.kv.v1.list_secrets(path=dir_in_mount, mount_point=mount)['data']['keys']
    else:
        objects_in_path = client.secrets.kv.v2.list_secrets(path=dir_in_mount, mount_point=mount)['data']['keys']
    for object in objects_in_path:
        abs_path = '{}/{}'.format(dir_in_mount, object)
        if object.endswith('/'):
            list_secrets_in_path(mount_version, mount, abs_path.strip('/'), final_secrets_list)
        else:
            final_secrets_list.append('{}/{}'.format(mount, abs_path.lstrip(('/'))))
    return final_secrets_list


def main():
    mount = input("Enter the mount you wish to list: ")
    mount_version = get_mount_version(mount)
    final_secrets_list = list()
    original_mount_secrets = list_secrets_in_path(mount_version, mount, '', final_secrets_list)
    print(*original_mount_secrets, sep="\n")


if __name__ == '__main__':
    main()

