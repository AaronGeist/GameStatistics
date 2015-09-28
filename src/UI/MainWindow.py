from src.DAL.BuyerDAL import BuyerDAL
from src.DAL.DailyDataDAL import DailyDataDAL
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
        super(MainWindow, self).__init__(parent, title=title, size=(800, 800))
        self.initUI()
        self.Show(True)

    def initUI(self):
        self.setupMenuBar()
        # menu bar should be drawn first
        # or sizer/layout will work wrongly
        self.setupPanel()

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

    def setupPanel(self):
        self.panel = wx.Panel(self)
        self.hbox = wx.BoxSizer(wx.VERTICAL)

        self.setupDateInput()
        self.displayTodayData()

        self.panel.SetSizer(self.hbox)

    def setupDateInput(self):

        sizer = wx.GridBagSizer(4, 4)
        dateText = wx.StaticText(self.panel, label='日期')
        sizer.Add(dateText, pos=(1, 1), flag=wx.EXPAND, border=5)

        self.dateInput = wx.TextCtrl(self.panel, value=TimeUtil.getToday())
        sizer.Add(self.dateInput, pos=(1, 2),
            flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)

        self.calculateButton = wx.Button(self.panel, label='计算得分', size=(100, 20))
        sizer.Add(self.calculateButton, pos=(1, 3), span=(1, 5))
        self.calculateButton.Enable(True)
        self.Bind(wx.EVT_TEXT, self.OnEnter, self.dateInput)
        self.Bind(wx.EVT_BUTTON, self.OnSearchDate, self.calculateButton)

        self.warnMsg = wx.StaticText(self.panel, label='非法日期，请重新输入')
        sizer.Add(self.warnMsg, pos=(2, 1), span=(2, 5), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        self.warnMsg.Hide()

        self.hbox.Add(sizer, wx.EXPAND | wx.ALL, 20)

        #
        #
        # buttonOk = wx.Button(self.panel, label="Ok", size=(90, 28))
        # buttonClose = wx.Button(self.panel, label="Close", size=(90, 28))
        # self.sizer.Add(buttonOk, pos=(3, 3))
        # self.sizer.Add(buttonClose, pos=(3, 4), flag=wx.RIGHT|wx.BOTTOM, border=5)
        #
        # self.sizer.AddGrowableCol(1)
        # self.sizer.AddGrowableRow(2)

        # # self.text = wx.TextCtrl(self.panel, -1, value=TimeUtil.getToday(), pos=(10, 10), size=(100, 20))
        # self.text = wx.TextCtrl(self.panel, -1, value=TimeUtil.getToday())
        # self.sizer.Add(self.text, pos=(0, 0), span=(1, 5), flag=wx.LEFT|wx.RIGHT)
        # # self.button = wx.Button(self.panel, -1, label='Calculate Score', pos=(120, 10), size=(100, 20))


    # TODO maybe we should have a limited number to display
    def displayTodayData(self):

        sizer = wx.GridBagSizer(4, 4)

        today = TimeUtil.getToday()
        today = "2015-09-01"
        # Load buyer data
        dailyData = DailyDataDAL.fetchAllByDate(today)

        # set data into data grid
        self.data = UserGridData()
        self.data.InsertRows(dailyData.toStringList())
        self.grid = wx.grid.Grid(self.panel)
        self.grid.SetTable(self.data)
        sizer.Add(self.grid, pos=(1, 1), span=(1, 3), flag=wx.EXPAND|wx.TOP, border=5)

        searchText = wx.StaticText(self.panel, label='名称')
        sizer.Add(searchText, pos=(2, 1), flag=wx.EXPAND, border=5)

        self.searchInput = wx.TextCtrl(self.panel)
        sizer.Add(self.searchInput, pos=(2, 2),
            flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)

        self.searchBtn = wx.Button(self.panel, label='查找', size=(100, 20))
        sizer.Add(self.searchBtn, pos=(2, 3))
        self.searchBtn.Enable(True)
        self.Bind(wx.EVT_BUTTON, self.OnSearchName, self.searchBtn)

        # sizer.AddGrowableRow(0)
        self.hbox.Add(sizer, wx.EXPAND | wx.ALL, 20)


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
        if TimeUtil.isValidDate(self.dateInput.GetValue()):
            self.warnMsg.Hide()
            self.calculateButton.Enable(True)
        else:
            self.warnMsg.Show()
            # re-layout
            self.hbox.Layout()
            self.calculateButton.Enable(False)

    def OnSearchName(self, evt):
        self.data.set_value(0, 0, "x")
        self.grid.Refresh()

    def OnSearchDate(self, evt):
        dailyData = DailyDataDAL.fetchAllByDate(self.dateInput.GetValue())

        # self.data.Clear()
        # self.data.InsertRows(dailyData.toStringList())
        # self.data.set_value(0, 0, "x")
        # self.grid.Refresh()

        self.data.UpdateTable(dailyData.toStringList())
        self.grid.Refresh()

