import numpy as np
import cv2
from mss import mss
from PIL import Image
# There's no native way of handling the feature of getting the window "always on top"
# It's OS dependent forcing it to not be cross platform
# -> this is a windows way of handling things. Marked with TODOs
import os 

# signals and signal handlers for garbage collection -> obsolete as there's an easier solution with a shared variable
# import signal


# shared_flag shared by multiple threads
#shared_flag = 0

class SCR():
	# class var
	arr = [0] * 4
	bounding_box = {'top': 0, 'left': 0, 'width': 1000, 'height': 1000}
	
	# To keep up with the active monitors, array elements are used as placeholders for each active screen


	def __init__(self):
		self.sct = mss()
	def setVar(self,top,left,width,height):
		self.bounding_box={'top':top,'left':left,'width':width,'height':height}	
	def run(self, name):
		if (self.arr[int(name[6])] == 0):
			print(name[6] + "\'th bucket got filled up !")
			self.arr[int(name[6])] = 1
			while True:
				sct_img = self.sct.grab(self.bounding_box)
	
				cv2.namedWindow(name, cv2.WINDOW_NORMAL|cv2.WINDOW_KEEPRATIO)
				
				#TODO: resizing upon wheel input
				#TODO: fix for cross-platform
				#os.system('''/usr/bin/osascript -e 'tell app "finder" to set frontmost of process "python" to true' ''') 
				

				# set the window FULL SCREEN then back to NORMAL - might be cross platform
			
			#	cv2.waitKey(1)
			#	
			#	cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
			#	cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
	
				#cv2.resizeWindow('screen', 600,600)
				cv2.imshow(name, np.array(sct_img))
				
				#time.sleep(1)
	
				if (cv2.waitKey(1) & 0xFF) == ord('q'):
					self.arr[int(name[6])] = 0
					cv2.destroyAllWindows()
					break
					
	def demolish(self):
		cv2.destroyAllWindows()
	
	
	


