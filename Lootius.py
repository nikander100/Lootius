#!/usr/bin/env python
import wx

class LootiusFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(LootiusFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self);

        # put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Hello Lootius!");
        font = st.GetFont();
        font.PointSize += 10;
        font = font.Bold();
        st.SetFont(font);

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL);
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25));
        pnl.SetSizer(sizer);

        # create a menu bar
        self.makeMenuBar()

        # add a status bar
        self.CreateStatusBar();
        self.SetStatusText("Welcome to Lootius, may I be with you!");


    def makeMenuBar(self):
        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu();
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item");
        fileMenu.AppendSeparator();
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT);

        # Now a help menu for the about item
        helpMenu = wx.Menu();
        aboutItem = helpMenu.Append(wx.ID_ABOUT);
        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar();
        menuBar.Append(fileMenu, "&File");
        menuBar.Append(helpMenu, "&Help");

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem);
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem);
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem);


    def OnExit(self, event):
        self.Close(True);
    def OnHello(self, event):
        wx.MessageBox("Hello again from Lootius, what are you doing here?");
    def OnAbout(self, event):
        wx.MessageBox("This is Lootius, a loot tracker and toolbox for Entropia Universe.\nThis application is developed by Nikander and k-Max, but is opensource, feel free to contribute to it!", 
                    "About us.",
                    wx.OK|wx.ICON_INFORMATION);

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    lootius = wx.App();
    frm = LootiusFrame(None, title="Lootius");
    frm.Show();
    lootius.MainLoop();
