#!/usr/bin/env python3
__author__ = 'Enav Hidekel <enav.hidekel@gmail.com>'
__creation_date__ = '01/02/19'

""" Be sure to log into vault before running this script! 
    This script will retreive the user's token and set it to environment
    variable called 'VAULT_TOKEN'. """

import os
import sys

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


# Initialize the client using TLS + env Var
os.environ["VAULT_TOKEN"] = get_token()

# Verify the token is set as env var
print('env var set successful: {}'.format(os.environ["VAULT_TOKEN"]))