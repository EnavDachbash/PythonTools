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

# Read the secret:
print(client.read('secret/aws/main/KMS-terraform'))