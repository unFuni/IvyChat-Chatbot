import sys


sys.path.append('../') # Temporary, once in prodution, build each server / client directory with copy of messagings folder

import threading
import time

# third party lib
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

# project import
import messaging.packet as packet

import window
import globals

from messaging.packet_id import PacketId
import messaging.packet as packet

import queue

IP_ADDRESS = "127.0.0.1"
PORT = 7776

USERNAME = "Guest"

app = QApplication(sys.argv)
win = window.MainWindow()

def run_client():
    print("Waiting for connection to server...")
    
    globals.create_client(IP_ADDRESS, PORT, handle_incoming_packet)

    while globals.cli.connected == False:
        globals.cli.connect()
        time.sleep(1) # wait 1 second til another attempt
        print(f"Trying to connect to server...")

    print(f"Succcessfully connected @[{IP_ADDRESS}:{PORT}]")

    while globals.cli.connected: 
        globals.cli.recieve()
        time.sleep(0.1)

def handle_incoming_packet(pkt):
    match pkt.id:
        case PacketId.PING: 
            send = packet.PongPacket()
            send.write_packet(pkt.ping) # do it properly later
            globals.cli.send(send)
            pass

        case PacketId.PONG: 
            send = packet.PingPacket()
            send.write_packet(pkt.pong) # do it properly later
            globals.cli.send(send)
            pass

        case PacketId.HELLO:
            # handle user list

            print("Hello Recv")

            send = packet.ConnectPacket()
            send.write_packet(USERNAME) # do a proper name later
            globals.cli.send(send)
            pass

        case PacketId.RECIEVE_MESSAGE:
            print("Message Recv")
            globals.message_emitter.invoke(pkt.message)
            pass

        case PacketId.DISCONNECT:
            print("You've been disconnected from server...")
            globals.cli.__reconnect()
            pass

def message_recv(msg:str):
    win.chat_page.dialog.addOtherDialog(msg)

def main():
    network_thread = threading.Thread(target=run_client, daemon=True)
    network_thread.start()

    globals.create_message_recv_emitter()
    globals.message_emitter.message_recv_signal.connect(message_recv)

    win.show()

    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()