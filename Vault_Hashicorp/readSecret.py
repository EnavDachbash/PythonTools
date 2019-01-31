import os
import sys
import hvac


def get_token():
    try:
        f = open ('/Users/{0}/.vault-token'.format(os.environ['USER']))
        token = f.read().strip()
        # check here >> print (token)
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise
    finally:
        f.close()
        return token


# Initialize the client using TLS
client = hvac.Client(url='https://vault.dal.myhrtg.net:8200', token=get_token())

# set the secret to read
path2secret = input('Please etner the secret to read, omit the secret/ prefix: ')

# Read the secret:
print(client.read(path2secret))