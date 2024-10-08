import socket
from MicropaymentContract import return_rule_item, return_mc
import json

class Server:
    def __init__(self, host='localhost', port=12141):
        self.host = host
        self.port = port
        self.mc = return_mc()

    def connect_to_micropayment(self):
        rule_item = return_rule_item()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Rule Item before deposit: {rule_item}")

            s.bind((self.host, self.port))
            s.listen(1)
            print("Waiting for Client to connect...")

            conn, addr = s.accept()
            with conn:
                print(f"Connected by Client from {addr}")
                
                data = conn.recv(1024)
                req = data.decode()
                print(f"Received request: {req}")

                response = {}
                if req == 'Longitude and Latitude':
                    if rule_item['balance'] >= 50:
                        rule_item['balance'] -= 50
                        rule_item['server_approval'] = True

                        txid = self.mc.publish('micropayment_stream', 'key1', {'json': rule_item})
                        rule_item['txid'] = txid
                        self.mc.publish('micropayment_stream', 'key1', {'json': rule_item})

                        response = {
                            "data": "24.8591:66.9983",
                            "txid": txid
                        }
                    else:
                        response = {
                            "error": "Insufficient tokens"
                        }
                elif req == 'Location':
                    if rule_item['balance'] >= 50:
                        rule_item['balance'] -= 50
                        rule_item['server_approval'] = True
                        txid = self.mc.publish('micropayment_stream', 'key1', {'json': rule_item})
                        rule_item['txid'] = txid
                        self.mc.publish('micropayment_stream', 'key1', {'json': rule_item})

                        response = {
                            "data": "FAST University",
                            "txid": txid
                        }
                    else:
                        response = {
                            "error": "Insufficient tokens"
                        }
                else:
                    response = {
                        "error": "Invalid request"
                    }

                conn.sendall(json.dumps(response).encode())

                updated_rule_item = return_rule_item()
                print(f"Updated Rule Item from stream: {updated_rule_item}")

                conn.close()

server = Server()
server.connect_to_micropayment()
