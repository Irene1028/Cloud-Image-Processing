import struct,socket,select,string
from BaseServ import BaseServ
import socket


class LoginCheckor(BaseServ):
    def __init__(self,socket):
        BaseServ.__init__(self,socket)
        self.currentsocket = socket

    def RecvData(self):
        return BaseServ.RecvData(self)

    def CheckThisUser(self):
        ab_client = self.RecvData()
        UserID = ab_client.split(':')[0]
        PSW = ab_client.split(':')[1]
        print 'the PSW is '+ PSW
        print 'the UserID is '+ UserID
        res = self.__LookUpList(UserID,PSW)
        if res is True:
            self.__SendResult('Y')
        else:
            self.__SendResult('N')
        return UserID

    def __LookUpList(self,UserID,PSW):
        ab = {
                'wang': '1111',
                'xu': '2222',
                'ran': '3333',
                'lulu': '4444'
        }
        if UserID in ab:
            print 'username is '+UserID+',userpsw should be '+ ab[UserID]
            if PSW == ab[UserID]:
                print 'Login Success!'
                return True
            else:
                print 'wrong psw'
                return False
        else:
            print 'invalid client'
            return False

    def __SendResult(self,Result):
        self.currentsocket.send(Result)
        print Result

if __name__ is '__main__':
    LoginCheckor = LoginCheckor()
