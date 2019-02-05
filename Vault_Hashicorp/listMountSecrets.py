#!/usr/bin/env python3
""" Be sure to log into vault before running this script """
import os
import sys
import hvac
import urllib3

__author__ = 'Enav Hidekel <enav.hidekel@gmail.com>'
__creation_date__ = '31/01/19'

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


def list_secrets_in_path(mount_version, source_mount, dir_in_mount, final_secrets_list):
    if '1' in mount_version:
        objects_in_path = client.secrets.kv.v1.list_secrets(path=dir_in_mount, mount_point=source_mount)['data']['keys']
    else:
        objects_in_path = client.secrets.kv.v2.list_secrets(path=dir_in_mount, mount_point=source_mount)['data']['keys']
    for object in objects_in_path:
        abs_path = '{}/{}'.format(dir_in_mount, object)
        if object.endswith('/'):
            list_secrets_in_path(mount_version, source_mount, abs_path.strip('/'), final_secrets_list)
        else:
            final_secrets_list.append('{}/{}'.format(source_mount, abs_path.lstrip(('/'))))
    return final_secrets_list


def read_secret_from_original_mount(secret):
    read_secret_result = client.secrets.kv.v1.read_secret(secret)
    return read_secret_result['data']


def write_secret_to_new_mount(destination_mount, secret):
    print('Writing {} to {}'.format(secret, destination_mount))
    client.secrets.kv.v1.create_or_update_secret(path=destination_mount, secret=secret)
    return 'Now Writing {}/{}'.format(destination_mount, secret)


def get_mount_version(source_mount):
    secret_backend_config=client.sys.read_mount_configuration(source_mount)
    if 'options' in secret_backend_config.keys():
        print('mount is v2')
        secret_version='v2'
    else:
        secret_version='v1'
        print('mount is v1')
    return secret_version


def main():
    source_mount = input("Enter the source mount:   ")
#    destination_mount = input("Enter the destination mount, and omit the /secret prefix:   ")
    mount_version = get_mount_version(source_mount)
    final_secrets_list = list()
    original_mount_secrets = list_secrets_in_path(mount_version, source_mount, '', final_secrets_list)
    print(original_mount_secrets)

#    for secret in original_mount_secrets:
#        write_secret_to_new_mount('{}/{}'.format(destination_mount, secret), read_secret_from_original_mount(secret))



if __name__ == '__main__':
    main()
