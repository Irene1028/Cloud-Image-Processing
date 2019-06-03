from __future__ import division
from Window1 import Window1
import traceback
import wpf
import sys
import socket
import time
from Main_Client import MainClient
from System.Windows import Application, Window, MessageBox

class MyWindow(Window):
    def __init__(self): 
        wpf.LoadComponent(self, 'client_WPF.xaml')

    def Submit_Button_Click(self, sender, e):
        try:
            client = MainClient()
            client.UserID = self.InputuserID.Text
            client.PSW = self.Inputpassw.Password
            ss = client.conn()
            if client.result == 'Y':
                Choose = Window1(ss)
                Choose.ShowDialog()
                self.Hide()
        except Exception, e:
            tracelog = traceback.format_exc()
            MessageBox.Show(str(e))
        pass
    
    def InputuserID_TextChanged(self, sender, e):
        pass
       
if __name__ == '__main__':
    Application().Run(MyWindow())
    
    
    



