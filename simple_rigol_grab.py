# dmf 5.6.20 
# simple_rigol_grab
# 
# attempt to simplify my usage of rigol_grab
# IP address is stored in ~/Library/Application Support/SimpleRigolGrab.json'
#
# 5.7.20 working version; need to annotate and fully understand code
#
# limiting its functionality: 
#  1) IP address only
#  2) Date-time stamp
#  3) Mac OS X only 
#  4) Write image to Desktop
#  5) Read IP address from external file
#  6) Add check that IP has a Rigol at address
#  7) Add dialog announcing what was done - this displays the image
#  7.1) Add announcement if failure, also
#  8) Read target folder (e.g. Desktop) from external file
# To do:
#  - 
#  9) Fully annotate 'code for beginners'
#  10) Convert to App
#  11) Convert to menubar App (only?)
# Future:  
#  -
#  12) Prompt for file descriptor to add to filename 
#  13) Image file to Clipboard? 
#  14) Prompt for IP if external not available, and write to JSON
#  15) Prompt for target folder if not defined, and write to JSON
#  16) ... other? 
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


class RigolGrab(object):

    def __init__(self, verbose=False):
        self._verbose = verbose
        self._rigol = None
        self._resource_manager = pyvisa.ResourceManager()

    def grab(self, filename='rigol.png', auto_view=True):

        buf = self.rigol().query_binary_values(':DISP:DATA? ON,0,PNG', datatype='B')

        with open(filename, 'wb') as f:
            self.verbose_print('Capturing screen to', filename)
            f.write(bytearray(buf))

        self.report_status(filename)

        if auto_view:
            self.open_file_with_system_viewer(filename)

    def rigol(self):
   
        if self._rigol == None:

            inst = 'TCPIP0::{}::INSTR'
            name = inst.format(self.get_IPAddress())

            self.verbose_print('Opening', name)
            try:
                self._rigol = self._resource_manager.open_resource(name, write_termination='\n', read_termination='\n')
            except:
                self.err_out('Could not open oscilloscope')

            self.check_for_rigol()

        return self._rigol

    def check_for_rigol(self): 

        if ("RIGOL" in self.rigol().query("*IDN?")) is False:
            self.err_out('No RIGOL at that IP address')

    def get_timestamp_file(self):
        
        datestring = datetime.now().strftime("%m.%d.%y_%H-%M-%S")
        descriptor = 'Rigol-'

        # future: prompt for descriptor here (replace 'Rigol-')
        # will need error checking

        filestring = descriptor + datestring + '.png'
        file_to_write = Path.home() / self.get_folder() / filestring 
        
        return (file_to_write)

    def verbose_print(self, *args):
        if (self._verbose): print(*args)

    def err_out(self, message):
        self.report_failure(message)
        sys.exit(message + '...quitting')

    def close(self):
        self._rigol.close()
        self._resource_manager.close()

    @classmethod
    def open_file_with_system_viewer(cls, filepath):
        subprocess.call(('open', filepath))

    def get_IPAddress(self):
        file_with_address = Path.home() / 'Library/Application Support/SimpleRigolGrab.json' 
        
        # "It is good practice to use the with keyword when dealing with file objects. The 
        # advantage is that the file is properly closed after its suite finishes, even if 
        # an exception is raised at some point. ... If you’re not using the with keyword, 
        # then you should call f.close() to close the file and immediately free up any 
        # system resources used by it."
        with open(file_with_address) as json_file:
            data = json.load(json_file) 
        
        # 5.7.20 Here, will have to handle exception if this file doesn't exist, and 
        # promptfor input. Also, should check for validity. 

        return(data["IP_ADDRESS"])

    def get_folder(self):
        # 5.7.20 This is redundent with get_IPAddress, but OK for now. 
        file_with_folder = Path.home() / 'Library/Application Support/SimpleRigolGrab.json' 
        
        with open(file_with_folder) as json_file:
            data = json.load(json_file) 
        
        # 5.7.20 Here, will have to handle exception if this file doesn't exist, and 
        # prompt for input. Also, should check for validity. 

        return(data["FOLDER"])


    def report_failure(self, message):
        NORM_FONT= ("San Francisco", 12)

        self.popup = tk.Tk()
        self.popup.wm_title("Simple Rigol Grab")
        
        tk.Label(self.popup, font=NORM_FONT, text=message + '...quitting').pack(side="top", padx=10, pady=10)
        b1 = tk.Button(self.popup, text="OK", command=self.popup.destroy)
        # add a timeout
        b1.after(3000, lambda: self.popup.destroy()) # time in ms (so 2000 is 5s)
        b1.pack(pady=10)
        self.popup.eval('tk::PlaceWindow . center')

        self.popup.mainloop()


    def report_status(self, filename):
        NORM_FONT= ("San Francisco", 12)
        
        self.pic = tk.Tk()
        self.pic.title("Simple Rigol Grab")
        
        icon = tk.PhotoImage(file=filename)
        msg = "  " + str(filename) + " has been captured succesfully"
        
        tk.Label(self.pic, image=icon).pack(side="top")
        tk.Label(self.pic, text=msg, font=NORM_FONT).pack(side="left",pady=0)
        tk.Button(self.pic, text="OK", command=self.pic.destroy).pack(side="right", pady=10, padx=15)
        
        # add a timeout
        self.pic.after(5000, lambda: self.pic.destroy()) # time in ms (so 5000 is 5s)
        self.pic.resizable(0,0)

        self.pic.mainloop()

if __name__ == '__main__':

    grabber = RigolGrab(verbose=False)
    grabber.grab(grabber.get_timestamp_file(), auto_view=False)
    grabber.close()
