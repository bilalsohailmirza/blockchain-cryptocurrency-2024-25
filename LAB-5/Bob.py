# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 23:31:57 2024

@author: Administrator
"""

import socket

class BobClient:
    def __init__(self, host='localhost', port=12346):
        self.host = host
        self.port = port
        self.balance = 500  # Bob's initial balance

    def connect_to_escrow(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            # Step 1: Deposit money into escrow
            deposit_amount = 100
            print(f"Bob deposits ${deposit_amount} into escrow")
            s.sendall(str(deposit_amount).encode('utf-8'))
            response = s.recv(1024)
            print(response.decode('utf-8'))

            # Step 2: Confirm receipt of goods/services
            input("Press Enter once Bob receives the goods/services...")
            s.sendall(b"Confirm Receipt")
            response = s.recv(1024)
            print(response.decode('utf-8'))

# Bob initiates the transaction
bob = BobClient()
bob.connect_to_escrow()