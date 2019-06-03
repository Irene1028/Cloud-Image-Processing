import wpf,os
from PicTrans import PicTrans
from System import Uri,UriKind
from System.IO import Path,FileStream,FileAccess,FileAccess,FileMode,FileShare,SeekOrigin
from System.Windows.Media import *
from System.Windows.Media.Imaging import *
from Microsoft.Win32 import OpenFileDialog
from System.Windows import Application, Window, MessageBox
from CameraDisplay import CameraCap

class Window1(Window):
    def __init__(self,sok):
        wpf.LoadComponent(self, 'Window1.xaml')
        self.cursok = sok

    def Choose_Button_Click(self,sender, e):
        openFileDialog = OpenFileDialog()
        openFileDialog.Filter = "JPG|*.jpg"
        openFileDialog.ShowDialog()
        self.image1.Source = BitmapImage (Uri(openFileDialog.FileName))
        self.pathBlock.Text = openFileDialog.FileName

    def Camera_Button_Click(self,sender,e):
        camera = CameraCap(self)
        camera.Show()

    def StartTransFile(self,filename):
        print os.path.abspath(filename)
        self.image1.Source= BitmapImage(Uri(os.path.abspath(filename)))
        self.pathBlock.Text = os.path.abspath(filename)

    def Confirm_Button_Click(self,sender, e):
            number = 0
            if self.checkBox1.IsChecked == True:
                number = 1
            elif self.checkBox2.IsChecked == True:
                number = 2
            elif self.checkBox3.IsChecked == True:
                number = 3
            elif self.checkBox4.IsChecked == True:
                number = 4
            elif self.checkBox5.IsChecked == True:
                number = 5
            elif self.checkBox6.IsChecked == True:
                number = 6
            transp = PicTrans(self.cursok)
            transp.Pic_Trans(self.pathBlock.Text, number)
            path = transp.Pic_Recv()
            self.image2.Source = BitmapImage (Uri(path))



    