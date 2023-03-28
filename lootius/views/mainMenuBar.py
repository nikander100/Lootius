#!/usr/bin/env python
import wx

class mainMenuBar(wx.MenuBar):
    def __init__(self, LootiusFrame):
        self.weaponLoadoutEditorID = wx.NewId()
        self.fapLoadoutEditorID = wx.NewId()

        self.wikiID = wx.NewId()


        self.mainFrame = LootiusFrame
        wx.MenuBar.__init__(self);

        # File menu
        fileMenu = wx.Menu();
        self.Append(fileMenu, "&File");

        preferencesShortCut = "CTRL+,";
        preferencesItem = wx.MenuItem(fileMenu, wx.ID_PREFERENCES, "&Preferences" + "\t" + preferencesShortCut);
        fileMenu.Append(preferencesItem)
        fileMenu.AppendSeparator();
        
        fileMenu.Append(wx.ID_EXIT);

        # Combat Menu
        combatMenu = wx.Menu()
        self.Append(combatMenu, "&Combat")

        weaponLoadoutItem = wx.MenuItem(combatMenu, self.weaponLoadoutEditorID, "Add &Weapon Loadout")
        combatMenu.Append(weaponLoadoutItem)

        fapLoadoutItem = wx.MenuItem(combatMenu, self.fapLoadoutEditorID , "Add &Fap Loadout")
        combatMenu.Append(fapLoadoutItem)

        # Help menu
        helpMenu = wx.Menu();
        self.Append(helpMenu, "&Help")

        helpMenu.Append(self.wikiID, "&Github", "Go to Github repository")
        helpMenu.AppendSeparator();
        helpMenu.Append(wx.ID_ABOUT);