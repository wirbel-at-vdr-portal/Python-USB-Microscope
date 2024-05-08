# About
This is a Python script for an DNT USB microscope camera. This micrsocope was sold a an 5MPix one, but delivers only a 640x480 25fps stream.
I'm using Python-3.12.0 with OpenCV on Windows. It **should** work with other similar cameras and Linux as well.
This program, and associated information is Open Source (see Licence).

![Screenshot](doc/Screenshot.png)

## Features
- Image scaling using Bicubic interpolation.
- Blur image smoothing (default = off)
- Fullscreen / Windowed mode
- Image rotation in 90deg steps
- Variable Contrast
- Variable Brightness
- Snapshot images
- On Screen menu (default = on), can be turned off

## Dependencies
- Python 3
- OpenCV with v4l (Linux) or MSMF (Windows) or FFMPEG video capture.

NOTE: the version included in mingw64 doesnt include all video capture devices (for example MSMF is missing).

## Running the Program
Run **USB-microscope.py**.

It uses the default camera device, you may need to change it, if more than one video device is available.
If needed, change the line

*dev = 0*

## Using the program
- **ESC** or **q** - end program 
- **+** or **-** - change window size and scale up/down
- **s** - smooth image
- **b** - toggle trough brightness values
- **c** - toggle trough contrast values
- **r** - rotate clockwise in 90deg steps
- **m** - toggle menu
- **CTRL + s** - save snapshot as png
