from __future__ import division
import socket
import threading
import time
import traceback
import wpf
import struct
import os
import stat
import clr

from Microsoft import Win32
from System.Windows import Window,Interop
from System.Windows import Int32Rect
from System import Uri
from System.Windows.Media.Imaging import*
from System.Windows.Media import *
from System import *
from System.ComponentModel import *
from System.Collections.Generic import List
from System.Collections.Generic import IList
from System.IO import Path,FileStream,FileMode
from ctypes import *


clr.AddReference("System.Drawing")
clr.AddReference('WindowsBase')
clr.AddReference('System.Windows.Presentation')
#from Window1 import Window1
from System.Drawing.Imaging import *
from System.Drawing import *
from System.Windows.Threading import Dispatcher
from System.Windows.Threading import DispatcherExtensions
dispatcher = Dispatcher.CurrentDispatcher
from System.Windows import Application, Window

class CameraCap(Window):
    def __init__(self,ss):
        wpf.LoadComponent(self,'CameraDisplay.xaml')
        DLLDir = r"./Cameracapture_dll.dll"
        try :
          self.Cameracapturedll = CDLL(DLLDir) 
        except :
          DLLDir = r"..\..\CameracaptureDLL\Debug\CameraCapture.dll"
          self.Cameracapturedll = CDLL(DLLDir) 

        #DLLDir = r"C:\Users\Administrator\Desktop\xy2017\Day8\client-WPF\Cameracapture_dll.dll"
        ##DLLDir = cdll.LoadLibrary('Cameracapture_dll.dll')
        ##self.Addr=Addr
        self.ss=ss
        #try :
        #    self.Cameracapturedll = CDLL(DLLDir)
        #except :
        #    DLLDir =os.getcwd() + r"C:\Users\Administrator\Desktop\xy2017\Day8\client-WPF\Cameracapture_dll.dll"#os.getcwd() + r"\Debug\Cameracapture_dll.dll"
        #    self.Cameracapturedll = CDLL(DLLDir)
        self.Cameracapturedll.CreateNewCamera()
        self.width= self.Cameracapturedll.CameraWidth()
        self.height=self.Cameracapturedll.CameraHeight()
        self.total_bytes=(self.width*4)*(self.height)
        self.CameraDisplay.BeginInit()
        self.wbbmp = WriteableBitmap(self.width,self.height,96,96,PixelFormats.Bgr32,None)
        self.CameraDisplay.Source = self.wbbmp
        self.CameraDisplay.EndInit()
        self.Show()
        self._worker = BackgroundWorker()
        self._worker.DoWork += self.WorkLoop
        self._worker.RunWorkerCompleted+=self.CleanUp
        self._worker.WorkerSupportsCancellation=True
        self._worker.RunWorkerAsync()

    def WriteBmp(self):
        self.wbbmp.Lock()
        self.wbbmp.WritePixels(Int32Rect(0,0,self.width,self.height),self.buffer,self.total_bytes,self.wbbmp.BackBufferStride)
        #self.CameraDisplay.Source = self.wbbmp
        self.wbbmp.Unlock()

    def WorkLoop(self, sender, e):
        while not self._worker.CancellationPending:
            data=self.Cameracapturedll.GrabFrame()
            self.buffer=IntPtr(data)
            Dispatcher.BeginInvoke(dispatcher,Action(self.WriteBmp))    

    def CleanUp(self, sender, e):
        #ISOTIMEFORMAT='%Y-%m-%d %X'
        #print  time.strftime("%a%b%d%H:%M:%S%Y", time.localtime()) 
        #print  time.strftime("%a%b%d%H:%M:%S%Y", time.localtime()) 
        name=time.strftime("%a%b%d%H%M%S%Y",time.localtime())+"camera1.jpg"
        try:
            filestream= FileStream(name,FileMode.Create)
        except:
            filestream= FileStream(time.strftime("%a%b%d%H%M%S%Y", time.localtime())+"camera2.jpg",FileMode.Create)
        encoder=JpegBitmapEncoder()
        encoder.FlipHorizontal=True
        encoder.FlipVertical=True
        encoder.Frames.Add(BitmapFrame.Create(self.CameraDisplay.Source))
        encoder.Save(filestream)
        #Receive=receive_window(self.Addr,name)
        filestream.Close()
        self.Cameracapturedll.Release()
        self.ss.pathBlock.Text=name     
        self.ss.StartTransFile(name)
        self.Hide()
    
    def Cancle_Button_Click(self, sender, e):
        self._worker.CancelAsync()
    
    def Window_Close(self, sender, e):
        self._worker.CancelAsync()

 
if __name__ == '__main__':
    Application().Run(CameraCap())
