import struct,socket,select,string
import cv2
import datetime
import numpy as np
class PicProcess:
    def __init__(self,num,orgpath,id):
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H-%M-%S-")
        self.path = 'G:/Day9xy/clnt_pic/' + otherStyleTime + id + '-' + str(num) +'-'+ orgpath.split('/')[-1]
        self.orgpath = orgpath
        self.img =cv2.imread(self.orgpath)
        self.img0 =cv2.imread(self.orgpath,0)
        self.dst = ''
        self.num = num

    def Savedst(self):
        cv2.imwrite(self.path,self.dst)

    def Eroded(self):
        kernel=np.uint8(np.zeros((5,5)))  
        for x in range(5):  
            kernel[x,2]=1
            kernel[2,x]=1
        self.dst=cv2.erode(self.img,kernel)
        self.Savedst()

    def Dilated(self):
        kernel=np.uint8(np.zeros((5,5)))  
        for x in range(5):  
            kernel[x,2]=1
            kernel[2,x]=1
        self.dst=cv2.dilate(self.img,kernel)
        self.Savedst()

    def Histogram(self) :
        self.dst= cv2.equalizeHist(self.img0)
        self.Savedst()

    def Canny(self):
        img1 = cv2.GaussianBlur(self.img,(3,3),0)  
        self.dst = cv2.Canny(img1, 50, 150)
        self.Savedst()

    def threshold(self):
        i,self.dst = cv2.threshold(self.img0,127,255,cv2.THRESH_BINARY)
        self.Savedst()


    def Gauss(self):
        self.dst = cv2.GaussianBlur(self.img,(5,5),1.5)
        self.Savedst()

    def edge_check(self):
        self.img = cv2.imread(self.orgpath,0)
        self.dst = cv2.Canny(self.img,100,200)
        self.Savedst()

    def Med_Blur(self):
        self.dst =  cv2.medianBlur(self.img,5)
        self.Savedst()
    def Blur(self):
        self.dst =  cv2.blur(self.img,(25,25))
        self.Savedst()

    def ChooseFuc(self):
        if self.num == 1:
            self.Eroded()
        elif self.num ==2:
            self.Dilated()
        elif self.num == 3:
            self.Blur()
        elif self.num ==4:
            self.Histogram()
        elif self.num ==5:
            self.Canny()
        elif self.num ==6:
            self.threshold()
   
        return self.path