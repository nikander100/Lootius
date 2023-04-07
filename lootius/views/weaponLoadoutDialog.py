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

        weaponInputName = wx.StaticText(self, wx.ID_ANY, "Weapon:", style=wx.ALIGN_LEFT)
        self.weaponInputBox = wx.ComboBox(self, wx.ID_ANY, value="Select..", choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.__widgetMaker(self.weaponInputBox, weaponQuery)
        weaponInput.Add(weaponInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        weaponInput.Add(self.weaponInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        """ Amp select row"""
        ampInput = wx.BoxSizer(wx.HORIZONTAL)
        ampInputName = wx.StaticText(self, wx.ID_ANY, "Amplifier:", style=wx.ALIGN_LEFT)
        self.ampInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        ampInput.Add(ampInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        ampInput.Add(self.ampInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.ampInputBox.Disable()

        """ Absorber select row"""
        absorberInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            self.absQuery = session.query(WeaponAbsorbers).filter(WeaponAbsorbers.weaponTypeID == 1)
            self.absMeleeQuery = session.query(WeaponAbsorbers)
        
        absorberInputName = wx.StaticText(self, wx.ID_ANY, "Absorber:", style=wx.ALIGN_LEFT)
        self.absorberInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        absorberInput.Add(absorberInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        absorberInput.Add(self.absorberInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.absorberInputBox.Disable()

        """ Scope loadout select row"""
        scopeLoadout = wx.BoxSizer(wx.VERTICAL)

        # Scope select row
        scopeInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            scopeQuery = session.query(Scopes)

        scopeInputName = wx.StaticText(self, wx.ID_ANY, "Scope:", style=wx.ALIGN_LEFT)
        self.scopeInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.__widgetMaker(self.scopeInputBox, scopeQuery)
        scopeInput.Add(scopeInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        scopeInput.Add(self.scopeInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.scopeInputBox.Disable()

        # ScopeSight select row
        scopeSightInput = wx.BoxSizer(wx.HORIZONTAL)
        with Session() as session:
            sightQuery = session.query(Sights)

        scopeSightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.scopeSightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.__widgetMaker(self.scopeSightInputBox, sightQuery)
        scopeSightInput.Add(scopeSightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT, 10)
        scopeSightInput.Add(self.scopeSightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.scopeSightInputBox.Disable()

        scopeLoadout.Add(scopeInput, 0, wx.BOTTOM|wx.EXPAND, 1)
        scopeLoadout.Add(scopeSightInput, 0, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)

        """ Sight select row"""
        sightInput = wx.BoxSizer(wx.HORIZONTAL)
        sightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.sightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.__widgetMaker(self.sightInputBox, sightQuery)
        sightInput.Add(sightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        sightInput.Add(self.sightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.sightInputBox.Disable()

        """ Socket loadout select row"""
        socketLoadout = wx.BoxSizer(wx.VERTICAL)
        self.socketLoadoutSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Enahncers:"), wx.HORIZONTAL)
        socketLoadout.Add(self.socketLoadoutSizer, 1, wx.EXPAND, 0)

        with Session() as session:
            enahncerQuery = session.query(EnhancerClass).filter(EnhancerClass.enhancerTypeID == 3)
            enhancerValues = list(map(lambda enhancer: enhancer.getTypeName(), enahncerQuery))

        self.socket = {}
        socketNames = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
        for name in socketNames:
            self.socket[name] = {
                "Item": wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY),
                "Amount": wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=999)
            }
            self.socket[name]["Item"].Disable()
            self.socket[name]["Amount"].Disable()

        # Socket 1 to 5 [section left]
        socketOnetoFive = wx.BoxSizer(wx.VERTICAL)

        socketOne = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 1"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["One"]["Item"], enahncerQuery, True)
        socketOne.Add(self.socket["One"]["Item"], 1, 0, 0)
        socketOne.Add(self.socket["One"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketOne, 0, wx.EXPAND, 0)

        socketTwo = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 2"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Two"]["Item"], enahncerQuery, True)
        socketTwo.Add(self.socket["Two"]["Item"], 1, 0, 0)
        socketTwo.Add(self.socket["Two"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketTwo, 0, wx.EXPAND, 0)

        socketThree = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 3"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Three"]["Item"], enahncerQuery, True)
        socketThree.Add(self.socket["Three"]["Item"], 1, 0, 0)
        socketThree.Add(self.socket["Three"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketThree, 0, wx.EXPAND, 0)

        socketFour = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 4"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Four"]["Item"], enahncerQuery, True)
        socketFour.Add(self.socket["Four"]["Item"], 1, 0, 0)
        socketFour.Add(self.socket["Four"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketFour, 0, wx.EXPAND, 0)

        socketFive = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 5"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Five"]["Item"], enahncerQuery, True)
        socketFive.Add(self.socket["Five"]["Item"], 1, 0, 0)
        socketFive.Add(self.socket["Five"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketFive, 0, wx.EXPAND, 0)

        self.socketLoadoutSizer.Add(socketOnetoFive, 1, wx.LEFT|wx.RIGHT, 5)

        # Socket 6 to 10 [section right]
        socketSixtoTen = wx.BoxSizer(wx.VERTICAL)

        socketSix = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 6"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Six"]["Item"], enahncerQuery, True)
        socketSix.Add(self.socket["Six"]["Item"], 1, 0, 0)
        socketSix.Add(self.socket["Six"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketSix, 0, wx.EXPAND, 0)

        socketSeven = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 7"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Seven"]["Item"], enahncerQuery, True)
        socketSeven.Add(self.socket["Seven"]["Item"], 1, 0, 0)
        socketSeven.Add(self.socket["Seven"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketSeven, 0, wx.EXPAND, 0)

        socketEight = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 8"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Eight"]["Item"], enahncerQuery, True)
        socketEight.Add(self.socket["Eight"]["Item"], 1, 0, 0)
        socketEight.Add(self.socket["Eight"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketEight, 0, wx.EXPAND, 0)

        socketNine = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 9"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Nine"]["Item"], enahncerQuery, True)
        socketNine.Add(self.socket["Nine"]["Item"], 1, 0, 0)
        socketNine.Add(self.socket["Nine"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketNine, 0, wx.EXPAND, 0)

        socketTen = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 10"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Ten"]["Item"], enahncerQuery, True)
        socketTen.Add(self.socket["Ten"]["Item"], 1, 0, 0)
        socketTen.Add(self.socket["Ten"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketTen, 0, wx.EXPAND, 0)

        self.socketLoadoutSizer.Add(socketSixtoTen, 1, wx.LEFT|wx.RIGHT, 5)

        """Button controls"""
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.buttonSave = wx.Button(self, wx.ID_SAVE, "Save")
        self.buttonSave.SetDefault()
        self.buttonSave.Disable()
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
        self.buttonSave.Bind(wx.EVT_BUTTON, self.onSave)

    def __widgetMaker(self, widget, querys, isEnhancer=False):
        # set first item (empty selector)
        widget.Clear()
        widget.Append("")
        # set names (if enhancer is true use other value)
        if isEnhancer != True:
            value = list(map(lambda query: query.name, querys))
        else:
            value = list(map(lambda query: query.getTypeName(), querys))
        widget.Append(value)
        # set client data (id reference for the item)
        for _, obj in enumerate(querys):
            widget.SetClientData(_ + 1, obj.id)

    def __enableEnhancers(self):
        for _, enhancer in self.socket.items():
            enhancer["Item"].Enable()
            enhancer["Amount"].Enable()

    def __disableEnhancers(self):
        for _, enhancer in self.socket.items():
            enhancer["Item"].Disable()
            enhancer["Amount"].Disable()

    def onWepSelect(self, event):
            selectedWeaponID = event.GetClientData()
            self.ampInputBox.SetSelection(-1)
            self.absorberInputBox.SetSelection(-1)
            self.scopeInputBox.SetSelection(-1)
            self.scopeSightInputBox.SetSelection(-1)
            self.scopeSightInputBox.Disable()
            self.sightInputBox.SetSelection(-1)
            if selectedWeaponID == None:
                print("No item selected")
                self.ampInputBox.Disable()
                self.absorberInputBox.Disable()
                self.scopeInputBox.Disable()
                self.scopeSightInputBox.Disable()
                self.sightInputBox.Disable()
                self.__disableEnhancers()
                
            else:
                with Session() as session:
                    selectedWeapon = session.query(Weapons).filter_by(id=selectedWeaponID).first()
                    print(f"\n\n\n{selectedWeapon.name}\n\n\n") #debug

                    # Amp
                    self.ampInputBox.Enable()
                    self.__widgetMaker(self.ampInputBox, selectedWeapon.type.amps)

                    # Abs
                    self.absorberInputBox.Enable()
                    self.__widgetMaker(self.absorberInputBox, self.absQuery)
                    # Enhancer
                    self.__enableEnhancers()
                if selectedWeapon.type.type == "laser" or selectedWeapon.type.type == "blp":
                    self.scopeInputBox.Enable()
                    self.sightInputBox.Enable()
                else:
                    if selectedWeapon.type.type == "melee":
                        self.__widgetMaker(self.absorberInputBox, self.absQuery)
                    self.scopeInputBox.Disable()
                    self.scopeInputBox.SetSelection(-1)
                    self.scopeSightInputBox.Disable()
                    self.scopeSightInputBox.SetSelection(-1)
                    self.sightInputBox.Disable()
                    self.sightInputBox.SetSelection(-1)

    def onScopeSelect(self, event):
        selectedScopeName = event.GetString()
        if selectedScopeName == "":
            self.scopeSightInputBox.Disable()
            self.scopeSightInputBox.SetSelection(-1)
        else:
            self.scopeSightInputBox.Enable()

    def onNameSet(self, event):
        #check if name not in use by other loadout (or overwrite exustugn loadout if known?)
        setName = event.GetEventObject()
        if not setName.IsEmpty():
            self.buttonSave.Enable()
        else:
            self.buttonSave.Disable()

    # Dummy Save
    def onSave(self, event):
        selectedName = self.weaponLoadoutNameInput.GetValue()
        selectedWeapon = self.weaponInputBox.GetClientData(self.weaponInputBox.GetSelection()) if self.weaponInputBox.GetSelection() != -1 else None
        selectedAmp = self.ampInputBox.GetClientData(self.ampInputBox.GetSelection()) if self.ampInputBox.GetSelection() != -1 else None
        selectedAbs = self.absorberInputBox.GetClientData(self.absorberInputBox.GetSelection()) if self.absorberInputBox.GetSelection() != -1 else None
        selectedScope = self.scopeInputBox.GetClientData(self.scopeInputBox.GetSelection()) if self.scopeInputBox.GetSelection() != -1 else None
        selectedScopeSight = self.scopeSightInputBox.GetClientData(self.scopeSightInputBox.GetSelection()) if self.scopeSightInputBox.GetSelection() != -1 else None
        selectedSight = self.sightInputBox.GetClientData(self.sightInputBox.GetSelection()) if self.sightInputBox.GetSelection() != -1 else None
        selectedLoadout = [selectedName, selectedWeapon, selectedAmp, selectedAbs, selectedScope, selectedScopeSight, selectedSight]
        # selectedEnhancer
        # selectedEnhancerAmount
        print("I SAVED ",selectedLoadout)