#!/usr/bin/env python
import wx

"""
TODO Add min size for frame
"""
class WeaponLoadoutDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, title=(f"{parent.title} - Add Weapon Loadout"), size=(390, 525), style=wx.CAPTION|wx.CLOSE_BOX)

        """Main frame in window."""
        weaponLoadout = wx.BoxSizer(wx.VERTICAL)

        """ Weapon select row"""
        weaponInput = wx.BoxSizer(wx.HORIZONTAL)
        weaponInputName = wx.StaticText(self, wx.ID_ANY, "Weapon:", style=wx.ALIGN_LEFT)
        self.weaponInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        weaponInput.Add(weaponInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        weaponInput.Add(self.weaponInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Amp select row"""
        ampInput = wx.BoxSizer(wx.HORIZONTAL)
        ampInputName = wx.StaticText(self, wx.ID_ANY, "Amplifier:", style=wx.ALIGN_LEFT)
        self.ampInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        ampInput.Add(ampInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        ampInput.Add(self.ampInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Absorber select row"""
        absorberInput = wx.BoxSizer(wx.HORIZONTAL)
        absorberInputName = wx.StaticText(self, wx.ID_ANY, "Absorber:", style=wx.ALIGN_LEFT)
        self.absorberInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        absorberInput.Add(absorberInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        absorberInput.Add(self.absorberInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Scope loadout select row"""
        scopeLoadout = wx.BoxSizer(wx.VERTICAL)

        # Scope select row
        scopeInput = wx.BoxSizer(wx.HORIZONTAL)
        scopeInputName = wx.StaticText(self, wx.ID_ANY, "Scope:", style=wx.ALIGN_LEFT)
        self.scopeInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        scopeInput.Add(scopeInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        scopeInput.Add(self.scopeInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        # ScopeSight select row
        scopeSightInput = wx.BoxSizer(wx.HORIZONTAL)
        scopeSightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.scopeSightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        scopeSightInput.Add(scopeSightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT, 10)
        scopeSightInput.Add(self.scopeSightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        scopeLoadout.Add(scopeInput, 0, wx.BOTTOM|wx.EXPAND, 1)
        scopeLoadout.Add(scopeSightInput, 0, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)

        """ Sight select row"""
        sightInput = wx.BoxSizer(wx.HORIZONTAL)
        sightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.sightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        sightInput.Add(sightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        sightInput.Add(self.sightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Socket loadout select row"""
        socketLoadout = wx.BoxSizer(wx.VERTICAL)
        socketLoadoutSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Enahncers:"), wx.HORIZONTAL)
        socketLoadout.Add(socketLoadoutSizer, 1, wx.EXPAND, 0)

        # Socket 1 to 5 [section left]
        socketOnetoFive = wx.BoxSizer(wx.VERTICAL)

        socketOne = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 1"), wx.HORIZONTAL)
        self.socketOneInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketOneAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketOne.Add(self.socketOneInputBox, 1, 0, 0)
        socketOne.Add(self.socketOneAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketOne, 0, wx.EXPAND, 0)

        socketTwo = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 2"), wx.HORIZONTAL)
        self.socketTwoInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketTwoAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketTwo.Add(self.socketTwoInputBox, 1, 0, 0)
        socketTwo.Add(self.socketTwoAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketTwo, 0, wx.EXPAND, 0)

        socketThree = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 3"), wx.HORIZONTAL)
        self.socketThreeInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketThreeAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketThree.Add(self.socketThreeInputBox, 1, 0, 0)
        socketThree.Add(self.socketThreeAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketThree, 0, wx.EXPAND, 0)

        socketFour = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 4"), wx.HORIZONTAL)
        self.socketFourInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketFourAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketFour.Add(self.socketFourInputBox, 1, 0, 0)
        socketFour.Add(self.socketFourAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketFour, 0, wx.EXPAND, 0)

        socketFive = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 5"), wx.HORIZONTAL)
        self.socketFiveInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketFiveAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketFive.Add(self.socketFiveInputBox, 1, 0, 0)
        socketFive.Add(self.socketFiveAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketFive, 0, wx.EXPAND, 0)

        socketLoadoutSizer.Add(socketOnetoFive, 1, wx.LEFT|wx.RIGHT, 5)

        # Socket 6 to 10 [section right]
        socketSixtoTen = wx.BoxSizer(wx.VERTICAL)

        socketSix = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 1"), wx.HORIZONTAL)
        self.socketSixInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketSixAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketSix.Add(self.socketSixInputBox, 1, 0, 0)
        socketSix.Add(self.socketSixAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketSix, 0, wx.EXPAND, 0)

        socketSeven = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 2"), wx.HORIZONTAL)
        self.socketSevenInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketSevenAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketSeven.Add(self.socketSevenInputBox, 1, 0, 0)
        socketSeven.Add(self.socketSevenAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketSeven, 0, wx.EXPAND, 0)

        socketEight = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 3"), wx.HORIZONTAL)
        self.socketEightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketEightAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketEight.Add(self.socketEightInputBox, 1, 0, 0)
        socketEight.Add(self.socketEightAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketEight, 0, wx.EXPAND, 0)

        socketNine = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 4"), wx.HORIZONTAL)
        self.socketNineInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketNineAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketNine.Add(self.socketNineInputBox, 1, 0, 0)
        socketNine.Add(self.socketNineAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketNine, 0, wx.EXPAND, 0)

        socketTen = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 5"), wx.HORIZONTAL)
        self.socketTenInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketTenAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketTen.Add(self.socketTenInputBox, 1, 0, 0)
        socketTen.Add(self.socketTenAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketTen, 0, wx.EXPAND, 0)

        socketLoadoutSizer.Add(socketSixtoTen, 1, wx.LEFT|wx.RIGHT, 5)

        """Button controls"""
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.buttonSave = wx.Button(self, wx.ID_SAVE, "Save")
        self.buttonSave.SetDefault()
        buttons.Add(self.buttonCancel, 1, wx.EXPAND, 0)
        buttons.Add(self.buttonSave, 1, wx.EXPAND, 0)

        """Main ui"""
        weaponLoadout.Add(weaponInput, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 10)
        weaponLoadout.Add(ampInput, 0, wx.BOTTOM|wx.EXPAND, 5)
        weaponLoadout.Add(absorberInput, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)
        weaponLoadout.Add(scopeLoadout, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)
        weaponLoadout.Add(sightInput, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)
        weaponLoadout.Add(socketLoadout, 0 ,wx.EXPAND, 0)
        weaponLoadout.Add(buttons, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(weaponLoadout)
        weaponLoadout.SetSizeHints(self)

        self.SetAffirmativeId(self.buttonSave.GetId())
        self.SetEscapeId(self.buttonCancel.GetId())

        self.Layout()