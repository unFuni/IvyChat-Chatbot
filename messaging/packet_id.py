import enum

class PacketId(enum.Enum):
    PING = 0
    PONG = 1

    #server operations
    RECIEVE_MESSAGE = 2
    HELLO = 3
    DISCONNECT = 4

    #client operations
    CONNECT = 5
    SEND_MESSAGE = 6