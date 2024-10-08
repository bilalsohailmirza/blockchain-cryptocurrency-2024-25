import socket
from MicropaymentContract import return_rule_item, return_mc
import json

class Client:
    def __init__(self, host='localhost', port=12141):
        self.host = host
        self.port = port
        self.mc = return_mc()

    def connect_to_micropayment(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            print("Client connected to Server")

            i = int(input('Press 1 for Longitude and Latitude, Press 2 for Location: '))
            
            if i == 1:
                data = 'Longitude and Latitude'
                s.sendall(data.encode())
            elif i == 2:
                data = 'Location'
                s.sendall(data.encode())
            else:
                print('Invalid parameter, try again')
                return

            response = s.recv(1024).decode()

            try:
                response_json = json.loads(response)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                return

            if 'error' in response_json:
                print(f"Error from server: {response_json['error']}")
            else:
                received_data = response_json.get("data")
                received_txid = response_json.get("txid")

                rule_item = return_rule_item()
                if rule_item['txid'] == received_txid:
                    print(f"Received Transaction ID: {received_txid}")
                    print("Transaction ID verified successfully with Multichain!")
                    print(f"Received Data: {received_data}")
                else:
                    print("Transaction ID verification failed!")

            s.close()

client = Client()
client.connect_to_micropayment()
