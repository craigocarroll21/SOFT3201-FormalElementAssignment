import argparse
import socket
import json
import subprocess
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

#Create command line argument parser for client and server modes
parser = argparse.ArgumentParser()
mode = parser.add_mutually_exclusive_group()
mode.add_argument("-r", action="store_true", help="Run in server mode")
mode.add_argument("-t", action="store_true", help="Run in client mode")

parser.add_argument("-p", type=int, default=7777, help="PORT")
parser.add_argument("-ip", default="127.0.0.1", help="Server IP")

args = parser.parse_args()

if args.r == False and args.t == False:
    print("ERROR: Please choose either server mode (-r) or client mode (-t)")
    sys.exit(1)