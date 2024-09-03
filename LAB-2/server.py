# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 10:19:54 2024

@author: Anabia
"""

import json
import hashlib
import socket
from cryptography.fernet import Fernet

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on
KEY = 'MFKGHIWoLZaQBQnl-kFx_--g_I3O8r1NYQjiEd-IbRE='

# Initialize the ledger
ledger_file = "server_ledger.json"
try:
    with open(ledger_file, "r") as file:
        ledger = json.load(file)
except FileNotFoundError:
    ledger = []

# Function to update the ledger
def update_ledger(data):
    data = data.decode()
    key = hashlib.sha256(data.encode()).hexdigest()[:8]
    reverse_key = key[::-1]
    entry = {
        "key": key,
        "reverse_key": reverse_key,
        "data": data
    }
    ledger.append(entry)
    with open(ledger_file, "w") as file:
        json.dump(ledger, file, indent=4)
    return ledger

# Start the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024).decode('utf-8')
            if data:
                fernet = Fernet(KEY)
                decrypt_data = fernet.decrypt(data.encode('utf-8'))
                print(f"Received data: {decrypt_data.decode()}")
                updated_ledger = update_ledger(decrypt_data)
                conn.sendall(json.dumps(updated_ledger).encode('utf-8'))