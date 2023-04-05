#!/usr/bin/env python
import wx
import sqlalchemy 
from sqlalchemy.orm import joinedload
import time

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
            self.weaponValue = list(map(lambda weapon: weapon.name, weaponQuery))

        weaponInputName = wx.StaticText(self, wx.ID_ANY, "Weapon:", style=wx.ALIGN_LEFT)
        self.weaponInputBox = wx.ComboBox(self, wx.ID_ANY, value="Select..", choices=[""], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.weaponInputBox.AppendItems(self.weaponValue)
        weaponInput.Add(weaponInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        weaponInput.Add(self.weaponInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Amp select row"""
        ampInput = wx.BoxSizer(wx.HORIZONTAL)
        ampInputName = wx.StaticText(self, wx.ID_ANY, "Amplifier:", style=wx.ALIGN_LEFT)
        self.ampInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[""], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        ampInput.Add(ampInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        ampInput.Add(self.ampInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.ampInputBox.Enable(False)

        """ Absorber select row"""
        absorberInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            absQuery = session.query(WeaponAbsorbers).filter(WeaponAbsorbers.weaponTypeID == 1)
            self.absValue = list(map(lambda abs: abs.name, absQuery))
        
        absorberInputName = wx.StaticText(self, wx.ID_ANY, "Absorber:", style=wx.ALIGN_LEFT)
        self.absorberInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[""], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.absorberInputBox.AppendItems(self.absValue)
        absorberInput.Add(absorberInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        absorberInput.Add(self.absorberInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.absorberInputBox.Enable(False)

        """ Scope loadout select row"""
        scopeLoadout = wx.BoxSizer(wx.VERTICAL)

        # Scope select row
        scopeInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            scopeQuery = session.query(Scopes)
            self.scopeValue = list(map(lambda scope: scope.name, scopeQuery))

        scopeInputName = wx.StaticText(self, wx.ID_ANY, "Scope:", style=wx.ALIGN_LEFT)
        self.scopeInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[""], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.scopeInputBox.AppendItems(self.scopeValue)
        scopeInput.Add(scopeInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        scopeInput.Add(self.scopeInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.scopeInputBox.Enable(False)

        # ScopeSight select row
        scopeSightInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            sightQuery = session.query(Sights)
            self.sightValue = list(map(lambda sight: sight.name, sightQuery))

        scopeSightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.scopeSightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[""], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.scopeSightInputBox.AppendItems(self.sightValue)
        scopeSightInput.Add(scopeSightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT, 10)
        scopeSightInput.Add(self.scopeSightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.scopeSightInputBox.Enable(False)

        scopeLoadout.Add(scopeInput, 0, wx.BOTTOM|wx.EXPAND, 1)
        scopeLoadout.Add(scopeSightInput, 0, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)

        """ Sight select row"""
        sightInput = wx.BoxSizer(wx.HORIZONTAL)
        sightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.sightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[""], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.sightInputBox.AppendItems(self.sightValue)
        sightInput.Add(sightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        sightInput.Add(self.sightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.sightInputBox.Enable(False)

        """ Socket loadout select row"""
        socketLoadout = wx.BoxSizer(wx.VERTICAL)
        self.socketLoadoutSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Enahncers:"), wx.HORIZONTAL)
        socketLoadout.Add(self.socketLoadoutSizer, 1, wx.EXPAND, 0)

        with Session() as session:
            enahncerQuery = session.query(EnhancerClass).filter(EnhancerClass.enhancerTypeID == 3)
            enhancerValues = list(map(lambda enhancer: enhancer.getTypeName(), enahncerQuery))

        # Socket 1 to 5 [section left]
        socketOnetoFive = wx.BoxSizer(wx.VERTICAL)

        socketOne = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 1"), wx.HORIZONTAL)
        self.socketOneInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketOneInputBox.SetItems(enhancerValues)
        self.socketOneAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketOneInputBox.Enable(False)
        self.socketOneAmount.Enable(False)
        socketOne.Add(self.socketOneInputBox, 1, 0, 0)
        socketOne.Add(self.socketOneAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketOne, 0, wx.EXPAND, 0)

        socketTwo = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 2"), wx.HORIZONTAL)
        self.socketTwoInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketTwoInputBox.SetItems(enhancerValues)
        self.socketTwoAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketTwoInputBox.Enable(False)
        self.socketTwoAmount.Enable(False)
        socketTwo.Add(self.socketTwoInputBox, 1, 0, 0)
        socketTwo.Add(self.socketTwoAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketTwo, 0, wx.EXPAND, 0)

        socketThree = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 3"), wx.HORIZONTAL)
        self.socketThreeInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketThreeInputBox.SetItems(enhancerValues)
        self.socketThreeAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketThreeInputBox.Enable(False)
        self.socketThreeAmount.Enable(False)
        socketThree.Add(self.socketThreeInputBox, 1, 0, 0)
        socketThree.Add(self.socketThreeAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketThree, 0, wx.EXPAND, 0)

        socketFour = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 4"), wx.HORIZONTAL)
        self.socketFourInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketFourInputBox.SetItems(enhancerValues)
        self.socketFourAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketFourInputBox.Enable(False)
        self.socketFourAmount.Enable(False)
        socketFour.Add(self.socketFourInputBox, 1, 0, 0)
        socketFour.Add(self.socketFourAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketFour, 0, wx.EXPAND, 0)

        socketFive = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 5"), wx.HORIZONTAL)
        self.socketFiveInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketFiveInputBox.SetItems(enhancerValues)
        self.socketFiveAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketFiveInputBox.Enable(False)
        self.socketFiveAmount.Enable(False)
        socketFive.Add(self.socketFiveInputBox, 1, 0, 0)
        socketFive.Add(self.socketFiveAmount, 0, 0 ,0)
        socketOnetoFive.Add(socketFive, 0, wx.EXPAND, 0)

        self.socketLoadoutSizer.Add(socketOnetoFive, 1, wx.LEFT|wx.RIGHT, 5)

        # Socket 6 to 10 [section right]
        socketSixtoTen = wx.BoxSizer(wx.VERTICAL)

        socketSix = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 6"), wx.HORIZONTAL)
        self.socketSixInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketSixInputBox.SetItems(enhancerValues)
        self.socketSixAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketSixInputBox.Enable(False)
        self.socketSixAmount.Enable(False)
        socketSix.Add(self.socketSixInputBox, 1, 0, 0)
        socketSix.Add(self.socketSixAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketSix, 0, wx.EXPAND, 0)

        socketSeven = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 7"), wx.HORIZONTAL)
        self.socketSevenInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketSevenInputBox.SetItems(enhancerValues)
        self.socketSevenAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketSevenInputBox.Enable(False)
        self.socketSevenAmount.Enable(False)
        socketSeven.Add(self.socketSevenInputBox, 1, 0, 0)
        socketSeven.Add(self.socketSevenAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketSeven, 0, wx.EXPAND, 0)

        socketEight = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 8"), wx.HORIZONTAL)
        self.socketEightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketEightInputBox.SetItems(enhancerValues)
        self.socketEightAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketEightInputBox.Enable(False)
        self.socketEightAmount.Enable(False)
        socketEight.Add(self.socketEightInputBox, 1, 0, 0)
        socketEight.Add(self.socketEightAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketEight, 0, wx.EXPAND, 0)

        socketNine = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 9"), wx.HORIZONTAL)
        self.socketNineInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketNineInputBox.SetItems(enhancerValues)
        self.socketNineAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketNineInputBox.Enable(False)
        self.socketNineAmount.Enable(False)
        socketNine.Add(self.socketNineInputBox, 1, 0, 0)
        socketNine.Add(self.socketNineAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketNine, 0, wx.EXPAND, 0)

        socketTen = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 10"), wx.HORIZONTAL)
        self.socketTenInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.socketTenInputBox.SetItems(enhancerValues)
        self.socketTenAmount = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
        self.socketTenInputBox.Enable(False)
        self.socketTenAmount.Enable(False)
        socketTen.Add(self.socketTenInputBox, 1, 0, 0)
        socketTen.Add(self.socketTenAmount, 0, 0 ,0)
        socketSixtoTen.Add(socketTen, 0, wx.EXPAND, 0)

        self.socketLoadoutSizer.Add(socketSixtoTen, 1, wx.LEFT|wx.RIGHT, 5)

        """Button controls"""
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.buttonSave = wx.Button(self, wx.ID_SAVE, "Save")
        self.buttonSave.SetDefault()
        self.buttonSave.Enable(False)
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

        self.weaponInputBox.Bind(wx.EVT_COMBOBOX, self.onWepSelect)
        self.scopeInputBox.Bind(wx.EVT_COMBOBOX, self.onScopeSelect)
        self.weaponLoadoutNameInput.Bind(wx.EVT_TEXT, self.onNameSet)

    def on_save(self, event):
            print("I SAVED")

    def onWepSelect(self, event):
            selectedWeaponName = event.GetString()
            self.ampInputBox.SetSelection(-1)
            self.absorberInputBox.SetSelection(-1)
            self.scopeInputBox.SetSelection(-1)
            self.scopeSightInputBox.SetSelection(-1)
            self.scopeSightInputBox.Enable(False)
            self.sightInputBox.SetSelection(-1)
            if selectedWeaponName == "":
                print("No item selected")
                self.ampInputBox.Enable(False)
                self.absorberInputBox.Enable(False)
                self.scopeInputBox.Enable(False)
                self.scopeSightInputBox.Enable(False)
                self.sightInputBox.Enable(False)
                # disalbe sockets
                self.socketOneInputBox.Disable()
                self.socketOneAmount.Disable()
                self.socketTwoInputBox.Enable(False)
                self.socketTwoAmount.Enable(False)
                self.socketThreeInputBox.Enable(False)
                self.socketThreeAmount.Enable(False)
                self.socketFourInputBox.Enable(False)
                self.socketFourAmount.Enable(False)
                self.socketFiveInputBox.Enable(False)
                self.socketFiveAmount.Enable(False)
                self.socketSixInputBox.Enable(False)
                self.socketSixAmount.Enable(False)
                self.socketSevenInputBox.Enable(False)
                self.socketSevenAmount.Enable(False)
                self.socketEightInputBox.Enable(False)
                self.socketEightAmount.Enable(False)
                self.socketNineInputBox.Enable(False)
                self.socketNineAmount.Enable(False)
                self.socketTenInputBox.Enable(False)
                self.socketTenAmount.Enable(False)
            else:
                with Session() as session:
                    selectedWeapon = session.query(Weapons).filter_by(name=selectedWeaponName).first()
                    print(selectedWeaponName)

                    # Amp
                    self.ampInputBox.Enable(True)
                    ampQuery = list(map(lambda amp: amp.name, selectedWeapon.type.amps))
                    self.ampInputBox.SetItems([""])
                    self.ampInputBox.AppendItems(ampQuery)

                    # Abs
                    self.absorberInputBox.Enable(True)
                    if selectedWeapon.type.type != "melee":
                        self.absorberInputBox.SetItems([""])
                        self.absorberInputBox.AppendItems(self.absValue)
                    # Enhancer
                    self.socketOneInputBox.Enable()
                    self.socketOneAmount.Enable(True)
                    self.socketTwoInputBox.Enable(True)
                    self.socketTwoAmount.Enable(True)
                    self.socketThreeInputBox.Enable(True)
                    self.socketThreeAmount.Enable(True)
                    self.socketFourInputBox.Enable(True)
                    self.socketFourAmount.Enable(True)
                    self.socketFiveInputBox.Enable(True)
                    self.socketFiveAmount.Enable(True)
                    self.socketSixInputBox.Enable(True)
                    self.socketSixAmount.Enable(True)
                    self.socketSevenInputBox.Enable(True)
                    self.socketSevenAmount.Enable(True)
                    self.socketEightInputBox.Enable(True)
                    self.socketEightAmount.Enable(True)
                    self.socketNineInputBox.Enable(True)
                    self.socketNineAmount.Enable(True)
                    self.socketTenInputBox.Enable(True)
                    self.socketTenAmount.Enable(True)
                    # enhancers here in subfyunc
                if selectedWeapon.type.type == "laser" or selectedWeapon.type.type == "blp":
                    self.scopeInputBox.Enable(True)
                    self.sightInputBox.Enable(True)
                else:
                    if selectedWeapon.type.type == "melee":
                        absMeleeQuery = session.query(WeaponAbsorbers)
                        absMeleeValue = list(map(lambda abs: abs.name, absMeleeQuery))
                        self.absorberInputBox.SetItems([""])
                        self.absorberInputBox.AppendItems(absMeleeValue)
                    self.scopeInputBox.Enable(False)
                    self.scopeInputBox.SetSelection(-1)
                    self.scopeSightInputBox.Enable(False)
                    self.scopeSightInputBox.SetSelection(-1)
                    self.sightInputBox.Enable(False)
                    self.sightInputBox.SetSelection(-1)

    def onScopeSelect(self, event):
        selectedScopeName = event.GetString()
        if selectedScopeName == "":
            self.scopeSightInputBox.Enable(False)
            self.scopeSightInputBox.SetSelection(-1)
        else:
            self.scopeSightInputBox.Enable(True)

    def onNameSet(self, event):
        #check if name not in use by other loadout (or overwrite exustugn loadout if known?)
        setName = event.GetEventObject()
        if not setName.IsEmpty():
            self.buttonSave.Enable(True)
        else:
            self.buttonSave.Enable(False)
