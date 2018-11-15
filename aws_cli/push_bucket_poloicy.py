#!/usr/bin/env python

__author__ = 'Enav Hidekel'
__date__ = 'Nov 15, 2018'

"""
This script will
1. receive 1 account number
2. list all buckets
3. for each bucket >>
  3.1 change policy file
  3.2 update policy
"""

import boto3
import json
import re
from argparse import ArgumentParser

# Set up argument\s parsing:
parser = ArgumentParser(description=__doc__)
parser.add_argument('-a', '--account', help='Account(s) number to handle.'
                                            'Multiple accounts should be comma-delimited with NO SPACES')
args = parser.parse_args()

# Handle user input where no arguments passed:
if not getattr(args, 'account'):
    setattr(args, 'account', raw_input('Please enter account to handle: '))

# Handle multiple accounts input:
accounts = args.account.split(',')


def get_admin_role(a):
    """ This function would receive account number and list all of it's s3 buckets. """
    # Iterate over each account provided, and list buckets
    with open('/home/enav.hidekel/.aws/config', 'r') as current:
        prev_line = ""
        line_number = 1
        global role
        role = ""
        for line in current.readlines():
            if re.search(a, line):
                role = prev_line.split()[1][:-1]
            prev_line = line
            line_number += 1


def get_bucket_list(role):
    """ This function would receive admin role and start a new session. """
    # Creates new aws session (with admin role) and list buckets
    new_session = boto3.session.Session(profile_name=role)
    s3 = new_session.resource('s3')
    s3_client = new_session.client('s3')
    for bucket in s3.buckets.all():
        policy = edit_policy(bucket.name)
        s3_client.put_bucket_policy(Bucket=bucket.name, Policy=policy)


def edit_policy(bucket_name):
    """ This function will receive a bucket name and will edit the policy file accordingly.
     It will then enforce it. """
    bucket_policy = {
        "Version": "2012-10-17",
        "Id": "Policy1542271002809",
        "Statement": [
            {
                "Sid": "CrossAccountList",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::420262034214:role/admin"
                },
                "Action": "s3:ListBucket",
                "Resource": "arn:aws:s3:::%s" % bucket_name
            },
            {
                "Sid": "CrossAccountS3",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::420262034214:role/admin"
                },
                "Action": "s3:*",
                "Resource": "arn:aws:s3:::%s/*" % bucket_name
            }
        ]
    }

    # Convert the policy to a JSON string
    new_bucket_policy = json.dumps(bucket_policy)
    return new_bucket_policy


def main():

    for a in accounts:
        get_admin_role(a)
        print('{0} {1}'.format('The role to use is:', role))
        get_bucket_list(role)


if __name__ == '__main__':
    main()



#!/usr/bin/env python

__author__ = 'Enav Hidekel'
__date__ = 'Nov 15, 2018'

"""
This script will
1. receive 1 account number
2. list all buckets
3. for each bucket >>
  3.1 change policy file
  3.2 update policy
"""

import boto3
import json
import re
from argparse import ArgumentParser

# Set up argument\s parsing:
parser = ArgumentParser(description=__doc__)
parser.add_argument('-a', '--account', help='Account(s) number to handle.'
                                            'Multiple accounts should be comma-delimited with NO SPACES')
args = parser.parse_args()

# Handle user input where no arguments passed:
if not getattr(args, 'account'):
    setattr(args, 'account', raw_input('Please enter account to handle: '))

# Handle multiple accounts input:
accounts = args.account.split(',')


def get_admin_role(a):
    """ This function would receive account number and list all of it's s3 buckets. """
    # Iterate over each account provided, and list buckets
    with open('/home/enav.hidekel/.aws/config', 'r') as current:
        prev_line = ""
        line_number = 1
        global role
        role = ""
        for line in current.readlines():
            if re.search(a, line):
                role = prev_line.split()[1][:-1]
            prev_line = line
            line_number += 1


def update_all_buckets(role):
    """ This function would receive admin role and start a new session. """
    # Creates new aws session (with admin role) and list buckets
    new_session = boto3.session.Session(profile_name=role)
    s3 = new_session.resource('s3')
    s3_client = new_session.client('s3')
    for bucket in s3.buckets.all():
        print('{0} {1}'.format('Now Editing:', bucket.name))
        policy = edit_policy(bucket.name)
        s3_client.put_bucket_policy(Bucket=bucket.name, Policy=policy)


def edit_policy(bucket_name):
    """ This function will receive a bucket name and will edit the policy file accordingly.
     It will then enforce it. """
    bucket_policy = {
        "Version": "2012-10-17",
        "Id": "Policy1542271002809",
        "Statement": [
            {
                "Sid": "CrossAccountList",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::420262034214:role/admin"
                },
                "Action": "s3:ListBucket",
                "Resource": "arn:aws:s3:::%s" % bucket_name
            },
            {
                "Sid": "CrossAccountS3",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::420262034214:role/admin"
                },
                "Action": "s3:*",
                "Resource": "arn:aws:s3:::%s/*" % bucket_name
            }
        ]
    }

    # Convert the policy to a JSON string
    new_bucket_policy = json.dumps(bucket_policy)
    return new_bucket_policy


def main():

    for a in accounts:
        get_admin_role(a)
        update_all_buckets(role)


if __name__ == '__main__':
    main()



