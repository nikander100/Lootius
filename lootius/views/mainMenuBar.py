#!/usr/bin/env python
import wx

class mainMenuBar(wx.MenuBar):
    def __init__(self, LootiusFrame):

        wx.MenuBar.__init__(self);

        # File menu
        fileMenu = wx.Menu();
        self.Append(fileMenu, "&File");

        preferencesShortCut = "CTRL+,";
        preferencesItem = wx.MenuItem(fileMenu, wx.ID_PREFERENCES, "&Preferences" + "\t" + preferencesShortCut);
        fileMenu.Append(preferencesItem)
        fileMenu.AppendSeparator();
        fileMenu.Append(wx.ID_EXIT);

        # Help menu
        helpMenu = wx.Menu();
        self.Append(helpMenu, "&Help");

        helpMenu.Append(wx.ID_ABOUT);