import enum

class PacketType(enum.Enum):
    CLIENT = 0
    SERVER = 1
    BIDIRECTIONAL = 2
