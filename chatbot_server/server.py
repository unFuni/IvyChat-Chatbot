import client
import socket as skt
import threading

from messaging import packet

class Server:
    def __init__(self, max_connections):
        self.clients = dict()
        self.max_connections = max_connections
    
    def listen(self, ip_address, port):
        self.connection = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        skt.socket.bind(self.connection, (ip_address, port))
        skt.socket.listen(self.connection, self.max_connections + 1)

        print(f"Listening @{ip_address}:{port}")

    def handle(self): # Handle new connection, if valid, handle them as seperate client threads
        connection, address = skt.socket.accept(self.connection)

        cli = client.Client(self, address, connection)

        print(f"Binded client @{address}")

        thread = threading.Thread(target = self.__handle_client, args = (cli,))
        thread.start()

    def __handle_client(self, cli : client.Client):

        send = packet.HelloPacket()
        send.write_packet("") # Can send some sort of like message history and what not here if we want

        cli.send_packet(send)

        while(cli.connected):
            cli.handle()

    def add_client(self, cli : client.Client):
        self.clients[cli.address] = cli

        print(f"USER: {cli.username} has connected...")

    def get_client(self, address : str) -> client.Client:
        if address in self.clients:
            return self.clients[address]
        return None

    def close(self):
        for client in self.clients.values:
            client.disconnect()

        skt.socket.close(self.connection)