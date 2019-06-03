#import numpy as np
import struct,socket,select
from BaseServ import BaseServ
from PicProcess import PicProcess
import LoginCheckor
import socket
import sys
#import Queue

class OpencvServer:
    def __init__(self):
        self.__host = socket.gethostname()
        self.__port = 8001
        self.__inputs = []
        #self.__outputs = []
        self.__addr = (self.__host, self.__port)
        
    def __conn(self):
        print 'running'
        ss = socket.socket()
        ss.bind(self.__addr)
        ss.listen(10)
        print 'listenning'
        return ss 

    def __new_coming(self,ss):
        client,add = ss.accept()
        print 'welcome %s %s' % (client, add)
        wel = '''new client into opencv cloud server'''
        self.__inputs.append(client)
        return client

    def WorkLoop(self):
        ss = self.__conn() 
        self.__inputs.append(ss) 
        while True:
            try:
                r,w,e=select.select(self.__inputs,[],[])
                for temp in r: 
                    if temp is ss:
                        cursocket = self.__new_coming(ss)
                        checker = LoginCheckor.LoginCheckor(cursocket)
                        userid = checker.CheckThisUser()
                    else:
                        trans = BaseServ(cursocket)
                        num, orgpath = trans.ReceivePic()
                        picprocess = PicProcess(num,orgpath,userid)
                        path = picprocess.ChooseFuc()
                        trans.SendPic(path)
            except socket.error:
                self.__inputs.remove(temp)
                cursocket.close()
if __name__=='__main__':
    server = OpencvServer()
    server.WorkLoop()


