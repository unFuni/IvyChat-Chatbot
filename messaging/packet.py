from messaging.packet_id import PacketId
from messaging.packet_opt_type import PacketType
import io

class Packet:

    def __init__(self, id: PacketId, type : PacketType):
        self.id = id
        self.stream = io.BytesIO()
        self.type = type

    def __write_int(self, val : int): # convert int to bytes, write len of int, move len of int
        self.stream.write(val.to_bytes(4, byteorder='little'))
        self.stream.seek(4)

    def __write_string(self, val : str): # convert str in bytes, write len of buff, write buff,
        data = val.encode('utf-8')

        self.__write_int(len(data))

        self.stream.write(data)

    def __read_string(self): # read the size in bytes of the string, read a string of size
        len = self.__read_int()
        val = self.stream.read(len).decode('utf-8')

        return val

    def __read_int(self): # Integer is 4 bytes, so read 4
        val = int.from_bytes(self.stream.read(4), byteorder='little')

        return val
    
    def __set_buffer(self, data : bytes):
        self.stream = io.BytesIO(data)

    def read_packet(self, data):
        self.__set_buffer(data)

    def write_packet(self):
        pass
        
    def to_bytes(self):
        data = io.BytesIO()
        
        packet_data = self.stream.getvalue()

        size = len(packet_data) + 4

        data.write(size.to_bytes(4, 'little'))

        data.write(self.id.value.__int__().to_bytes(4, 'little'))
        data.write(packet_data)

        return data.getvalue()

class PingPacket(Packet):
    def __init__(self):
        super().__init__(PacketId.PING, PacketType.BIDIRECTIONAL)
        self.ping = 0

    def read_packet(self, data):
        super().read_packet(data)
        self.ping = self._Packet__read_int()

    def write_packet(self, ping : int):
        super().write_packet()
        self.ping = ping
        self._Packet__write_int(ping)

class PongPacket(Packet):
    def __init__(self):
        super().__init__(PacketId.PONG, PacketType.BIDIRECTIONAL)
        self.pong = 0

    def read_packet(self, data):
        super().read_packet(data)
        self.pong = self._Packet__read_int()

    def write_packet(self, pong : int):
        super().write_packet()
        self.pong = pong
        self._Packet__write_int(pong)

class RecieveMessagePacket(Packet):
    def __init__(self):
        super().__init__(PacketId.RECIEVE_MESSAGE, PacketType.SERVER)

        self.message = ""

    def read_packet(self, data):
        super().read_packet(data)

        self.message = self._Packet__read_string()

    def write_packet(self, message):
        self._Packet__write_string(message)
        
class SendMessagePacket(Packet):
    def __init__(self):
        super().__init__(PacketId.SEND_MESSAGE, PacketType.CLIENT)
        self.message = ""

    def read_packet(self, data):
        super().read_packet(data)
        self.message = self._Packet__read_string()

    def write_packet(self, message : str):
        self.message = message
        self._Packet__write_string(message)

class ConnectPacket(Packet): 
    def __init__(self):
        super().__init__(PacketId.CONNECT, PacketType.CLIENT)
        self.username = ""

    def read_packet(self, data):
        super().read_packet(data)
        self.username = self._Packet__read_string()

    def write_packet(self, username):
        self.username = username
        self._Packet__write_string(username)

class DisconnectPacket(Packet):
    def __init__(self):
        super().__init__(PacketId.DISCONNECT, PacketType.SERVER)
        self.message = ""

    def read_packet(self, data):
        super().read_packet(data)
        self.message = self._Packet__read_string()
    
    def write_packet(self, message : str):
        self.message = message
        self._Packet__write_string(message)

class HelloPacket(Packet):
    def __init__(self):
        super().__init__(PacketId.HELLO, PacketType.SERVER)

        self.users = []
        
    def read_packet(self, data):
        super().read_packet(data)

        len = self._Packet__read_int()
        
        for i in range(len):
            self.users.append(self._Packet__read_string())

    def write_packet(self, users : list[str]):
        self.users = users

        self._Packet__write_int(len(self.users))

        for user in self.users:
            self._Packet__write_string(user)