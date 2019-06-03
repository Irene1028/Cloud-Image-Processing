import struct,socket,select
import os
import math
import datetime

import stat
class PicTrans():
    def __init__(self,sok):
        self.path = ''
        self.ss = sok
    
    def Send(self,data):
        bytes = self.ss.send(data)
        return bytes
        

    def Recv(self):
        data = self.ss.recv(1024)
        return data

    def Pic_Trans(self,FilePath,num):
        try:
            if os.path.isfile(FilePath):
                fp = open(FilePath,'rb')
                FileState = os.stat(FilePath)
                fhead = struct.pack('64sii', os.path.basename(FilePath),FileState[stat.ST_SIZE],num)
                self.Send(fhead)
                PicData = fp.read()
                while PicData:
                    bytes = self.Send(PicData)
                    PicData = PicData[bytes:]
                fp.close()
        except:
            pass

    def Pic_Recv(self):
        datainfo = self.Recv()
        FileName,FileSize = struct.unpack('64si', datainfo)
        path = 'G:/Day9xy/clnt_pic/' + FileName.strip('\00')  
        fp = open(path,'wb')
        num1 = 0
        while True:
            if num1 < FileSize :
                data = self.ss.recv(min(1024, FileSize-num1))
                fp.write(data)
                num1 = num1 + len(data)
            else:
                break
        fp.close()
        return path