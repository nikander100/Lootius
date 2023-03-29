#!/usr/bin/env python
import wx

"""
TODO Add min size for frame
"""
class WeaponLoadoutDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, title=(f"{parent.title} - Add Weapon Loadout"), size=(390, 525), style=wx.CAPTION|wx.CLOSE_BOX)
        # self.SetBackgroundColour(wx.NullColour)

        # Main frame in window.
        weaponLoadout = wx.BoxSizer(wx.VERTICAL)

        # Weapon select row
        weaponInput = wx.BoxSizer(wx.HORIZONTAL)

        weaponInputName = wx.StaticText(self, wx.ID_ANY, "Weapon:", style=wx.ALIGN_LEFT)
        weaponInput.Add(weaponInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        self.weaponInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        weaponInput.Add(self.weaponInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)


        weaponLoadout.Add(weaponInput, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)