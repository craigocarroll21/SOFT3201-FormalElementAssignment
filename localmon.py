#!/usr/bin/env python3
#localmon.py
#Author: Craig O Carroll
#Date: 31/10/2026
#ChatGPT was used to plan the program structure and set up our github link to linux ubuntu terminal. Code will be written by me 

import argparse
import subprocess
import json
import sys

#Create an argument parser to handle command line options
parser = argparse.ArgumentParser()

#Add Argument for transmit mode -t (client)
parser.add_argument("-t", action="store_true", help="Run in transmit mode (client)")

#Add Argument for receive mode -r (server)
parser.add_argument("-r", action="store_true", help="Run in receive mode (server)")

args = parser.parse_args()
print(args)

#Get local computer hostname
hostname = subprocess.run(["hostname"], capture_output=True, text=True, check=True).stdout.strip()
print(hostname)

#Store network interface details (link)
link_result = subprocess.run(["ip", "-json", "link", "show"], capture_output=True, text=True, check=True)
print(link_result.stdout)

#Convert JSON output into a Python list
interfaces = json.loads(link_result.stdout)
print(interfaces)

#Get details for first network interface
first_interface = interfaces[0]
print(first_interface["ifname"])
print(first_interface["mtu"])
print(first_interface["address"])
print(first_interface["flags"])
print(first_interface["operstate"])

#Get details for second network interface
second_interface = interfaces[1]
print(second_interface["ifname"])
print(second_interface["mtu"])
print(second_interface["address"])
print(second_interface["flags"])
print(second_interface["operstate"])


#Store IP address details (address)
address_result = subprocess.run(["ip", "-json", "address", "show"], capture_output=True, text=True, check=True)
print(address_result.stdout)

#Convert JSON output into a Python list
address_interfaces = json.loads(address_result.stdout)
print(address_interfaces)

#Get IP address details for first network interface
first_address_interface = address_interfaces[0]
print(first_address_interface["addr_info"])

#Get IP address details for second network interface
second_address_interface = address_interfaces[1]
print(second_address_interface["addr_info"])

#Store network routing details (route)
route_result = subprocess.run(["ip", "-json", "route", "show"], capture_output=True, text=True)
print(route_result.stdout)

#Convert JSON output into a Python list
route_interfaces = json.loads(route_result.stdout)
print(route_interfaces)

#Get routing details for first network interface
first_route_interface = route_interfaces[0]
print(first_route_interface["dst"])
print(first_route_interface["gateway"])

#Get routing details for second network interface
second_route_interface = route_interfaces[1]
print(second_route_interface["dst"])

#store collected network information in a dictionary
network_info = {}
network_info["hostname"] = hostname
network_info["interfaces"] = interfaces
network_info["addresses"] = address_interfaces
network_info["routes"] = route_interfaces

#Write the network information to a JSON file
with open("local_network_info.json", "w") as fout:
    json.dump(network_info, fout, indent=4)