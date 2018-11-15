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



