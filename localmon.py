#!/usr/bin/env python3
#localmon.py
#Author: Craig O Carroll
#Date: 31/10/2026
#ChatGPT was used to plan the program structure and set up our github link to linux ubuntu terminal. Code will be written by me 

import argparse

#Create an argument parser to handle command line options
parser = argparse.ArgumentParser()

#Add Argument for transmit mode -t (client)
parser.add_argument("-t", action="store_true", help="Run in transmit mode (client)")

#Add Argument for receive mode -r (server)
parser.add_argument("-r", action="store_true", help="Run in receive mode (server)")

args = parser.parse_args()
print(args)