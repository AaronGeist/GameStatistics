from src.DAL.BuyerDAL import BuyerDAL
from src.UI.UserData import UserGridData
from src.Util.TimeUtil import TimeUtil

__author__ = 'yzhou7'

import wx
from src.SystemInitializer import SystemInitializer as init


# this class provides entry point for all clients
# it should have the following functions:
# 1. view all buyers's data
# 2. query single buyer'data
# 3. clean up out-of-data data

class MainWindow(wx.Frame):
    '''定义一个窗口类'''

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 800))
        self.panel = wx.Panel(self)
        self.warnMsg = wx.StaticText(self.panel, -1, label='Invalid Date', pos=(10, 30), size=(-1, -1))
        self.warnMsg.Hide()

        self.setupMenuBar()
        self.displayTodayData()
        self.setupDateInput()
        self.Show(True)

    def setupMenuBar(self):
        self.CreateStatusBar()

        menubar = wx.MenuBar()
        menufile = wx.Menu()

        mnuinit = menufile.Append(wx.ID_NEW, "New", "Create new profile")
        mnuabout = menufile.Append(wx.ID_ABOUT, '&About', 'about this shit')
        mnuexit = menufile.Append(wx.ID_EXIT, 'E&xit', 'end program')

        menubar.Append(menufile, '&File')

        # 事件绑定
        self.Bind(wx.EVT_MENU, self.onInit, mnuinit)
        self.Bind(wx.EVT_MENU, self.onAbout, mnuabout)
        self.Bind(wx.EVT_MENU, self.onExit, mnuexit)

        self.SetMenuBar(menubar)

    # TODO maybe we should have a limited number to display
    def displayTodayData(self):
        # Load buyer data
        buyerData = BuyerDAL.fetchAllByDate("20150901")

        rows = list()
        for data in buyerData:
            rows.extend(data.toStringList())

        # set data into data grid
        self.data = UserGridData()
        self.data.InsertRows(rows)
        self.grid = wx.grid.Grid(self.panel, -1, pos=(300, 300), size=(600, 600))
        self.grid.SetTable(self.data)

        btn = wx.Button(self, label="set a2 to x")
        btn.Bind(wx.EVT_BUTTON, self.OnTest)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.grid, 1, wx.EXPAND)
        self.Sizer.Add(btn, 0, wx.EXPAND)

    def setupDateInput(self):
        self.text = wx.TextCtrl(self.panel, -1, value=TimeUtil.getToday(), pos=(10, 10), size=(100, 20))
        self.button = wx.Button(self.panel, -1, label='Calculate Score', pos=(120, 10), size=(100, 20))
        self.button.Enable(True)
        self.Bind(wx.EVT_TEXT, self.OnEnter, self.text)

    def OnTest(self, event):
        self.data.set_value(1, 0, "x")
        self.grid.Refresh()

    def onInit(self, evt):
        dlg = wx.MessageDialog(self, 'Creating new profile', 'Init my app', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        init.initialize()

    def onAbout(self, evt):
        '''点击about的事件响应'''
        dlg = wx.MessageDialog(self, 'This app is a simple text editor', 'About my app', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def onExit(self, evt):
        '''点击退出'''
        self.Close(True)

    def OnEnter(self, evt):
        if TimeUtil.isValidDate(self.text.GetValue()):
            self.warnMsg.Hide()
            self.button.Enable(True)
        else:
            self.warnMsg.Show()
            self.button.Enable(False)
