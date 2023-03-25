#!/usr/bin/env

"""
    want to do an setup like pyfa does.
    where they have a main frame they import in the app
    so the main app stays nice and clean
"""
if __name__ == '__main__':

    """first precheck (all thins here)
    second set errorhandling
    third read and load config, do we want to use py-fa or lootnan way of config
    on first load setup databases"""
    import wx
    #possibly not needed here
    import wx.adv 
    import sys
    from os.path import realpath, join, dirname, abspath
    from os import path

    from database import db
    from models.databaseModel import WeaponTypes

    # Setup Db
    dbPath = realpath(join(dirname(abspath(__file__)), "./database/", "lootiusTest.db"))
    if path.exists(dbPath) == False:
        db.Setup.run(dbPath)
    else:
        print("path exists")
    Session = db.DB.getSession()
    # with Session.begin() as session:
    #     tmp = WeaponTypes()
    #     tmp.type = "testing"
    #     session.add(tmp)


    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    from views.app import LootiusApp
    lootius = LootiusApp()
    from views.mainFrame import LootiusFrame
    frm = LootiusFrame()
    frm.Show();
    lootius.MainLoop();