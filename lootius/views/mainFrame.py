import wx
import wx.adv 
import webbrowser

from modules.logParser import ChatLogParser
from views.mainMenuBar import mainMenuBar
from views.preferenceDialog import PreferenceDialog
from views.weaponLoadoutDialog import WeaponLoadoutDialog


"""
TODO Add min size for frame
"""
class LootiusFrame(wx.Frame):

    def __init__(self, title="Lootius", size=(320, 160, 1280, 720)):
        # ensure the parent's __init__ is called
        self.title = title
        super().__init__(None, wx.ID_ANY, self.title)
        self.Size = size
        self.SetBackgroundColour(wx.Colour(30,30,30))

        # Modules
        self.chatLogParser = ChatLogParser(self)

        # create a panel in the frame
        # pnl = wx.Panel(self);
        # pnl.SetBackgroundColour(wx.Colour(30,30,30))

        #tmp
        mains = wx.BoxSizer(wx.HORIZONTAL)
        buttonReset = wx.Button(self, wx.NewId(), "Reset Database")
        mains.Add(buttonReset, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))

        self.SetSizer(mains)
        self.Bind(wx.EVT_BUTTON, self.resetDb, id=buttonReset.GetId())
        #end tmp


        # Add menubar
        self.SetMenuBar(mainMenuBar(self))
        self.registerMenu()

        # add a status bar
        self.CreateStatusBar();
        self.SetStatusText("Welcome to Lootius, may I be with you!"); ##show latest hof/global in statusbar option?

    #tmp
    @staticmethod
    def resetDb(event):
        from time import sleep
        from database import db
        # from models.databaseModel import SocketLoadout

        # e = db.DB.getSession()
        # with e() as ses:
        #     ses.query(SocketLoadout).filter(SocketLoadout.id == 1).delete()
        #     ses.commit()
        # return
        from os.path import realpath, join, dirname, abspath
        dbPath = realpath(join(dirname(abspath(__file__)), "../database/", "lootiusTest.db"))

        db.DB.dropAll()
        print("\n\n\nDeleted DATABASE\n\n\n")
        sleep(3)
        db.Setup.run(dbPath)
        print("\n\n\nRemade DATABASE\n\n\n")
    #end tmp

    def ExitApp(self, event):
        self.Close()
        event.Skip()

    def ShowAboutBox(self, event):
        info = wx.adv.AboutDialogInfo()
        info.Name = "Lootius"
        info.Version = "0.0.0"
        info.Description = """This is Lootius, a loot tracker and toolbox for Entropia Universe.\n 
                            This application is developed by Nikander and k-Max, but is opensource, feel free to contribute to it!"""
        info.AddDeveloper("Nikander")
        info.AddDeveloper("K-Max")
        wx.adv.AboutBox(info)

    def OnShowPreferenceDialog(self, event):
        with PreferenceDialog(self) as dlg:
            dlg.ShowModal()
    
    def onShowWeaponLoadoutDialog(self, event):
        with WeaponLoadoutDialog(self) as dlg:
            dlg.ShowModal()

    

    @staticmethod
    def goWiki():
        webbrowser.open("https://github.com/nikander100/Lootius/tree/dev")
    
    def registerMenu(self):
        menuBar = self.GetMenuBar();
        # Quit
        self.Bind(wx.EVT_MENU, self.ExitApp, id=wx.ID_EXIT)
        # About
        self.Bind(wx.EVT_MENU, self.ShowAboutBox, id=wx.ID_ABOUT)
        # Preference dialog
        self.Bind(wx.EVT_MENU, self.OnShowPreferenceDialog, id=wx.ID_PREFERENCES)
        # Weapon loadout dialog
        self.Bind(wx.EVT_MENU, self.onShowWeaponLoadoutDialog, id=menuBar.weaponLoadoutEditorID)


        # goto Github (gonna  be wiki link but for now repo link)
        self.Bind(wx.EVT_MENU, self.goWiki, id=menuBar.wikiID)


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