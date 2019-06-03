import struct,socket,select
from Window1 import Window1
import socket
import time
import sys
class MainClient:
    def __init__(self):
        self.__host = socket.gethostname()
        self.__port = 8001
        self.UserID = ""
        self.PSW = ""
        self.result = ""
        #self.__addr = (self.__host, self.__port)
    def conn(self):
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.connect((self.__host , 8001))
        time.sleep(2)
        ss.send(self.UserID + ':'+ self.PSW)
        self.result = ss.recv(1024)
        return ss
    

