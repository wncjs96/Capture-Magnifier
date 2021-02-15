from mss import mss

# Buttons for monitors, + Full monitor .. 
# Pick a monitor -> Select region, Resizeable window to capture screen, mouse wheel to magnify

# Functionally, Screen capture, save it as png, then resize

#with mss() as sct:
#    sct.shot()

sct = mss()
filename = sct.shot(mon=-1, output='fullscreen.png')
print(filename)
