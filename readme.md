# Capture-Magnifier

The users can decide a part of the screen that's going to be captured and rendered real time, and then they can zoom in and out of the screen on a separate window.

## Installation: 

This project recommends Python 3.7 or higher.

## Prerequisites:
Tkinter: pip install tkinter
Pillow: python -m pip install --upgrade Pillow
mss: python -m pip install -U --user mss
numpy: python -m pip install --upgrade numpy
opencv: python -m pip install --upgrade opencv-python
pynput: python -m pip install --upgrade pynput

## Work

A screenshot taken by mss is processed by numpy and cv to make an array of pixels, then it's processed manually by me, outputting the result afterwards.
The whole thing is wrapped by tkinter, the graphical interface. Pynput is used to interact with users.


## License
[MIT](https://choosealicense.com/licenses/mit/)
