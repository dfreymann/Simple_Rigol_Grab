# simplewin.py 
# dmf 5.12.20
# GUI routines for SimpleRigolGrab 
#
# ---------
# Copyright (c) 2020 Douglas M Freymann 
#

import sys
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtWidgets import QInputDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt

class display_grab_success(object):
    # Wrapper to move PyQt code to one file 
    
    def __init__(self, passedvalue):
        self.filename = passedvalue

    def show(self):
        a = imagewin(self.filename)
        a.displayImage()

class display_grab_failure(object):
    # Wrapper to move PyQt code to one file 

    def __init__(self, passedvalue):
        self.errormsg = passedvalue

     # error popup and time-out... 
    def show(self):
        b = failpopup(self.errormsg).displayPopup()

# reminder for the beginner:  
# everything is in methods and you call them from 
# other methods in the class, or from outside.  
class imagewin(QWidget):
    # Display the captured Rigol image

    def __init__(self, inputval):
        # http://zetcode.com/gui/pyqt5/firstprograms/
        # "The [win] class inherits from the QWidget class. 
        # This means that we call two constructors: the first 
        # one for the Example class and the second one for the 
        # inherited class. The super() method returns the parent
        # object of the Example class and we call its constructor."
        super(imagewin, self).__init__()
        self.filename = str(inputval)
        self.message = "  " + self.filename + " has been captured succesfully"
 
    # test method, not used
    def displaymessage(self):
        print(self.message)

    def displayImage(self): 
        # This is the display of the captured image 
        image = QLabel()
        image.setPixmap(QPixmap(self.filename))
        # This is the OK button to close the window
        bOK = QPushButton('OK')
        bOK.setMaximumWidth(60)
        bOK.setStyleSheet("font: 12pt")

        # need lambda here! if do 'win.close()' only get an error 
        # because? win.close() is type bool. lamba invokes the 
        # win.close() as a function. at least that's what I can 
        # infer so far...
        bOK.clicked.connect(lambda: self.close())
        
        # This is just a text widget reporting status 
        msg = QLabel()
        msg.setText(self.message)
        # Found on the internets:
        msg.setStyleSheet("font: 16pt")

        # This organizes the info text and the OK button 
        # horizontally 
        msg_layout = QHBoxLayout()
        msg_layout.addWidget(msg)
        msg_layout.addStretch
        msg_layout.addWidget(bOK)

        # This sets the vertical layout of the image and 
        # info text/OK button widgets
        imagebox = QVBoxLayout()
        imagebox.addWidget(image)
        imagebox.addLayout(msg_layout)

        # This sets a time-out for the display
        time = QTimer(self)               
        time.setInterval(6000)
        # Need lambda here! 
        time.timeout.connect(lambda: self.close())
        # Need to start it! 
        time.start()

        # This incorporates the layout into the window
        self.setLayout(imagebox)
        self.setWindowTitle("Simple Rigol Grab")

        # This shows and quits when done 
        self.show()

class failpopup(QWidget):
    # Report failure to find Rigol  

    def __init__(self, inputval):
        # http://zetcode.com/gui/pyqt5/firstprograms/
        # "The [win] class inherits from the QWidget class. 
        # This means that we call two constructors: the first 
        # one for the Example class and the second one for the 
        # inherited class. The super() method returns the parent
        # object of the Example class and we call its constructor."
        super(failpopup, self).__init__()
        self.message = inputval
 
    # test method, not used
    def displaymessage(self):
        print(self.message)

    def displayPopup(self): 

        # This is the OK button to close the window
        bOK = QPushButton('OK')
        bOK.setMaximumWidth(60)
        bOK.setStyleSheet("font: 12pt")

        # need lambda here! if do 'win.close()' only get an error 
        # because? win.close() is type bool. lamba invokes the 
        # win.close() as a function. at least that's what I can 
        # infer so far...
        bOK.clicked.connect(lambda: self.close())
        
        bOK_layout = QHBoxLayout()
        bOK_layout.addWidget(bOK)

        # This is just a text widget reporting status 
        msg = QLabel()
        msg.setText(self.message)
        # Found on the internets:
        msg.setStyleSheet("font: 16pt")
        msg.setAlignment(Qt.AlignCenter)

        # This sets the vertical layout of the image and 
        # info text/OK button widgets
        popupbox = QVBoxLayout()
        popupbox.addWidget(msg)
        popupbox.addLayout(bOK_layout)

        # This sets a time-out for the display
        time = QTimer(self)               
        time.setInterval(3000)
        # Need lambda here! 
        time.timeout.connect(lambda: self.close())
        # Need to start it! 
        time.start()

        # This incorporates the layout into the window
        self.setLayout(popupbox)
        self.setWindowTitle("Simple Rigol Grab")
        
        # This shows and quits when done 
        self.show()

class get_descriptor(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Simple Rigol Grab"

    def get(self):
        text, okPressed = QInputDialog.getText(self, "Filename","Enter a short descriptor:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return(text)
        else:
            return("Rigol")


