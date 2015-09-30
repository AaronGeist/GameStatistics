__author__ = 'yzhou7'

import wx

from src.DAL.DailyDataDAL import DailyDataDAL
from src.UI.UserData import UserGridData
from src.Util.TimeUtil import TimeUtil


# this class provides entry point for all clients
# it should have the following functions:
# 1. view all buyers's data
# 2. query single buyer'data
# 3. clean up out-of-data data

class BuyerPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("white")
        self.initUI()
        self.Show(True)

    def initUI(self):
        self.vBox = wx.BoxSizer(wx.VERTICAL)

        self.setupDateInput()
        self.displayTodayData()

        self.SetSizer(self.vBox)
        self.vBox.Layout()

    def setupDateInput(self):

        sizer = wx.GridBagSizer(4, 4)
        dateText = wx.StaticText(self, label='日期')
        sizer.Add(dateText, pos=(0, 0), flag=wx.EXPAND | wx.TOP | wx.LEFT, border=15)

        self.dateInput = wx.TextCtrl(self, value=TimeUtil.getToday(), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.onSearchDate, self.dateInput)
        sizer.Add(self.dateInput, pos=(0, 1),
                  flag=wx.TOP | wx.LEFT, border=12)

        self.calculateButton = wx.Button(self, label='计算一天战况', size=(100, 30))
        sizer.Add(self.calculateButton, pos=(0, 2), flag=wx.EXPAND | wx.TOP | wx.LEFT, border=12)
        self.calculateButton.Enable(True)
        self.Bind(wx.EVT_TEXT, self.OnEnter, self.dateInput)
        self.Bind(wx.EVT_BUTTON, self.onSearchDate, self.calculateButton)

        self.warnMsg = wx.StaticText(self, label='非法日期，请重新输入')
        self.warnMsg.SetForegroundColour('red')
        sizer.Add(self.warnMsg, pos=(0, 3), flag=wx.TOP | wx.LEFT, border=15)
        self.warnMsg.Hide()

        self.vBox.Add(sizer, wx.ALIGN_TOP, 10)

    def displayTodayData(self):
        sizer = wx.GridBagSizer(4, 4)
        today = TimeUtil.getToday()
        # Load buyer data
        dailyData = DailyDataDAL.fetchAllByDate(today)

        # set data into data grid
        self.data = UserGridData()
        self.data.InsertRows(dailyData.toStringList())
        self.grid = wx.grid.Grid(self, size=(500, 300))
        self.grid.SetTable(self.data)
        self.grid.AutoSize()
        sizer.Add(self.grid, pos=(1, 1), span=(3, 3), flag=wx.EXPAND | wx.TOP, border=5)

        searchText = wx.StaticText(self, label='名称')
        sizer.Add(searchText, pos=(4, 1), flag=wx.EXPAND, border=5)

        self.searchInput = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.onSearchName, self.searchInput)
        sizer.Add(self.searchInput, pos=(4, 2),
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)


        self.searchBtn = wx.Button(self, label='查找', size=(100, 20))
        sizer.Add(self.searchBtn, pos=(4, 3))
        self.searchBtn.Enable(True)
        self.Bind(wx.EVT_BUTTON, self.onSearchName, self.searchBtn)

        sizer.AddGrowableRow(1)
        self.vBox.Add(sizer, wx.ALIGN_BOTTOM, 10)

    def updateGrid(self, rows):
        self.grid.ClearGrid()
        self.data.InsertRows(rows)
        self.grid.SetTable(self.data)
        self.grid.AutoSize()
        self.vBox.Layout()

    def OnEnter(self, evt):
        if TimeUtil.isValidDate(self.dateInput.GetValue()):
            self.warnMsg.Hide()
            self.calculateButton.Enable(True)
        else:
            self.warnMsg.Show()
            # re-layout
            self.vBox.Layout()
            self.calculateButton.Enable(False)

    def onSearchName(self, evt):
        dailyData = DailyDataDAL.fetchByNameDate(self.dateInput.GetValue(), self.searchInput.GetValue())
        self.updateGrid(dailyData.toStringList())

    def onSearchDate(self, evt):
        dailyData = DailyDataDAL.fetchAllByDate(self.dateInput.GetValue())
        self.updateGrid(dailyData.toStringList())
