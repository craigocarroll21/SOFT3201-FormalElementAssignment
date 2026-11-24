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