# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 10:20:44 2024

@author: Anabia
"""

import json
import socket
from cryptography.fernet import Fernet
# Client configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
KEY = 'MFKGHIWoLZaQBQnl-kFx_--g_I3O8r1NYQjiEd-IbRE='

# Initialize the local ledger
ledger_file = "client_ledger.json"
try:
    with open(ledger_file, "r") as file:
        ledger = json.load(file)
except FileNotFoundError:
    ledger = []

# Function to update local ledger with the data received from the server
def update_local_ledger(updated_ledger):
    with open(ledger_file, "w") as file:
        json.dump(updated_ledger, file, indent=4)

# Send data to the server
def send_data(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        fernet = Fernet(KEY)
        encrypt_data = fernet.encrypt(data.encode('utf-8'))
        
        s.sendall(encrypt_data)
        response = s.recv(1024).decode('utf-8')
        if response:
            updated_ledger = json.loads(response)
            update_local_ledger(updated_ledger)
            print(f"Updated ledger received from server: {updated_ledger}")

# Example usage
data = "hello"
send_data(data)
