import numpy as np
import cv2
import tkinter
from PIL import Image as Img
from PIL import ImageTk
from mss import mss
import time

class SCR():
	# class var
	arr = [0] * 4
	bounding_box = {'top': 0, 'left': 0, 'width': 1000, 'height': 1000}
	sct = mss()
	root = tkinter.Tk()
	# A root window for displaying objects
	
	# To keep up with the active monitors, array elements are used as placeholders for each active screen
	#def __init__(self):
		#self.sct = mss()
		#self.root = root
	def setVar(self,top,left,width,height):
		self.bounding_box={'top':top,'left':left,'width':width,'height':height}	
	def run(self, name):
		if (self.arr[int(name[6])] == 0):
			print(name[6] + "\'th bucket got filled up !")
			self.arr[int(name[6])] = 1
			while True:
				sct_img = self.sct.grab(self.bounding_box)
				img = np.array(sct_img)
				#color channel setup
				b,g,r,p = cv2.split(img)
				img = cv2.merge((r,g,b))
				
				im = Img.fromarray(img)
				imgtk = ImageTk.PhotoImage(image=im)
				print('gets here')	
				tkinter.Label(self.root, image=imgtk).pack()
				self.root.mainloop()	
				time.sleep(1)
			
				if (cv2.waitKey(1) & 0xFF) == ord('q'):
					self.arr[int(name[6])] = 0
					self.root.quit()
					break
					
	def demolish(self):
		# destroys all the windows active
		shared_flag = 1
		print("Shared flag : " + str(shared_flag))
		cv2.destroyAllWindows()
	
def main():
	app = SCR()
	app.run('screen0')
	#app.root.mainloop()
	exit(0)

if __name__ == "__main__" : main()

