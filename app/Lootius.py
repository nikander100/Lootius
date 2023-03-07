#!/usr/bin/env python
import wx
#possibly not needed here
import wx.adv 

"""
    want to do an setup like pyfa does.
    where they have a main frame they import in the app
    so the main app stays nice and clean
"""
if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    from views.app import LootiusApp
    lootius = LootiusApp()
    from views.mainFrame import LootiusFrame
    frm = LootiusFrame()
    frm.Show();
    lootius.MainLoop();
