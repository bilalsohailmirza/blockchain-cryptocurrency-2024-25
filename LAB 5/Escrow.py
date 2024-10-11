import socket
import multichain
class EscrowServer:
    def __init__(self, host='localhost', port=12346):
        self.host = host
        self.port = port
        self.balance = 0
        self.bob_approval = False
        self.alice_approval = False

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(2)
            print("Escrow server started and waiting for connections...")

            bob_conn, bob_addr = s.accept()
            print(f"Connected by Bob at {bob_addr}")

            alice_conn, alice_addr = s.accept()
            print(f"Connected by Alice at {alice_addr}")

            try:
                self.handle_bob(bob_conn)
                self.handle_alice(alice_conn)

                if self.bob_approval and self.alice_approval:
                    print(f"Releasing ${self.balance} to Alice.")
                    bob_conn.sendall(b"Transaction Complete: Funds released to Alice")
                else:
                    print("Transaction incomplete: Waiting for both approvals.")
            finally:
                bob_conn.close()
                alice_conn.close()

    def handle_bob(self, conn):
        data = conn.recv(1024)
        deposit_amount = int(data.decode('utf-8'))
        self.balance += deposit_amount
        print(f"Bob deposited: ${deposit_amount}")
        conn.sendall(b"Deposit successful")

        data = conn.recv(1024)
        if data.decode('utf-8') == 'Confirm Receipt':
            self.bob_approval = True
            print("Bob has confirmed receipt.")

    def handle_alice(self, conn):
        data = conn.recv(1024)
        if data.decode('utf-8') == 'Confirm Delivery':
            self.alice_approval = True

            print("Alice has confirmed delivery.")

escrow = EscrowServer()
escrow.start_server()
