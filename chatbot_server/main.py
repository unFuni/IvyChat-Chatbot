import sys

# messaing_dir = os.path.abspath(os.path.join(os.getcwd(), "../messaging/"))
sys.path.append('../') # Temporary, once in prodution, build each server / client directory with copy of messagings folder

import time
import server

MAX_CONN = 64
IP_ADDRESS = "127.0.0.1"
PORT = 7776

svr = server.Server(MAX_CONN)

def main():
    svr.listen(IP_ADDRESS, PORT)
    
    while True:
        svr.handle()

        time.sleep(0.1) # try accepting new connection in 0.1 sec intervals

if __name__ == "__main__":
    main()