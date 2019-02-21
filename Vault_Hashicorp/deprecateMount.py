#!/usr/bin/env python3

__author__ = 'Enav Hidekel <enav.hidekel@gmail.com>'
__creation_date__ = '31/01/19'

""" Be sure to log into vault before running this script! 
    This script will read all secrets in <source_mount> and
    write them to <destination_mount>. """

import os
import sys
import hvac
import urllib3


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
urllib3.disable_warnings()
os.environ["VAULT_TOKEN"] = get_token()
client = hvac.Client(url='https://vault.dal.myhrtg.net:8200', token=os.environ["VAULT_TOKEN"], verify=False)

# ================== END GLOBAL ================== #


def get_mount_version(mount):
    secret_backend_config = client.sys.read_mount_configuration(mount)
    if 'options' in secret_backend_config:
        if secret_backend_config['options']['version'] == '2':
            print('Analysis: mount version is 2')
            mount_ver = 'v2'
        else:
            mount_ver = 'v1'
            print('Analysis: mount version is 1')
    else:
        mount_ver = 'v1'
        print('Analysis: mount version is 1')
    return mount_ver


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
            final_secrets_list.append('{}'.format(abs_path.lstrip('/')))
#           NOTE: no need for the source_mount parameter here:
#           final_secrets_list.append('{}/{}'.format(source_mount, abs_path.lstrip(('/'))))
    return final_secrets_list


def read_secret_from_original_mount(mount_version, source_mount, secret):
    if '1' in mount_version:
        read_secret_result = client.secrets.kv.v1.read_secret(mount_point=source_mount, path=secret)['data']
    else:
        read_secret_result = client.secrets.kv.v2.read_secret_version(mount_point=source_mount, path=secret)['data']['data']
    return read_secret_result


def write_secret_to_new_mount(destination_mount, secret, mount_version, content):
    if '1' in mount_version:
        client.secrets.kv.v1.create_or_update_secret(mount_point=destination_mount, path=secret, secret=content)
    else:
        client.secrets.kv.v2.create_or_update_secret(mount_point=destination_mount, path=secret, secret=content)
    return 'Now Writing {}/{}'.format(destination_mount, secret)


def init_destination_mount(source_mount, mount_version):
    ver = mount_version[1]
    print('Going to create new mount:  deprecated/{} of version {}'.format(source_mount, ver))
    destination_mount = 'deprecated/{}'.format(source_mount)
    client.sys.enable_secrets_engine(backend_type='kv', path=destination_mount, options={
        "version": ver
    })
    return destination_mount


def main():
    source_mount = input("Enter the source mount: ")
    mount_version = get_mount_version(source_mount)
    final_secrets_list = list()
    secrets_list = list_secrets_in_path(mount_version, source_mount, '', final_secrets_list)
    destination_mount = init_destination_mount(source_mount, mount_version)
    print('Starting secrets copy from source mount')
    for secret in secrets_list:
        content = read_secret_from_original_mount(mount_version, source_mount, secret)
        write_secret_to_new_mount(destination_mount, secret, mount_version, content)
    print('All done! secrets written to: {}'.format(destination_mount))


if __name__ == '__main__':
    main()
