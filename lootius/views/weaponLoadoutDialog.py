#!/usr/bin/env python
import wx
import sqlalchemy 

from database import db
from models.databaseModel import Weapons, Sights, Scopes,  WeaponAmps, EnhancerTypes, EnhancerClass, WeaponTypes, WeaponAbsorbers, EnhancerTypeNames, EnhancerNames
Session = db.DB.getSession()

"""
TODO add data intereaction to business layer instead of straight into gui? still have to figure out how to do that though, also setup cascading for database, loadouts primerly.
"""
class WeaponLoadoutDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, title=(f"{parent.title} - Add Weapon Loadout"), style=wx.CAPTION|wx.CLOSE_BOX)

        """Main frame in window."""
        weaponLoadout = wx.BoxSizer(wx.VERTICAL)
        
        """loadout name row"""
        weaponLoadoutName = wx.BoxSizer(wx.HORIZONTAL)
        weaponLoadoutNameText = wx.StaticText(self, wx.ID_ANY, "Name:", style=wx.ALIGN_LEFT)
        self.weaponLoadoutNameInput = wx.TextCtrl(self, wx.ID_ANY, "")
        weaponLoadoutName.Add(weaponLoadoutNameText, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        weaponLoadoutName.Add(self.weaponLoadoutNameInput, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Weapon select row"""
        weaponInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            weaponQuery = session.query(Weapons).all()

        weaponInputName = wx.StaticText(self, wx.ID_ANY, "Weapon:", style=wx.ALIGN_LEFT)
        self.weaponInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.weaponInputBox.SetItems([weapon.name for weapon in weaponQuery])
        weaponInput.Add(weaponInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        weaponInput.Add(self.weaponInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Amp select row"""
        ampInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            ampQuery = session.query(WeaponAmps)

        ampInputName = wx.StaticText(self, wx.ID_ANY, "Amplifier:", style=wx.ALIGN_LEFT)
        self.ampInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.ampInputBox.SetItems([amp.name for amp in ampQuery])
        ampInput.Add(ampInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        ampInput.Add(self.ampInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Absorber select row"""
        absorberInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            absQuery = session.query(WeaponAbsorbers)
        
        absorberInputName = wx.StaticText(self, wx.ID_ANY, "Absorber:", style=wx.ALIGN_LEFT)
        self.absorberInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.absorberInputBox.SetItems([abs.name for abs in absQuery])
        absorberInput.Add(absorberInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        absorberInput.Add(self.absorberInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Scope loadout select row"""
        scopeLoadout = wx.BoxSizer(wx.VERTICAL)

        # Scope select row
        scopeInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            scopeQuery = session.query(Scopes)

        scopeInputName = wx.StaticText(self, wx.ID_ANY, "Scope:", style=wx.ALIGN_LEFT)
        self.scopeInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.scopeInputBox.SetItems([scope.name for scope in scopeQuery])
        scopeInput.Add(scopeInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        scopeInput.Add(self.scopeInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        # ScopeSight select row
        scopeSightInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            sightQuery = session.query(Sights)

        scopeSightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.scopeSightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.scopeSightInputBox.SetItems([sight.name for sight in sightQuery])
        scopeSightInput.Add(scopeSightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT, 10)
        scopeSightInput.Add(self.scopeSightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        scopeLoadout.Add(scopeInput, 0, wx.BOTTOM|wx.EXPAND, 1)
        scopeLoadout.Add(scopeSightInput, 0, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)

        """ Sight select row"""
        sightInput = wx.BoxSizer(wx.HORIZONTAL)
        sightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.sightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.sightInputBox.SetItems([sight.name for sight in sightQuery])
        sightInput.Add(sightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        sightInput.Add(self.sightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Socket loadout select row"""
        socketLoadout = wx.BoxSizer(wx.VERTICAL)
        socketLoadoutSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Enahncers:"), wx.HORIZONTAL)
        socketLoadout.Add(socketLoadoutSizer, 1, wx.EXPAND, 0)

        # Socket 1 to 5 [section left]
        socketOnetoFive = wx.BoxSizer(wx.VERTICAL)

        with Session() as session:
            enahncerQuery = session.query(EnhancerClass).join(EnhancerNames).join(EnhancerTypeNames)
            enhancherValues = [f"{enhancer.enhancerNameID} {enhancer.enhancerTypeNameID}" for enhancer in enahncerQuery]

        socketOne = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 1"), wx.HORIZONTAL)
        self.socketOneInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketOneInputBox.SetItems(enhancherValues)
        self.socketOneAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketOne.Add(self.socketOneInputBox, 1, 0, 0)
        socketOne.Add(self.socketOneAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketOne, 0, wx.EXPAND, 0)

        socketTwo = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 2"), wx.HORIZONTAL)
        self.socketTwoInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketTwoInputBox.SetItems(enhancherValues)
        self.socketTwoAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketTwo.Add(self.socketTwoInputBox, 1, 0, 0)
        socketTwo.Add(self.socketTwoAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketTwo, 0, wx.EXPAND, 0)

        socketThree = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 3"), wx.HORIZONTAL)
        self.socketThreeInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketThreeInputBox.SetItems(enhancherValues)
        self.socketThreeAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketThree.Add(self.socketThreeInputBox, 1, 0, 0)
        socketThree.Add(self.socketThreeAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketThree, 0, wx.EXPAND, 0)

        socketFour = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 4"), wx.HORIZONTAL)
        self.socketFourInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketFourInputBox.SetItems(enhancherValues)
        self.socketFourAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketFour.Add(self.socketFourInputBox, 1, 0, 0)
        socketFour.Add(self.socketFourAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketFour, 0, wx.EXPAND, 0)

        socketFive = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 5"), wx.HORIZONTAL)
        self.socketFiveInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketFiveInputBox.SetItems(enhancherValues)
        self.socketFiveAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketFive.Add(self.socketFiveInputBox, 1, 0, 0)
        socketFive.Add(self.socketFiveAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketFive, 0, wx.EXPAND, 0)

        socketLoadoutSizer.Add(socketOnetoFive, 1, wx.LEFT|wx.RIGHT, 5)

        # Socket 6 to 10 [section right]
        socketSixtoTen = wx.BoxSizer(wx.VERTICAL)

        socketSix = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 6"), wx.HORIZONTAL)
        self.socketSixInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketSixInputBox.SetItems(enhancherValues)
        self.socketSixAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketSix.Add(self.socketSixInputBox, 1, 0, 0)
        socketSix.Add(self.socketSixAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketSix, 0, wx.EXPAND, 0)

        socketSeven = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 7"), wx.HORIZONTAL)
        self.socketSevenInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketSevenInputBox.SetItems(enhancherValues)
        self.socketSevenAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketSeven.Add(self.socketSevenInputBox, 1, 0, 0)
        socketSeven.Add(self.socketSevenAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketSeven, 0, wx.EXPAND, 0)

        socketEight = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 8"), wx.HORIZONTAL)
        self.socketEightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketEightInputBox.SetItems(enhancherValues)
        self.socketEightAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketEight.Add(self.socketEightInputBox, 1, 0, 0)
        socketEight.Add(self.socketEightAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketEight, 0, wx.EXPAND, 0)

        socketNine = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 9"), wx.HORIZONTAL)
        self.socketNineInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketNineInputBox.SetItems(enhancherValues)
        self.socketNineAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        socketNine.Add(self.socketNineInputBox, 1, 0, 0)
        socketNine.Add(self.socketNineAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketNine, 0, wx.EXPAND, 0)

        socketTen = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 10"), wx.HORIZONTAL)
        self.socketTenInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketTenInputBox.SetItems(enhancherValues)
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
        weaponLoadout.Add(weaponLoadoutName, 0, wx.EXPAND|wx.TOP, 10)
        weaponLoadout.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND|wx.TOP, 5)
        weaponLoadout.Add(weaponInput, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)
        weaponLoadout.Add(ampInput, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)
        weaponLoadout.Add(absorberInput, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)
        weaponLoadout.Add(scopeLoadout, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)
        weaponLoadout.Add(sightInput, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)
        weaponLoadout.Add(socketLoadout, 0, wx.EXPAND, 0)
        weaponLoadout.Add(buttons, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(weaponLoadout)
        weaponLoadout.SetSizeHints(self)

        self.SetAffirmativeId(self.buttonSave.GetId())
        self.SetEscapeId(self.buttonCancel.GetId())

        self.Layout()

        self.weaponInputBox.Bind(wx.EVT_COMBOBOX, self.onWepChoice)

    def on_save(self, event):
            print("I SAVED")

    count = 0
    def onWepChoice(self, event):
            selected_display_value = event.GetString()
            self.count += 1
            print(selected_display_value, self.count)