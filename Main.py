__author__ = 'yzhou7'

import wx
from src.UI.MainWindow import MainWindow

app = wx.App(False)
frame = MainWindow(None, 'ӯ��ͳ�� V1')
app.MainLoop()

# app = wx.App(False)
# app.TopWindow = UserData.UserDataWindow()
# app.TopWindow.Show()
# app.MainLoop()
