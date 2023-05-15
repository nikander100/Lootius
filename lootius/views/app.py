import wx
from modules.logParser import ChatLogParser
from modules.combatModule import CombatModule

class LootiusApp(wx.App):
    def OnInit(self):
        self.AppName = "Lootius"
        self.chatLogParser = ChatLogParser(self)
        self.combatModule = CombatModule(self)
        return True