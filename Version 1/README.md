# simple_rigol_grab

An attempt to simplify usage of rigol_grab (_OS X only_) to grab images from my Rigol DS1054Z oscilloscope.

Plus, learn Python.

Version 1 is implemented using tkinter to show info windows. However, there's a problem when trying to convert to an app on Mac OSX 10.14.6 (see 'py2app_try_notes.txt'), so as far as converting to an app, I'm SOL for now. This version can be used from the command line and works just fine.

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

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Origin

Originating from the code for rigol-grab by Robert Poor
