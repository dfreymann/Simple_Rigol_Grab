# simple_rigol_grab

An attempt to simplify usage of rigol_grab (_OS X only_) to grab images from my Rigol DS1054Z oscilloscope.

[TO BE REVISED!]

Short version

* originally using tkinter, but problems... so, 'Version 1'.

* will now split to using PyQT... so, ''Version 2'.  This is because I want the end product to be either an app (click and run) or a menu bar app.

## Configuration

* Rigol connected to ethernet with known IP address

* Known IP address and output folder stored in
  
       '~/Library/Application Support/SimpleRigolGrab.json'

## Functionality

python3 simple_rigol_grab.py

* Grab the image from the rigol
* If success,
  * save a .png image file to disk, and
  * display the image on the screen for 5s  
* If fail,
  * error message popup
* Done

## In progress

* The goal is to convert this to an app -> _click and done_
