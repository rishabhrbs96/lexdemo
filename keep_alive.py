import socket
import sys
import os
import threading


class KeepAliveThread(threading.Thread):
    def run(self):
        HOST = os.environ.get("HOST", '0.0.0.0')
        PORT = os.environ.get("PORT", 5000)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print('Binding to %s: %d' % (HOST, PORT))
            s.bind((HOST, PORT))
        except socket.error as msg:
            sys.exit()

        print('Listening')
        s.listen(10)
        while 1:
            conn, addr = s.accept()
            print('Connected with ' + addr[0] + ':' + str(addr[1]))

        s.close()


ka = KeepAliveThread()
ka.run()
