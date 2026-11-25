import argparse
import socket
import json
import subprocess
import sys
import struct


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

def recv_exact(sock, size):
    data = b""

    while len(data) < size:
        part = sock.recv(size - len(data))

        if not part:
            return None

        data += part

    return data

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

# Protocol header: 4-byte magic value, 1-byte message type and 4-byte payload length. Total header size is 9 bytes.

if args.r:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", args.p))
    server_socket.listen(1)
    print("Server listening on port", args.p)

    while True:
        connect_socket, address = server_socket.accept()
        print("Connection from", address)

        request_header = recv_exact(connect_socket, 9)

        if not request_header:
            print("Error: Failed to receive request header")
            connect_socket.close()
            continue
        print("Received request header:", request_header)

        magic, message_type, payload_length = struct.unpack("!4sBI", request_header)

        if magic == b"RMON" and message_type == 1 and payload_length == 0:
            print("Request header validated")  
        else:    
            print("Error: Invalid request header")
            connect_socket.close()
            continue

if args.t:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.ip, args.p))
    print("Connected to server")

    request_header = struct.pack("!4sBI", b"RMON", 1, 0)
    client_socket.sendall(request_header)

    