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


def list_secrets_in_path(path, final_secrets_list):
    # check the versioned path
    objects_in_path = client.secrets.kv.v1.list_secrets(path=path)['data']['keys']
    for object in objects_in_path:
        abs_path = '{}/{}'.format(path, object)
        if object.endswith('/'):
            list_secrets_in_path(abs_path.strip('/'), final_secrets_list)
        else:
            final_secrets_list.append(abs_path)
    return final_secrets_list


def read_secret_from_original_mount(secret):
    read_secret_result = client.secrets.kv.v1.read_secret(secret)
    return read_secret_result['data']


def write_secret_to_new_mount(destination_mount, secret):
    print('Writing {} to {}'.format(secret, destination_mount))
    client.secrets.kv.v1.create_or_update_secret(path=destination_mount, secret=secret)
    return 'Now Writing {}/{}'.format(destination_mount, secret)


def main():
    source_mount = input("Enter the source mount, and omit the /secret prefix:   ")
    destination_mount = input("Enter the destination mount, and omit the /secret prefix:   ")
    final_secrets_list = list()
    original_mount_secrets = list_secrets_in_path(source_mount, final_secrets_list)

    for secret in original_mount_secrets:
        write_secret_to_new_mount('{}/{}'.format(destination_mount, secret), read_secret_from_original_mount(secret))



if __name__ == '__main__':
    main()
