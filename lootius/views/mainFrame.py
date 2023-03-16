import wx
import wx.adv 

from views.mainMenuBar import mainMenuBar
from modules.logParser import ChatLogParser
from views.preferenceDialog import PreferenceDialog

class LootiusFrame(wx.Frame):

    def __init__(self, title="Lootius"):
        # ensure the parent's __init__ is called
        self.title = title
        super().__init__(None, wx.ID_ANY, self.title)
        self.SetSize(320, 160, 1280, 720)

        # Modules
        self.chatLogParser = ChatLogParser(self)

        # create a panel in the frame
        pnl = wx.Panel(self);

        # Add menubar
        self.SetMenuBar(mainMenuBar(self))
        self.registerMenu()

        # add a status bar
        self.CreateStatusBar();
        self.SetStatusText("Welcome to Lootius, may I be with you!"); ##show latest hof/global in statusbar option?

    def ExitApp(self, event):
        self.Close()
        event.Skip()

    def ShowAboutBox(self, event):
        info = wx.adv.AboutDialogInfo()
        info.Name = "Lootius"
        info.Version = "0.0.0"
        info.Description = "This is Lootius, a loot tracker and toolbox for Entropia Universe.\nThis application is developed by Nikander and k-Max, but is opensource, feel free to contribute to it!"
        info.AddDeveloper("Nikander")
        info.AddDeveloper("K-Max")
        wx.adv.AboutBox(info)

    def OnShowPreferenceDialog(self, event):
        with PreferenceDialog(self) as dlg:
            dlg.ShowModal()
    
    def registerMenu(self):
        menuBar = self.GetMenuBar();
        # Quit
        self.Bind(wx.EVT_MENU, self.ExitApp, id=wx.ID_EXIT)
        # About
        self.Bind(wx.EVT_MENU, self.ShowAboutBox, id=wx.ID_ABOUT)
        # Preference dialog
        self.Bind(wx.EVT_MENU, self.OnShowPreferenceDialog, id=wx.ID_PREFERENCES)


        # # put some text with a larger bold font on it
        # st = wx.StaticText(pnl, label="Hello Lootius!");
        # font = st.GetFont();
        # font.PointSize += 10;
        # font = font.Bold();
        # st.SetFont(font);

        # # and create a sizer to manage the layout of child widgets
        # sizer = wx.BoxSizer(wx.VERTICAL);
        # sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25));
        # pnl.SetSizer(sizer);