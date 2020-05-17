# simple_rigol_grab.py
# dmf 5.6.20 
# Grabber routines for SimpleRigolGrab
#  
# ---------
# Copyright (c) 2019 Robert Poor
# Copyright (c) 2020 Douglas M Freymann 
# 
# Based on original source - 
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

# local library implementing simple PyQT GUI handling:
#   imagewin(the_filename).displayImage()       - display the succesfully retreived image
#   failpopup(failure_message).displayPopup()   - notify of failure to find the rigol 
from simple_win import *

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

        instrument = self.rigol()
        if (instrument == None):
            # failed to open
            return
        else:
            # success! 
            buf = instrument.query_binary_values(':DISP:DATA? ON,0,PNG', datatype='B')

        # the filename contains a timestamp only, for now
        filename = self.get_timestamp_file()
        
        # 'wb' here is w - write, b - binary
        with open(filename, 'wb') as f:
            f.write(bytearray(buf))

        # report succesful write and display the image 
        c = display_grab_success(filename).show()

        # (future) this will be re-configured to respond to an 'edit' button during
        # display (which otherwise times-out and closes) to go directly to editing
        # self.open_file_with_system_viewer(filename)

        self.close()

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
                return self._rigol

            # check it's a Rigol
            if ("RIGOL" in self._rigol.query("*IDN?")) is False:
                # something was found, but not a Rigol
                self._rigol = None
                self.err_out('No RIGOL at that IP address')

        return self._rigol

    # access the IP configuration parameter
    def get_IPaddress(self):
        
        file_with_address = Path.home() / 'Library/Application Support/simple_rigol_grab.json' 
        
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

    # Why is this (@classmethod) decoration used here? 
    # "A class method is a method that is bound to a class rather than its object. 
    # It doesn't require creation of a class instance, much like staticmethod."
    # Note the 'cls' parameter. But I still don't get it. 
    @classmethod
    def open_file_with_system_viewer(cls, filepath):
        subprocess.call(('open', filepath))
  
    # error message and quit... 
    def err_out(self, message):
        d = display_grab_failure(message).show()
   
    # close down after succesful open
    def close(self):
        self._rigol.close()
        self._resource_manager.close()

