# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 23:32:27 2024

@author: Administrator
"""

import socket

class AliceServer:
    def __init__(self, host='localhost', port=12346):
        self.host = host
        self.port = port

    def connect_to_escrow(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            # Step 1: Confirm delivery of goods/services
            input("Press Enter once Alice has delivered the goods/services...")
            s.sendall(b"Confirm Delivery")
            response = s.recv(1024)
            print(response.decode('utf-8'))

# Alice confirms the delivery of goods/services
alice = AliceServer()
alice.connect_to_escrow()