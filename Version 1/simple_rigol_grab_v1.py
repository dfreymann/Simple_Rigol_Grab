# dmf 5.6.20 
# simple_rigol_grab_v1
#
# attempt to simplify my usage of rigol_grab (OS X only)
#
# 5.10.20   - version 1, using tkinter for info windows
#           - runs from the command line: python3 simple_rigol_grab.py
#
# configuration: 
#   > rigol connected via known IP address
#   > known IP address and output folder stored in 
#       '~/Library/Application Support/SimpleRigolGrab.json'
#
# functionality: 
#   > grab the image from the rigol
#   > if success, save file to disk and display the image for 5s  
#   > if fail, error message popup
#   > done
#
# in progress:
# the goal is to convert this to an app -> click and done
#
# 5.7.20 working version; need to annotate and fully understand code
# 5.9.20 removing verbose and auto_view arguments; will replace the latter
# with an option button to open the file in an editor (future). 
# # annotated code to try to understand as much as I can for now. 
#
# Limiting its functionality: 
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
#
# 5.11.20 At this point dropped development of this 'Version 1' in 
# order to move from tkinter to PyQt. Further development in the 
# live version of simple_rigol_grab. This 'Version 1' works fine 
# from the command line. 
#  
# ---------
# based on original source - 
# rigol_grab: save Rigol Oscilloscope display as a .png file
# source: https://github.com/rdpoor/rigol-grab
# 

import json         
import subprocess   
import sys          
import tkinter as tk 

# pyvisa is a wrapper for NI-VISA, which must be installed seperately.
# https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#329456
import pyvisa

# use this to work on getting a file timestamp 
from datetime import datetime 

# use this to handle file path
from pathlib import Path 

# Inherit base class called 'object'. Python 2 requires this to define 'new style'
# class; Python 3 this is optional but good practice.  
class RigolGrab(object):

    def __init__(self):

        # as I understand it, these are initialized in __init__ like this to 
        # be globally available to methods within the class, and by convention
        # not accessed from without. 
        self._rigol = None
        self._data = None
        self._resource_manager = pyvisa.ResourceManager()

    # do the things... 
    def grab(self):

        # get the image data from the oscilloscope. method self_rigol() identifies 
        # and opens the ni-visa resource if available. 
        buf = self.rigol().query_binary_values(':DISP:DATA? ON,0,PNG', datatype='B')

        # the filename contains a timestamp only, for now
        filename = self.get_timestamp_file()
        
        # 'wb' here is w - write, b - binary
        with open(filename, 'wb') as f:
            f.write(bytearray(buf))

        # report succesful write and display the image 
        self.report_status(filename)

        # (future) this will be re-configured to respond to an 'edit' button during
        # display (which otherwise times-out and closes) to go directly to editing
        # self.open_file_with_system_viewer(filename)

    # find the device... 
    def rigol(self):
   
        # None keyword is used to define a NULL... None is a datatype 
        # of its own. It is not 'True' or 'False'
        if self._rigol == None:

            inst = 'TCPIP0::{}::INSTR'
            name = inst.format(self.get_IPaddress())

            # open the connection
            try:
                self._rigol = self._resource_manager.open_resource(name, write_termination='\n', read_termination='\n')
            except:
                self.err_out('Could not open oscilloscope')

            # check it's a Rigol
            if ("RIGOL" in self._rigol.query("*IDN?")) is False:
                self.err_out('No RIGOL at that IP address')

        return self._rigol

    # access the IP configuration parameter
    def get_IPaddress(self):
        file_with_address = Path.home() / 'Library/Application Support/SimpleRigolGrab.json' 
        
        # "It is good practice to use the with keyword when dealing with file objects. The 
        # advantage is that the file is properly closed after its suite finishes, even if 
	# an exception is raised at some point. ... if you're not using the with keyword,        
	# then you should call f.close() to close the file and immediately free up any 
        # system resources used by it."
        with open(file_with_address) as json_file:
            self._data = json.load(json_file) 
        
        # 5.7.20 Here, will have to handle exception if this file doesn't exist, and 
        # prompt for input. Also, should check for validity. 

        return(self._data["IP_ADDRESS"])

    # give the output a name...
    def get_timestamp_file(self):
                
        # define the filename, timestamp only, for now
        # (future) add an input to change the descriptor
        datestring = datetime.now().strftime("%m.%d.%y_%H-%M-%S")
        descriptor = 'Rigol-'

        # future: prompt for descriptor here (replace 'Rigol-')
        # will need error checking

        filestring = descriptor + datestring + '.png'
        file_to_write = Path.home() / self.get_folder() / filestring 
        
        return (file_to_write)

    # access the FOLDER configuration parameter
    # (future) could combine with IP_ADDRESS method, and add other parameters
    def get_folder(self):
        
        # 5.7.20 Here, will have to handle exception if this file doesn't exist, and 
        # prompt for input. Also, should check for validity. 

        # for now, this is OK
        return(self._data["FOLDER"])

    # success window displays the image and times-out...  
    def report_status(self, filename):
        NORM_FONT= ("Lucida Grande", 14)

        self.pic = tk.Tk()
        self.pic.title("Simple Rigol Grab")
        
        icon = tk.PhotoImage(file=filename)
        msg = "  " + str(filename) + " has been captured succesfully"
        
        tk.Label(self.pic, image=icon).pack(side="top")
        tk.Label(self.pic, text=msg, font=NORM_FONT).pack(side="left",pady=0)
        tk.Button(self.pic, text="OK", command=self.pic.destroy).pack(side="right", pady=10, padx=15)
        
        # add a timeout
        # why the 'lambda' here? some examples from the internets have this. why?  
        # other examples from the internets do not. 
        self.pic.after(5000, lambda: self.pic.destroy()) # time in ms (so 5000 is 5s)
        self.pic.resizable(0,0)

        self.pic.mainloop()

    # Why is this (@classmethod) decoration used here? 
    # "A class method is a method that is bound to a class rather than its object. 
    # It doesn't require creation of a class instance, much like staticmethod."
    # Note the 'cls' parameter. But I still don't get it. 
    @classmethod
    def open_file_with_system_viewer(cls, filepath):
        subprocess.call(('open', filepath))
  
    # error message and quit... 
    def err_out(self, message):
        self.report_failure(message)
        sys.exit(message + '...quitting')
 
    # error popup and time-out... 
    def report_failure(self, message):
        NORM_FONT= ("Lucida Grande", 14)

        self.popup = tk.Tk()
        self.popup.wm_title("Simple Rigol Grab")
        
        tk.Label(self.popup, font=NORM_FONT, text=message + '...quitting').pack(side="top", padx=10, pady=10)
        b1 = tk.Button(self.popup, text="OK", command=self.popup.destroy)
        # add a timeout
        b1.after(3000, lambda: self.popup.destroy()) # time in ms (so 2000 is 5s)
        b1.pack(pady=10)
        self.popup.eval('tk::PlaceWindow . center')

        self.popup.mainloop()
   
    # shut it down...
    def close(self):
        self._rigol.close()
        self._resource_manager.close()

# the 'program'... 
if __name__ == '__main__':

    grabber = RigolGrab()
    grabber.grab()
    grabber.close()
