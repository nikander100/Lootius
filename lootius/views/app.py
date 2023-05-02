import wx
from modules.logParser import ChatLogParser

class LootiusApp(wx.App):
    def OnInit(self):
        self.AppName = "Lootius"
        self.chatLogParser = ChatLogParser(self)
        return True