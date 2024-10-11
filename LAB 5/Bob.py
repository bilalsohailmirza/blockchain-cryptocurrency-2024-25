import socket
from EscrowContract import return_rule_item, return_mc
import json

class BobClient:
    def __init__(self, host='localhost', port=12346):
        self.host = host
        self.port = port
        self.balance = 500  
        self.mc = return_mc()

    def connect_to_escrow(self):
        rule_item = return_rule_item()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.mc.subscribe('escrow_rules_stream')
            print(f"Rule Item before deposit: {rule_item}")

            deposit_amount = 100
            print(f"Bob deposits ${deposit_amount} into escrow")
            rule_item['balance'] += deposit_amount

            bob_txid = self.mc.publish('escrow_rules_stream', 'key1', {'json': rule_item})
            print(f"Published Bob's Transaction ID: {bob_txid}")

            updated_rule_item = return_rule_item()
            updated_rule_item['bob_txid'] = bob_txid
            print(f"Updated Rule Item after Bob's deposit: {updated_rule_item}")

            self.mc.publish('escrow_rules_stream', 'key1', {'json': updated_rule_item})

            with open('result.json', 'w') as json_file:
                json.dump(updated_rule_item, json_file, indent=4)
                print("Rule saved to 'result.json'.")

            s.bind((self.host, self.port))
            s.listen(1)
            print("Waiting for Alice to connect...")

            conn, addr = s.accept()
            with conn:
                print(f"Connected by Alice from {addr}")

                conn.sendall(bob_txid.encode())

                data = conn.recv(1024)
                alice_txid = data.decode()
                print(f"Received Alice's Transaction ID: {alice_txid}")

                updated_rule_item = return_rule_item()
                print(f"Updated Rule Item from stream: {updated_rule_item}")

                if alice_txid == updated_rule_item['alice_txid']:
                    print("Alice's transaction verified successfully!")
                    input("Press Enter to confirm that goods/services have been received...")

                    updated_rule_item['bob_approval'] = True
                    txid = self.mc.publish('escrow_rules_stream', 'key1', {'json': updated_rule_item})
                    print(f"Final Transaction ID after Bob's approval: {txid}")

                    with open('result.json', 'w') as json_file:
                        json.dump(updated_rule_item, json_file, indent=4)
                        print("Rule saved to 'result.json'.")
                else:
                    print("Transaction verification failed. Mismatched Transaction ID.")

bob = BobClient()
bob.connect_to_escrow()
