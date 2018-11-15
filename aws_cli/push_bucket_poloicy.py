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


def main():

    for a in accounts:
        get_admin_role(a)

    print(role)
#    s3 = boto3.resource('s3')


if __name__ == '__main__':
    main()



