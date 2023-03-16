#!/usr/bin/env python
import wx

class PreferenceDialog(wx.Dialog):

    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.SetTitle("Lootius - " + "Preferences");
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        """wx.Toolbook is a left right settings tab patern compared to top down like this is.
        i find it personally better looking left right but have to figure out how to use it still."""
        self.listbook = wx.Listbook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT)

        self.listview = self.listbook.GetListView()

        self.imageList = wx.ImageList(32, 32)
        self.listbook.AssignImageList(self.imageList)

        mainSizer.Add(self.listbook, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 5)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline2, 0, wx.EXPAND, 5)

        """to be looked at"""
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddStretchSpacer()
        self.btnOK = wx.Button(self, wx.ID_ANY, "OK", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.btnOK, 0, wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.EXPAND, 5)
        self.SetSizer(mainSizer)