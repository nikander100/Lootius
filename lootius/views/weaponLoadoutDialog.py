#!/usr/bin/env python
import wx

"""
TODO Add min size for frame
"""
class WeaponLoadoutDialog(wx.Dialog):

    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.SetTitle("Lootius - " + "Weapon Loadout");
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline2, 0, wx.EXPAND, 5)

        """to be looked at"""
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddStretchSpacer()

        # cancel button
        self.btnCancel = wx.Button(self, wx.ID_ANY, "Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.on_close)
        btnSizer.Add(self.btnCancel, 0, wx.RIGHT, 2)

        # save button
        self.btnOK = wx.Button(self, wx.ID_ANY, "Save", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.btnOK, 0, wx.RIGHT, 5)

        mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        self.SetSizer(mainSizer)

    def on_close(self, event):
        self.Close()