import sys
sys.path.append('../') # Temporary, once in prodution, build each server / client directory with copy of messagings folder

import threading
import time

# third party lib
import dearpygui

# project import
import client
import messaging.packet as packet

IP_ADDRESS = "127.0.0.1"
PORT = 7776

USERNAME = "Guest"

cli = client.Client(IP_ADDRESS, PORT, 1028, 1028, 4)

def run_client():
    print("Waiting for connection to server...")
    
    while cli.connected == False:
        cli.connect()
        time.sleep(1) # wait 1 second til another attempt
        print(f"Trying to connect to server...")

    print(f"Succcessfully connected @[{IP_ADDRESS}:{PORT}]")

    while cli.connected: 
        cli.recieve()
        time.sleep(0.1)

def main():
    network_thread = threading.Thread(target=run_client)
    network_thread.start()
    
    while True:
        text = input("Send a message: ")

        msg_packet = packet.SendMessagePacket()
        msg_packet.write_packet("Guest", text)
        cli.send(msg_packet)

if __name__ == "__main__":
    main()