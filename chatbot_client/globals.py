from client import Client

from messageemitter import MessageEmitter

cli:Client = None

message_emitter:MessageEmitter = None

def create_message_recv_emitter():
    global message_emitter
    message_emitter = MessageEmitter()

def create_client(address, port, handler):
    global cli
    cli = Client(address, port, 1028, 1028, 4, handler)