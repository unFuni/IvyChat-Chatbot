from messaging import packet
from messaging.packet_id import PacketId

import socket
import io

class Client:
    def __init__(self, server, address, connection):
        self.server = server
        self.address = address
        self.connection = connection

        self.connected = True

        self.username = ""

    def send_packet(self, pkt : packet.Packet):
        if self.connected == False:
            return

        try:
            data = pkt.to_bytes()
            socket.socket.send(self.connection, data)
        except Exception as e:
            print(e)
            self.close()

    def handle(self):
        if self.connected == False:
            return
        
        try:
            data = socket.socket.recv(self.connection, 1028)
        except Exception as e:
            print(e)
            self.close()
            return
        
        total_size = len(data)

        if total_size < 8 or total_size >= 1028:
            return
        
        buffer = io.BytesIO(data)

        size = int.from_bytes(buffer.read(4), 'little')
        id = int.from_bytes(buffer.read(4), 'little')
        
        pkt = None

        match PacketId(id):
            case PacketId.PING: pkt = packet.PingPacket()
            case PacketId.PONG: pkt = packet.PongPacket()
            case PacketId.CONNECT: pkt = packet.ConnectPacket()
            case PacketId.SEND_MESSAGE: pkt = packet.SendMessagePacket()

        if pkt == None:
            return
        
        pkt.read_packet(buffer.read(size))
        self.__handle_incoming_packet(pkt)
        
    def __handle_incoming_packet(self, pkt):
        match pkt.id:
            case PacketId.PING: 
                send = packet.PongPacket()
                send.write_packet(pkt.ping) # do it properly later
                self.send_packet(send)
                pass

            case PacketId.PONG: 
                send = packet.PingPacket()
                send.write_packet(pkt.pong) # do it properly later
                self.send_packet(send)
                pass

            case PacketId.CONNECT:
                self.username = pkt.username 
                self.server.add_client(self)
                pass

            case PacketId.SEND_MESSAGE:
                self.__handle_recv_input(pkt.message)
                pass

    def __handle_recv_input(self, message : str):

        if not message:
            self.__send_recv_packet("Please provide a proper input...")
            return

        messages = message.split()
        
        command = messages[0]

        match command.lower():
            case "help":
                self.__send_recv_packet("""
                <help>
                <hello>
                <math> <a...z>
                """)
                pass
            case "hello":
                self.__send_recv_packet(f"Hi, {self.username}")
                pass
            case "math":
                variables = messages[1:]

                total = 0

                for variable in variables:
                    
                    print(variable)

                    number = 0
                    try:
                        number = float(variable)
                    except:
                        pass
                
                    total += number

                self.__send_recv_packet(f"Your number is {total}...")

    def __send_recv_packet(self, msg : str):
        to_send = packet.RecieveMessagePacket()
        to_send.write_packet(msg)

        self.send_packet(to_send)


    def disconnect(self):
        self.send_packet(packet.DisconnectPacket())
        
        print(f"USER: {self.username} has been disconnected...")

        self.close()

    def close(self):
        self.connected = False
        socket.socket.close(self.connection)