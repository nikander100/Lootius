import wx
import wx.adv 
import webbrowser

from views.mainMenuBar import mainMenuBar
from views.preferenceDialog import PreferenceDialog
from views.weaponLoadoutDialog import WeaponLoadoutDialog


"""
TODO Add min size for frame
"""
class LootiusFrame(wx.Frame):

    def __init__(self, app, title="Lootius", size=(320, 160, 1280, 720)):
        # ensure the parent's __init__ is called
        self.title = title
        super().__init__(None, wx.ID_ANY, self.title)
        self.app = app
        self.Size = size
        self.SetBackgroundColour(wx.Colour(30,30,30))

        # Modules
        # self.chatLogParser = ChatLogParser(self)
        self.chatLogParser = self.app.chatLogParser
        # self.app.chatLogParser...

        # create a panel in the frame
        # pnl = wx.Panel(self);
        # pnl.SetBackgroundColour(wx.Colour(30,30,30))

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        self.sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Quick Stats"), wx.VERTICAL)
        #tmp
        buttonReset = wx.Button(self, wx.NewId(), "Reset Database")
        self.Bind(wx.EVT_BUTTON, self.resetDb, id=buttonReset.GetId())
        #end tmp
        self.sizer_3.Add(buttonReset, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        self.sizer_3.Add((0, 0), 0, 0, 0)
        self.sizer_3.Add((0, 0), 0, 0, 0)
        self.sizer_3.Add((0, 0), 0, 0, 0)
        self.sizer_3.Add((0, 0), 0, 0, 0)
        self.panel_3 = wx.Panel(self, wx.ID_ANY)
        sizer_2.Add(self.sizer_3, 1, wx.BOTTOM | wx.EXPAND | wx.LEFT, 5)
        sizer_2.Add(self.panel_3, 1, wx.EXPAND, 0)

        self.mainFrameSwitcher = wx.Notebook(self, wx.ID_ANY)

        self.panel_2 = wx.Panel(self.mainFrameSwitcher, wx.ID_ANY)
        self.mainFrameSwitcher.AddPage(self.panel_2, "notebook_2_pane_1")
        self.mainFrameSwitcher_Tables = wx.Panel(self.mainFrameSwitcher, wx.ID_ANY)
        self.mainFrameSwitcher.AddPage(self.mainFrameSwitcher_Tables, "Tables")
        self.mainFrameSwitcher_pane_1 = wx.Panel(self.mainFrameSwitcher, wx.ID_ANY)
        self.mainFrameSwitcher.AddPage(self.mainFrameSwitcher_pane_1, "Graphs")
        self.mainFrameSwitcher_pane_2 = wx.Panel(self.mainFrameSwitcher, wx.ID_ANY)
        self.mainFrameSwitcher.AddPage(self.mainFrameSwitcher_pane_2, "Detailed Stats")
        self.mainFrameSwitcher_Page2 = wx.Panel(self.mainFrameSwitcher, wx.ID_ANY)
        self.mainFrameSwitcher.AddPage(self.mainFrameSwitcher_Page2, "...")


        mainSizer.Add(sizer_2, 1, wx.EXPAND, 0)
        mainSizer.Add(self.mainFrameSwitcher, 3, wx.ALL | wx.EXPAND, 5)
        

        self.SetSizer(mainSizer)
        # self.Layout()


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
        from database.db import LocalSession
        from models.databaseModel import WeaponLoadout

        # with e() as ses:
        #     lol = ses.query(WeaponLoadout).filter(WeaponLoadout.name == "test").first()
        #     for enahncer in lol.enhancerLoadout:
        #         print (enahncer.enhancerClassID, enahncer.socket)
        #     ses.delete(lol)
        #     ses.commit()
        # return

        # from modules import loadoutManager
        # loadout = LocalSession.query(WeaponLoadout).filter_by(name="test").first()
        # print("\n\n\n\n\n\n\n\n\n\n",loadoutManager.getCostPerShot(loadout))
        # return
    
        from os.path import realpath, join, dirname, abspath
        dbPath = realpath(join(dirname(abspath(__file__)), "../database/", "lootiusTest.db"))

        db.dropAll()
        print("\n\n\nDeleted DATABASE\n\n\n")
        sleep(1.2)
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
    def goWiki(self):
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