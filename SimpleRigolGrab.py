# SimpleRigolGrab.py
# dmf 5.14.20  
# Persistent menu bar GUI to handle grabbing Rigol screen images at will
# 
# Currently runs from the command line 'python3 SimpleRigolGrab' but the 
# goal is to convert this to an app.
#
# 5.6.20    - simple_rigol_grab.py
#             attempt to simplify my usage of rigol_grab (OS X only)
# 5.7.20    - working version; need to annotate and fully understand code
# 5.9.20    - removing verbose and auto_view arguments; will replace the latter
#             with an option button to open the file in an editor (future). 
#             annotated code to try to understand as much as I can for now. 
# 5.10.20   - version 1, using tkinter for info windows
#           - runs from the command line: python3 simple_rigol_grab_v1.py
# 5.11.20   - begin converting from tkinter to PyQt for 
#             informational windows
# 5.12.20   - PyQt GUI setup completed. Running properly from command line. 
# 5.14.20   - Menu bar grabber icon menu implemented. Now handles repeated
#             grab requests, and fails gracefully if can't connect to 
#             instrument. Nice. 
# 
# Files:
#   SimpleRigolGrab.py      - implements grabbermenu menu-bar GUI
#   simple_rigol_grab.py    - implements grabber routines based original rigol_grab code
#   simple_win.py           - implements success and failure popup GUI
#
# Configuration: 
#   > rigol connected via known IP address
#   > known IP address and output folder stored in 
#       '~/Library/Application Support/SimpleRigolGrab.json'
#
# functionality: 
#   > grab the image from the rigol
#   > if success, save file to disk and display the image for 5s  
#   > if fail, error message popup
#
#
# Limited/changed its functionality: 
#  1) IP address only
#  2) Date-time stamp
#  3) Mac OS X only 
#  4) Write image to Desktop
#  5) Read IP address from external file
#  6) Add check that IP has a Rigol at address
#  7) Add dialog announcing what was done - this displays the image
#  7.1) Add announcement if failure, also
#  8) Read target folder (e.g. Desktop) from external file
#  9) Fully annotate 'code for beginners'
#  10) Convert to PyQT GUI from tkinter
#  11) Convert to menu bar handling of 'Grab' and 'Quit'
# To do:
#  12) Update (figure out) LICENSE file and README.md
#  13) Clean up call to imagewin GUI routines 
#  14) Error handling and prompts if external JSON not present
#  15) Prompt for IP if external not available, and write to JSON
#  16) Prompt for target folder if not defined, and write to JSON
#  17) Convert to App
# Someday:  
#  18) Prompt for file descriptor to add to filename 
#  19) Image file to Clipboard? 
#  20) Add an 'edit' button to image window to open in local editor
#  18) ... other? 
#
# ---------
# Copyright (c) 2020 Douglas M Freymann 
#

import sys 
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

# local routines to interact with rigol - 
from simplegrab import *              

class grabbermenu(object):

    def __init__(self):

        # create a Qt application
        self.app = QApplication([])
        # "The default behaviour in Qt is to close an application
        # once all the active windows have closed. Setting
        # `app.setQuitOnLastWindowClosed(False)` stops this and
        #  will ensure your application keeps running."
        self.app.setQuitOnLastWindowClosed(False)

        # Create the menu and set the actions 
        menu = QMenu()
        # Grab
        grabaction = menu.addAction("Grab Rigol")
        grabaction.triggered.connect(lambda: self.grab())
        # or Quit
        exitaction = menu.addAction("Quit")
        exitaction.triggered.connect(lambda: self.app.quit())
        # menu.addAction(exitaction)

        # Create the tray with an icon 
        self.tray = QSystemTrayIcon()
        
        # Notice: if this file is missing the program
        # runs anyway with an invisible 'icon'.
        self.tray.setIcon(QIcon("grabbericon.png"))

        # Add the menu to the tray
        self.tray.setContextMenu(menu)
        self.tray.show()
        
    def start(self):
        
        # Enter Qt application main loop 
        self.app.exec_()
        # and quit when done
        sys.exit()

    def grab(self): 
        # create an instance of the rigol grabber  
        self.grabber = RigolGrab()     
        self.grabber.grab()

if __name__ == "__main__":
    
    app = grabbermenu()
    app.start()

