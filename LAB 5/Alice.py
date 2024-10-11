import socket
from EscrowContract import return_rule_item, return_mc

class AliceServer:
    def __init__(self, host='localhost', port=12346):
        self.host = host
        self.port = port
        self.mc = return_mc()

    def connect_to_escrow(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Alice connects to Bob
            s.connect((self.host, self.port))
            print("Connected to Bob")

            # Receive Bob's transaction ID
            data = s.recv(1024)
            bob_txid = data.decode()
            print(f"Received Bob's Transaction ID: {bob_txid}")

            # Fetch the rule item from the Multichain stream to verify Bob's txid
            rule_item = return_rule_item()
            print(f"Rule Item from stream: {rule_item}")

            # Verify Bob's transaction ID
            if bob_txid == rule_item['bob_txid']:
                print("Bob's transaction verified successfully!")

                # Alice waits until goods/services are delivered
                input("Press Enter once Alice has delivered the goods/services...")

                # Alice updates the stream with her approval
                rule_item['alice_approval'] = True
                alice_txid = self.mc.publish('escrow_rules_stream', 'key1', {'json': rule_item})
                rule_item['alice_txid'] = alice_txid
                print(f"Alice's Transaction ID: {alice_txid}")

                # Publish Alice's transaction ID to the stream
                self.mc.publish('escrow_rules_stream', 'key1', {'json': rule_item})

                # Send Alice's transaction ID to Bob
                s.sendall(alice_txid.encode())
            else:
                print("Transaction verification failed. Quitting.")

# Alice confirms the delivery of goods/services
alice = AliceServer()
alice.connect_to_escrow()
