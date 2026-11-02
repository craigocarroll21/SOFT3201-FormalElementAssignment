#!/usr/bin/env python3
#localmon.py
#Author: Craig O Carroll
#Date: 31/10/2026
#ChatGPT was used to plan the program structure and set up our github link to linux ubuntu terminal. ChatGPT was also used at difficult points to offer guidence with adding and removing parts of code. Code is written by me 

import argparse
import subprocess
import json
import sys

#Function to run a command
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)
    
    except FileNotFoundError:
        print("Error: Command not found")
        sys.exit(1)

    except PermissionError:
        print("Error: Permission denied")
        sys.exit(1)


#Function to get local computer hostname
def get_hostname():
    try:
        hostname = run_command(["hostname"]).strip()
        print("Hostname:", hostname)
        return hostname

    except subprocess.CalledProcessError as e:
        print(f"Error getting hostname: {e.returncode}")
        sys.exit(1)

#Function to parse network info
def parse_network_info(data):
    try:
        if data == "":
            print("Error: No Network info received")
            sys.exit(1)
        return json.loads(data)
    except json.JSONDecodeError:
        print("Error: Invalid JSON data")
        sys.exit(1)

#Function to display netowkr info
def display_network_info(interfaces, address_interfaces, route_interfaces):

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

    #Get IP address details for first network interface
    first_address_interface = address_interfaces[0]
    print(first_address_interface["addr_info"])

    #Get IP address details for second network interface
    second_address_interface = address_interfaces[1]
    print(second_address_interface["addr_info"])

    #Get routing details for first network interface route
    first_route_interface = route_interfaces[0]
    print(first_route_interface["dst"])
    print(first_route_interface["gateway"])

    #Get routing details for second network interface route
    second_route_interface = route_interfaces[1]
    print(second_route_interface["dst"])

#Create an argument parser to handle command line options
parser = argparse.ArgumentParser()

#Add Argument for transmit mode -t (client)
parser.add_argument("-t", action="store_true", help="Run in transmit mode (client)")

#Add Argument for receive mode -r (server)
parser.add_argument("-r", action="store_true", help="Run in receive mode (server)")
args = parser.parse_args()
print(args)

#Store network interface details (link)
try: 
    link_result = run_command(["ip", "-json", "link", "show"])
    print("Getting network interface details...")

except subprocess.CalledProcessError as e:
    print(f"Error getting network interfaces: {e.returncode}")
    sys.exit(1)

#Store IP address details (address)
try:
    address_result = run_command(["ip", "-json", "address", "show"])
    print("Getting IP address details...")

except subprocess.CalledProcessError as e:
    print(f"Error getting IP address details: {e.returncode}")
    sys.exit(1)

#Store network routing details (route)
try:
    route_result = run_command(["ip", "-json", "route", "show"])
    print("Getting network routing details...")

except subprocess.CalledProcessError as e:
    print(f"Error getting network routing details: {e.returncode}")
    sys.exit(1)

#Parse and display network information from JSON results
interfaces = parse_network_info(link_result)

address_interfaces = parse_network_info(address_result)

route_interfaces = parse_network_info(route_result)

#Display network information
display_network_info(interfaces, address_interfaces, route_interfaces)

#Get the local computer hostname
hostname = get_hostname()

#store collected network information in a dictionary
network_info = {}
network_info["hostname"] = hostname
network_info["interfaces"] = interfaces
network_info["addresses"] = address_interfaces
network_info["routes"] = route_interfaces

#Write the network information to a JSON file
with open("local_network.json", "w") as fout:
    json.dump(network_info, fout, indent=4)