# SOFT3201-FormalElementAssignment
Programming for Networked Systems - TU716

# Part 1 - Local Network Monitoring
This project is a python based network monitoring application. It collects local network info using commands in linux and saves the resukts in JSON format.

Commands used:
    - ip -json link show
    - ip -json address show
    - ip -json route show
    - hostname

The program saves the collected information to a file called loca_network.json.

This JSON file contains:
    - Hostname
    - Network interfaces
    - IP addresses
    - Routes

Run the program from a linux terminal using:

    python3 localmon.py