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

# ================== END GLOBAL ================== #


# This works
def list_secrets_in_path(path):
    objects_in_path = client.secrets.kv.v1.list_secrets(path=path)['data']['keys']
    for object in objects_in_path:
        abs_path = '{}/{}'.format(path, object)
        if object.endswith('/'):
            list_secrets_in_path(abs_path.strip('/'))
        else:
            print(abs_path)


def main():
    source_mount = input("Enter the source mount, and omit the /secret prefix:   ")
    list_secrets_in_path(source_mount)


if __name__ == '__main__':
    main()

