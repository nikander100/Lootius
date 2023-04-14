#!/usr/bin/env python
import wx
from modules import loadoutManager

class WeaponLoadoutDialog(wx.Dialog):
    """
    A dialog for creating a new weapon loadout.

    Parameters
    ----------
    parent : wx.Window
        The parent window of the dialog.

    Attributes
    ----------
    weaponLoadoutNameInput : wx.TextCtrl
        The input box for the name of the weapon loadout.
    weaponInputBox : wx.ComboBox
        The combo box for selecting a weapon.
    ampInputBox : wx.ComboBox
        The combo box for selecting an amplifier.
    absInputBox : wx.ComboBox
        The combo box for selecting an absorber.
    scopeInputBox : wx.ComboBox
        The combo box for selecting a scope.
    scopeSightInputBox : wx.ComboBox
        The combo box for selecting a sight for the scope.
    sightInputBox : wx.ComboBox
        The combo box for selecting a sight.
    socket : dict
        A dictionary that maps socket names to their respective components. \n
        Each socket component is a dictionary with the following keys: \n
            * "Item": wx.ComboBox  \n
                The combo box for selecting a enhancer. \n
            * "Amount": wx.SpinCtrl \n
            The Spinctrl object representing the amount of enhancers.

    Methods
    -------
    __init__(self, parent)
        Initializes the dialog window.
    __widgetMaker(self, widget, query)
        Populates a combo box with items from a query.
    __enableEnhancers(self)
        Enables all socket enhancers.
    __disableEnhancers(self)
        Disables all socket enhancers.
    __resetEnhancers(self)
        Reset all socket enhancers to their default values.
    onWepSelect(self, event):
        Event handler for when a weapon is selected in the weapon combo box.
    onEnhancerSelect(self, event, enhancerAmountSpinCtrl):
        Event handler for when a enhancer is selected from the combobox.
    onScopeSelect(self, event):
        Event handler for when a scope is selected in the scope combo box.
    onNameSet(self, event):
        Enable the save button if the weapon loadout name is not empty.
    onSave(self, event):
        Event handler for when the "Save" button is clicked. Saves the selected loadout values to the loadout manager.
    
    """
    def __init__(self, parent):
        """
        Initialize the WeaponLoadoutDialog.

        Parameters
        ----------
        parent : wx.Window
            The parent window.
        """
        super().__init__(parent, id=wx.ID_ANY, title=(f"{parent.title} - Add Weapon Loadout"), style=wx.CAPTION|wx.CLOSE_BOX)

        weaponLoadout = wx.BoxSizer(wx.VERTICAL)
        
        weaponLoadoutName = wx.BoxSizer(wx.HORIZONTAL)
        weaponLoadoutNameText = wx.StaticText(self, wx.ID_ANY, "Name:", style=wx.ALIGN_LEFT)
        self.weaponLoadoutNameInput = wx.TextCtrl(self, wx.ID_ANY, "")
        weaponLoadoutName.Add(weaponLoadoutNameText, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        weaponLoadoutName.Add(self.weaponLoadoutNameInput, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        weaponInput = wx.BoxSizer(wx.HORIZONTAL)
        weapons = loadoutManager.getWeapons()

        weaponInputName = wx.StaticText(self, wx.ID_ANY, "Weapon:", style=wx.ALIGN_LEFT)
        self.weaponInputBox = wx.ComboBox(self, wx.ID_ANY, value="Select..", choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.__widgetMaker(self.weaponInputBox, weapons)
        weaponInput.Add(weaponInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        weaponInput.Add(self.weaponInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        ampInput = wx.BoxSizer(wx.HORIZONTAL)
        ampInputName = wx.StaticText(self, wx.ID_ANY, "Amplifier:", style=wx.ALIGN_LEFT)
        self.ampInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        ampInput.Add(ampInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        ampInput.Add(self.ampInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.ampInputBox.Disable()

        absInput = wx.BoxSizer(wx.HORIZONTAL)
        self.absorbers = loadoutManager.getAbsorbers(weaponType=1)
        self.meleeobsorbers = loadoutManager.getAbsorbers()
        
        absInputName = wx.StaticText(self, wx.ID_ANY, "Absorber:", style=wx.ALIGN_LEFT)
        self.absInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        absInput.Add(absInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        absInput.Add(self.absInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.absInputBox.Disable()

        scopeLoadout = wx.BoxSizer(wx.VERTICAL)

        scopeInput = wx.BoxSizer(wx.HORIZONTAL)
        scopes = loadoutManager.getScopes()

        scopeInputName = wx.StaticText(self, wx.ID_ANY, "Scope:", style=wx.ALIGN_LEFT)
        self.scopeInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.__widgetMaker(self.scopeInputBox, scopes)
        scopeInput.Add(scopeInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        scopeInput.Add(self.scopeInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.scopeInputBox.Disable()

        scopeSightInput = wx.BoxSizer(wx.HORIZONTAL)
        sights = loadoutManager.getSights()

        scopeSightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.scopeSightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.__widgetMaker(self.scopeSightInputBox, sights)
        scopeSightInput.Add(scopeSightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT, 10)
        scopeSightInput.Add(self.scopeSightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.scopeSightInputBox.Disable()

        scopeLoadout.Add(scopeInput, 0, wx.BOTTOM|wx.EXPAND, 1)
        scopeLoadout.Add(scopeSightInput, 0, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)

        sightInput = wx.BoxSizer(wx.HORIZONTAL)
        sightInputName = wx.StaticText(self, wx.ID_ANY, "Sight:", style=wx.ALIGN_LEFT)
        self.sightInputBox = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.__widgetMaker(self.sightInputBox, sights)
        sightInput.Add(sightInputName, 1, wx.ALIGN_CENTER_VERTICAL|wx.FIXED_MINSIZE|wx.LEFT|wx.RIGHT, 5)
        sightInput.Add(self.sightInputBox, 5, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.sightInputBox.Disable()

        socketLoadout = wx.BoxSizer(wx.VERTICAL)
        self.socketLoadoutSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Enahncers:"), wx.HORIZONTAL)
        socketLoadout.Add(self.socketLoadoutSizer, 1, wx.EXPAND, 0)

        enhancers = loadoutManager.getEnhancers(3)

        self.socket = {}
        socketNames = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
        for name in socketNames:
            self.socket[name] = {
                "Item": wx.ComboBox(self, wx.ID_ANY, name=name, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY),
                "Amount": wx.SpinCtrl(self, wx.ID_ANY, "0", name=name, min=0, max=999)
            }
            self.socket[name]["Item"].Disable()
            self.socket[name]["Amount"].Disable()

        socketOnetoFive = wx.BoxSizer(wx.VERTICAL)
        "Socket 1 to 5 [section left]"

        socketOne = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 1"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["One"]["Item"], enhancers)
        socketOne.Add(self.socket["One"]["Item"], 1, 0, 0)
        socketOne.Add(self.socket["One"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketOne, 0, wx.EXPAND, 0)

        socketTwo = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 2"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Two"]["Item"], enhancers)
        socketTwo.Add(self.socket["Two"]["Item"], 1, 0, 0)
        socketTwo.Add(self.socket["Two"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketTwo, 0, wx.EXPAND, 0)

        socketThree = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 3"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Three"]["Item"], enhancers)
        socketThree.Add(self.socket["Three"]["Item"], 1, 0, 0)
        socketThree.Add(self.socket["Three"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketThree, 0, wx.EXPAND, 0)

        socketFour = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 4"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Four"]["Item"], enhancers)
        socketFour.Add(self.socket["Four"]["Item"], 1, 0, 0)
        socketFour.Add(self.socket["Four"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketFour, 0, wx.EXPAND, 0)

        socketFive = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 5"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Five"]["Item"], enhancers)
        socketFive.Add(self.socket["Five"]["Item"], 1, 0, 0)
        socketFive.Add(self.socket["Five"]["Amount"], 0, 0 ,0)
        socketOnetoFive.Add(socketFive, 0, wx.EXPAND, 0)

        self.socketLoadoutSizer.Add(socketOnetoFive, 1, wx.LEFT|wx.RIGHT, 5)

        socketSixtoTen = wx.BoxSizer(wx.VERTICAL)
        "Socket 6 to 10 [section right]"

        socketSix = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 6"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Six"]["Item"], enhancers)
        socketSix.Add(self.socket["Six"]["Item"], 1, 0, 0)
        socketSix.Add(self.socket["Six"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketSix, 0, wx.EXPAND, 0)

        socketSeven = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 7"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Seven"]["Item"], enhancers)
        socketSeven.Add(self.socket["Seven"]["Item"], 1, 0, 0)
        socketSeven.Add(self.socket["Seven"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketSeven, 0, wx.EXPAND, 0)

        socketEight = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 8"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Eight"]["Item"], enhancers)
        socketEight.Add(self.socket["Eight"]["Item"], 1, 0, 0)
        socketEight.Add(self.socket["Eight"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketEight, 0, wx.EXPAND, 0)

        socketNine = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 9"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Nine"]["Item"], enhancers)
        socketNine.Add(self.socket["Nine"]["Item"], 1, 0, 0)
        socketNine.Add(self.socket["Nine"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketNine, 0, wx.EXPAND, 0)

        socketTen = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Socket 10"), wx.HORIZONTAL)
        self.__widgetMaker(self.socket["Ten"]["Item"], enhancers)
        socketTen.Add(self.socket["Ten"]["Item"], 1, 0, 0)
        socketTen.Add(self.socket["Ten"]["Amount"], 0, 0 ,0)
        socketSixtoTen.Add(socketTen, 0, wx.EXPAND, 0)

        self.socketLoadoutSizer.Add(socketSixtoTen, 1, wx.LEFT|wx.RIGHT, 5)

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        """Button controls"""
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
        weaponLoadout.Add(absInput, 0, wx.BOTTOM|wx.EXPAND|wx.TOP, 5)
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
        for name in self.socket:
            self.socket[name]["Item"].Bind(wx.EVT_COMBOBOX, lambda event, name=name: self.onEnhancerSelect(event, self.socket[name]["Amount"]))

    #possibly be added to modules later, if used in other files to!
    def __widgetMaker(self, widget, data):
        """
        Clear and populate a wxPython widget with query names and associated IDs.

        Parameters
        ----------
        widget : wxPython widget
            The widget to be cleared and populated.
        data : tuple of lists
            A tuple of two lists, where the first list contains the names of the data and the second
            list contains the IDs of the corresponding data.

        Returns
        -------
        None

        Notes
        -----
        The `widget` is first cleared using its `Clear()` method, and then an empty
        string is appended to it using `widget.Append("")`.

        The function creates a list of data names by extracting the first list of the `data` tuple.
        It then appends the list of names to the `widget` using `widget.Append(name)`.

        Finally, the function iterates over the IDs of the data using `enumerate()`
        to get both the index and the ID, and calls
        `widget.SetClientData(_ + 1, id)` for each ID in the list. This sets
        the client data associated with the item in the `widget` to the corresponding ID, plus 1.
        """
        widget.Clear()
        widget.Append("")
        widget.Append(data[0])
        for i, id in enumerate(data[1]):
            widget.SetClientData(i + 1, id)

    def __enableEnhancers(self):
        """
        Enables all socket enhancers.

        This method loops through all the socket components and enables the 'Item' field of each enhancer.
        """
        for _, enhancer in self.socket.items():
            enhancer["Item"].Enable()

    def __disableEnhancers(self):
        """
        Disables all socket enhancer components in the dialog window.

        The method iterates through each socket in the `socket` dictionary and disables
        both the `"Item"` and `"Amount"` components for the socket.
        """
        for _, enhancer in self.socket.items():
            enhancer["Item"].Disable()
            enhancer["Amount"].Disable()
    
    def __resetEnhancers(self):
        """
        Reset all socket enhancers to their default values.
    
        For each socket, set the enhancer item selection to -1 (unselected)
        and set the enhancer amount to its minimum value.
        """
        for _, enhancer in self.socket.items():
            enhancer["Item"].SetSelection(-1)
            enhancer["Amount"].SetValue(enhancer["Amount"].GetMin())


    def onWepSelect(self, event):
            """
            Event handler for when a weapon is selected in the weapon combo box.

            Parameters
            ----------
            event : wx.Event
                The event object that triggered the function call, and contains data from the combo box.

            Returns
            -------
            None

            Notes
            -----
            This function resets the values of all input boxes and combo boxes, and then enables or disables them
            based on the selected weapon type. It also queries the database to populate the amplifier and absorber
            combo boxes with the relevant items for the selected weapon type.

            """
            selectedWeaponID = event.GetClientData()
            self.ampInputBox.SetSelection(-1)
            self.absInputBox.SetSelection(-1)
            self.scopeInputBox.SetSelection(-1)
            self.scopeSightInputBox.SetSelection(-1)
            self.scopeSightInputBox.Disable()
            self.sightInputBox.SetSelection(-1)
            self.__resetEnhancers()
            if selectedWeaponID == None:
                print("No item selected")
                self.ampInputBox.Disable()
                self.absInputBox.Disable()
                self.scopeInputBox.Disable()
                self.scopeSightInputBox.Disable()
                self.sightInputBox.Disable()
                self.__disableEnhancers()
                self.buttonSave.Disable()
                
            else:
                if not self.weaponLoadoutNameInput.IsEmpty():
                    self.buttonSave.Enable()

                selectedWeapon = loadoutManager.getSelectedWeapon(selectedWeaponID)
                print(f'\n\n\n{selectedWeapon["weapon"].name}\n\n\n') #debug

                # Amp
                self.ampInputBox.Enable()
                self.__widgetMaker(self.ampInputBox, selectedWeapon["amps"])

                # Abs
                self.absInputBox.Enable()
                self.__widgetMaker(self.absInputBox, self.absorbers)
                # Enhancer
                self.__enableEnhancers()
                if selectedWeapon["weapon"].type.type == "laser" or selectedWeapon["weapon"].type.type == "blp":
                    self.scopeInputBox.Enable()
                    self.sightInputBox.Enable()
                else:
                    if selectedWeapon["weapon"].type.type == "melee":
                        self.__widgetMaker(self.absInputBox, self.meleeobsorbers)
                    self.scopeInputBox.Disable()
                    self.scopeInputBox.SetSelection(-1)
                    self.scopeSightInputBox.Disable()
                    self.scopeSightInputBox.SetSelection(-1)
                    self.sightInputBox.Disable()
                    self.sightInputBox.SetSelection(-1)
    
    def onEnhancerSelect(self, event, enhancerAmountSpinCtrl):
        """
        Event handler for when a enhancer is selected from the combobox.

        Parameters
        ----------
        event : wx.CommandEvent
            The command event that triggered the handler.
        enhancerAmountSpinCtrl : wx.SpinCtrl
            The spin control object for the amount of the selected enhancer.

        Returns
        -------
        None

        Notes
        -----
        - This method enables the `enhancerAmountSpinCtrl` if a valid enhancer is selected.
        - If no enhancer is selected, the `enhancerAmountSpinCtrl` is disabled and its value is set to the minimum.

        """
        selectedEnhancerName = event.GetString()
        if selectedEnhancerName == "":
            enhancerAmountSpinCtrl.Disable()
        else:
            enhancerAmountSpinCtrl.Enable()
        enhancerAmountSpinCtrl.SetValue(enhancerAmountSpinCtrl.GetMin())

    def onScopeSelect(self, event):
        """
        Event handler for when a scope is selected in the `scopeInputBox` combo box.

        Parameters
        ----------
        event : wx.CommandEvent
            The event object.

        Returns
        -------
        None

        Notes
        -----
        This method enables the `scopeSightInputBox` combo box if a scope is selected,
        and disables it otherwise. If the combo box is disabled, its selection is reset
        to -1.
        """
        selectedScopeName = event.GetString()
        if selectedScopeName == "":
            self.scopeSightInputBox.Disable()
            self.scopeSightInputBox.SetSelection(-1)
        else:
            self.scopeSightInputBox.Enable()

    def onNameSet(self, event):
        """
        Enable the save button if the weapon loadout name is not empty and a weapon has been selected.

        vbnet

        Parameters
        ----------
        event : wxPython event object
            The event object.

        Returns
        -------
        None

        Notes
        -----
        This function is called when the user enters a weapon loadout name in the name input box.
        If the name input box is not empty and a weapon has been selected, the save button is enabled.
        Otherwise, the save button is disabled.

        If the save button is enabled, the user can click on it to save the weapon loadout with the
        entered name and selected weapon.
        """
        # TODO check if name not in use by other loadout (or overwrite exustugn loadout if known?)
        setName = event.GetEventObject()
        if not setName.IsEmpty() and self.weaponInputBox.GetSelection() != -1 and self.weaponInputBox.GetClientData(self.weaponInputBox.GetSelection()):
            self.buttonSave.Enable()
        else:
            self.buttonSave.Disable()

    def onSave(self, event):
        """
        Save the current loadout with the selected equipment.

        Parameters
        ----------
        event : wx.Event
            The event that triggered the function call.

        Returns
        -------
        None

        Notes
        -----
        This function retrieves the values of the currently selected equipment for the loadout and passes them to the
        loadout manager to save them. Finally, it ends the modal dialog.

        """
        selectedName = self.weaponLoadoutNameInput.GetValue()
        selectedWeapon = self.weaponInputBox.GetClientData(self.weaponInputBox.GetSelection())
        selectedAmp = self.ampInputBox.GetClientData(self.ampInputBox.GetSelection()) if self.ampInputBox.GetSelection() != -1 else None
        selectedAbs = self.absInputBox.GetClientData(self.absInputBox.GetSelection()) if self.absInputBox.GetSelection() != -1 else None
        selectedScope = self.scopeInputBox.GetClientData(self.scopeInputBox.GetSelection()) if self.scopeInputBox.GetSelection() != -1 else None
        selectedScopeSight = self.scopeSightInputBox.GetClientData(self.scopeSightInputBox.GetSelection()) if self.scopeSightInputBox.GetSelection() != -1 else None
        selectedSight = self.sightInputBox.GetClientData(self.sightInputBox.GetSelection()) if self.sightInputBox.GetSelection() != -1 else None
        selectedEnhancers = []
        for i, name in enumerate(self.socket):
            selectedEnhancers.append([
                i + 1,
                self.socket[name]["Item"].GetClientData(self.socket[name]["Item"].GetSelection()) if self.socket[name]["Item"].GetSelection() != -1 else None,
                self.socket[name]["Amount"].GetValue()
            ])
        loadoutManager.setLoadout(selectedName, selectedWeapon, selectedAmp, selectedAbs, selectedScope, selectedScopeSight, selectedSight, selectedEnhancers)
        print("\n\n\nI SAVED ",selectedName, selectedWeapon, selectedAmp, selectedAbs, selectedScope, selectedScopeSight, selectedSight, selectedEnhancers)
        self.EndModal(0)
    
    
