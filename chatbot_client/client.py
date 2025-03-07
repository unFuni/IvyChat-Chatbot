import socket as skt
import io
import time

import messaging.packet as packet
from messaging.packet_id import PacketId

class Client:
    def __init__(self, address, port, out_buffer_size, in_buffer_size, max_retry, packet_handler):
        self.ip_address = address
        self.port = port
        self.send_buffer_size = out_buffer_size
        self.recv_buffer_size = in_buffer_size
        self.max_retry = max_retry

        self.packet_handler = packet_handler

        self.connected = False

    def connect(self):
        try:
            self.connection = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
            skt.socket.connect(self.connection, (self.ip_address, self.port))

            self.connected = True

            return True
        except:
            return False

    def send(self, pkt : packet.Packet):
        if self.connected == False:
            return

        try:
            data = pkt.to_bytes()

            if len(data) >= self.send_buffer_size:
                print("Message exteeds maximum size...")
                return

            skt.socket.send(self.connection, data)
        except:
            if self.__reconnect():
                self.send(pkt) # Maybe don't send the message again?

    def recieve(self):
        if self.connected == False:
            return
        
        try:
            data = skt.socket.recv(self.connection, 1028)
        except:
            return
        
        total_size = len(data)

        if total_size < 8 or total_size >= self.recv_buffer_size:
            return

        buffer = io.BytesIO(data)

        size = int.from_bytes(buffer.read(4), 'little')
        id = int.from_bytes(buffer.read(4), 'little')
        
        pkt = None

        match PacketId(id):
            case PacketId.PING: pkt = packet.PingPacket()
            case PacketId.PONG: pkt = packet.PongPacket()

            case PacketId.RECIEVE_MESSAGE: pkt = packet.RecieveMessagePacket()
            case PacketId.HELLO: pkt = packet.HelloPacket()

            case PacketId.SEND_MESSAGE: pkt = packet.SendMessagePacket()

        if pkt == None:
            return
        
        pkt.read_packet(buffer.read(size))
        self.packet_handler(pkt)        
    
    def __reconnect(self):
        num_retries = 0
        
        while num_retries < self.max_retry and self.connect() == False:
            print("Reconnecting...")
            num_retries += 1
            time.sleep(1) # wait 1 second til retry

        if num_retries >= self.max_retry and self.connected == False:
            print(f"RECONNECT OPT FAILURE: Max number of reconnections made [{self.max_retry}]")

        return self.connected