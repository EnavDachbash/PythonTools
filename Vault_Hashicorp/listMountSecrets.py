#!/usr/bin/env python3
""" Be sure to log into vault before running this script """
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
print('env var set successful')

# ================== END GLOBAL ================== #

# # This works
# def list_secrets_in_path(path):
#     objects_in_path = client.secrets.kv.v1.list_secrets(path=path)['data']['keys']
#     for object in objects_in_path:
#         abs_path = '{}/{}'.format(path, object)
#         if object.endswith('/'):
#             list_secrets_in_path(abs_path.strip('/'))
#         else:
#             print(abs_path)


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


def read_secret_from_original_mount(secret,source_mount):
    print('Reading secret {}'.format(secret))
    read_secret_result = client.secrets.kv.v1.read_secret(path=secret, mount_point=source_mount)
    return 'Enav'


def write_secret_to_new_mount(path, value):
    print('Writing {} to {}'.format(value, path))


def main():
    source_mount = input("Enter the source mount, and omit the /secret prefix:   ")
    destination_mount = input("Enter the destination mount, and omit the /secret prefix:   ")
    final_secrets_list = list()
    original_mount_secrets = list_secrets_in_path(source_mount, final_secrets_list)
    print(original_mount_secrets)
    for secret in original_mount_secrets:
        write_secret_to_new_mount('{}/{}'.format(destination_mount, secret), read_secret_from_original_mount(secret))


if __name__ == '__main__':
    main()
