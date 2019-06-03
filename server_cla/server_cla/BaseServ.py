import struct,socket,select
import datetime
import socket
import sys
import math
import stat
import os
import numpy as np
import cv2


class BaseServ:
    def __init__(self,socket):
        self.currentsocket = socket
        self.FilePath = ''
    def RecvData(self):
        psw = self.currentsocket.recv(1024) 
        return psw

    def SendData(self,data):
        bytes = self.currentsocket.send(data)
        return bytes

    def ReceivePic(self):
        datainfo = self.RecvData()
        print datainfo
        FileName,FileSize,num = struct.unpack('64sii', datainfo)
        self.FilePath = FileName.strip('\00')
        self.FilePath = 'G:/Day9xy/clnt_pic/' + self.FilePath
        fp = open( os.path.abspath(self.FilePath) ,'wb')
        num1 = 0
        while True:
            if num1 < FileSize :
                data = self.currentsocket.recv(min(1024, FileSize-num1))
                fp.write(data)
                num1 = num1 + len(data)
            else:
                break
        fp.close()
        print 'Pic has been recieved and saved' 
        return num,self.FilePath

    def SendPic(self,path):
        try:
            if os.path.isfile(path):
                fp = open(path,'rb')
                print os.path.basename(path)+'-----'
                FileState = os.stat(path)
                print FileState[stat.ST_SIZE]
                fhead = struct.pack('64si', os.path.basename(path),FileState[stat.ST_SIZE])
                self.SendData(fhead)
                PicData = fp.read()
                while PicData:
                    bytes = self.SendData(PicData)
                    PicData = PicData[bytes:]
                fp.close()
                print 'Pic has been sent'
        except:
            pass
