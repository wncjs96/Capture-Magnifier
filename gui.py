from tkinter import *
from pynput import mouse
from PIL import ImageGrab, ImageTk
import cvSCR as scr

#TODO: remove time (only for debugging)
import time

import threading
import logging

# GUI
# state 2 =>
# State 1:
# Button to capture screen + zoom
# Button to hide border
# Button to exit
# State 2:
# Button to Go back
# Button to hide border

class App():
	# class var
	top = 0
	left = 0
	width = 100
	height = 100
	boolBorder = False
	cap = scr.SCR()
	counter = 0
	# initializer, constructor
	def __init__(self):
		self.root = Tk()
		self.root.overrideredirect(1)
		#title
		self.root.title('Screen Capture')
		#ico
		self.root.iconbitmap('assets/SCR.ico')
		#preset
		self.root.attributes('-topmost', True)
		#geometry
		self.root.geometry(f"+{500}+{500}")
		#transparency
		self.root.wm_attributes('-transparentcolor', "white")
		
		#drag and move
		self.grip = Label(self.root, bitmap="gray25",bg='#282a2e')	
		self.grip.pack(side="top", fill="both")
		self.grip.bind("<ButtonPress-1>", self.start_move)
		self.grip.bind("<ButtonRelease-1>", self.stop_move)
		self.grip.bind("<B1-Motion>", self.do_move)
		
		self.frame = Frame(self.root, width=480, height=850, borderwidth=10, relief=RAISED)
		self.frame.configure(background='#1b2940')
		self.frame.pack_propagate(False)
		self.frame.pack()
		#Calibration to set up the bounding box for screen capturing
		self.bCalibrate = Button(self.frame, text="CALIBRATE", command=self.calibrate)
		self.bBetterCalibrate = Button(self.frame, text="Better Calibrate", command=self.makeNewCanvas)
		self.bShowBorder = Button(self.frame, text="Show Area", command=self.showBorder)
		self.bShowSCR = Button(self.frame, text="Show Capture", command=self.showSCR)
		self.bQuit = Button(self.frame, text="QUIT", command=self.quitroot)
		
		# keybinds for hotkeys
		# showSCR bind to a keyboard, TODO: remove this 
		self.root.bind("<Key-Delete>", lambda x: self.showSCR())

		self.bCalibrate.grid(row=0, column=0)
		self.bShowBorder.grid(row=0, column=1)
		self.bBetterCalibrate.grid(row=0, column=2)
		self.bShowSCR.grid(row=0, column=3)
		self.bQuit.grid(row=0, column=4)

		# explanation of each button (Label area)
		
		#self.tCalibrate = Label(self.frame, text="")
		self.tBetterCalibrate = Label(self.frame, text="BetterCalibrate has a fewer bugs but only works on the primary monitor for this version.", relief=RAISED)
		#self.tCalibrate.grid(row=1, column=0, columnspan=4)
		self.tShowCapture = Label(self.frame, text="DEL, Q for Show Capture")
		self.tBetterCalibrate.grid(row=2, column=0, columnspan=5)
		self.tShowCapture.grid(row=3, column=0, columnspan=5)
		
		# Clock for elapsed time (TODO: to be more sophisticated later)
		

		# There's an actual window hiding later used for calibration
		self.makeNewFrame(self.top, self.left, self.width, self.height)
		self.delimiter.withdraw()
	# instance methods
	def start_move(self, event):
		self.root.x = event.x
		self.root.y = event.y
	def stop_move(self, event):
		self.root.x = None
		self.root.y = None
	def do_move(self, event):
		deltax = event.x - self.root.x
		deltay = event.y - self.root.y
		x = self.root.winfo_x() + deltax
		y = self.root.winfo_y() + deltay
		self.root.geometry(f"+{x}+{y}")
	
	def on_click(self, x,y,button,pressed):
		print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x,y)))
		if pressed:
			self.left = x
			self.top = y
			#self.delimiter.deiconify()
			#self.delimiter.geometry(f"+{x}+{y}")
			#self.showBorder()
			print("x = "+ str(self.left) +" y = "+ str(self.top))
		else:
			# Stop listener
			self.width = x-self.left
			self.height = y-self.top
			#self.bCalibrate['state'] = NORMAL
			#self.delimiter.geometry(f"{self.width}x{self.height}")
			print("width = " + str(self.width) + " height = " + str(self.height))		
			self.cap.setVar(self.top,self.left,self.width,self.height)
			return False
		
	def calibrate(self):
		# disable the button during the calibration
		if (self.boolBorder == True):
			self.boolBorder = not self.boolBorder
			self.delimiter.withdraw()
		#self.bCalibrate['state'] = DISABLED
		
		#blocking 
		#with mouse.Listener(on_click=self.on_click) as listener:listener.join()
		#nonblocking - tkinter and pynput not compatible as they both handle user inputs.
		#solution - use start() to make it run along the main thread.
		#possible error- run time: main thread is not in main loop
		listener = mouse.Listener(on_click=self.on_click)
		listener.start()
		try:
			listener.join()	
		finally:
			listener.stop()
		#try..finally.
		#listener.wait()
		#listener.stop()	

	def makeNewFrame(self,top,left,width,height):
		self.delimiter = Toplevel() 
		self.delimiter.overrideredirect(1)
		#title
		self.delimiter.title('Delimiter')
		#ico
		self.delimiter.iconbitmap('assets/SCR.ico')
		#preset
		self.delimiter.attributes('-topmost', True)
		#geometry
		#self.delimiter.geometry(f"+{left}+{top}")
		#transparency
		self.delimiter.wm_attributes('-transparentcolor', "white")
		self.border = Frame(self.delimiter)
		#self.border = Frame(self.delimiter, width=width, height=height, borderwidth=10, relief=RAISED)
		#self.border.configure(background='white')
		#self.border.pack_propagate(False)
		#self.border.pack()
	
	def makeNewCanvas(self):
		if (self.boolBorder == True):
			self.boolBorder = not self.boolBorder
			self.delimiter.withdraw()
		self.delimiter2 = Toplevel()
		self.delimiter2.state('zoomed')
		self.delimiter2.overrideredirect(1)
		self.delimiter2.attributes('-topmost', True)
		self.delimiter2.wm_attributes('-transparentcolor', "blue")
		self.fullCanvas = Canvas(self.delimiter2)
		# gray-ish color
		capture = ImageGrab.grab(all_screens=True)
		background = ImageTk.PhotoImage(capture.point(lambda x: x*0.3))
		canvasImage = self.fullCanvas.create_image(0,0,anchor="nw",image=background)
		self.fullCanvas.pack(expand="YES", fill="both")
		#self.fullCanvas.pack()
		rect = self.fullCanvas.create_rectangle(0,0,0,0, outline='white')
		# upon drag, the rectangular shape to get the certain part
		self.fullCanvas.bind('<ButtonPress-1>', lambda event: self.getLeftTop(event, rect))
		self.fullCanvas.bind('<B1-Motion>', lambda event: self.renderRect(event, rect, canvasImage, capture))
		self.fullCanvas.bind('<ButtonRelease-1>', self.getWidthHeight)
		
		self.delimiter2.mainloop()
		self.delimiter2.destroy()

	def getLeftTop(self, event, rect):
		self.left = event.x
		self.top = event.y
		self.fullCanvas.coords(rect,event.x,event.y, event.x, event.y)
		print("x = "+ str(self.left) +" y = "+ str(self.top))

	def getWidthHeight(self, event):
		# Stop listener
		self.width = event.x-self.left
		self.height = event.y-self.top
		
		if (self.width < 0) :
			temp = self.left
			self.left = self.width*-1
			self.width = temp
		if (self.height < 0) :
			temp = self.top
			self.top = self.height*-1
			self.height = temp
		#self.delimiter.geometry(f"{self.width}x{self.height}")
		print("left = " +str(self.left)+" top = "+str(self.top) +" width = " + str(self.width) + " height = " + str(self.height))
		self.delimiter2.quit()
		self.cap.setVar(self.top, self.left, self.width, self.height)

	def renderRect(self, event, rect, canvasImage,capture):
		x,y = event.x, event.y
		self.fullCanvas.coords(rect, self.left,self.top,x,y)
		self.fullCanvas.itemconfig(rect, fill='blue')
	#	background = ImageTk.PhotoImage(capture)
	#	self.fullCanvas.create_image(0,0,anchor="nw",image=background)
	#	self.fullCanvas.pack(expand="YES", fill="both")
		
	def showBorder(self):
		# instead of making a new frame each time, just show the hidden border
		#self.makeNewFrame(self.top, self.left, self.width, self.height)
		self.boolBorder = not self.boolBorder
		if (self.boolBorder == True):
			self.delimiter.deiconify()
			self.delimiter.geometry(f"+{self.left}+{self.top}")
			self.delimiter.geometry(f"{self.width}x{self.height}")
			if (self.border.winfo_exists()):
				self.border.pack_forget()
			self.border = Frame(self.delimiter, width=self.width, height=self.height, borderwidth=10, relief=GROOVE, bd=1)
			self.border.configure(background='white')
			self.border.pack_propagate(False)
			self.border.pack()
		else:
			self.delimiter.withdraw()
	
	def quitroot(self):
		# TODO: end the threads (range screen 1..4)
		self.cap.demolish()	
		# quit and destroy
		self.root.quit()
		# destroy for garbage collection and remove dependencies
		#self.root.destroy()


	def showSCR(self):
		#repeat run till a signal is sent
		#another thread to run separately so that you can move the original panel
		#TODO: for normal computer, figure out how many monitors that can be handled by general purpose processors
		# For testing purposes, only 4 to be added
		name = "screen" + str(self.counter % 4)

		scrThread = threading.Thread(target=self.cap.run, args=(name,))
		
		#solution - use start() to make it run along the main thread.
		scrThread.start()

		self.counter = self.counter + 1
		print("name : "+ name + " Counter : " + str(self.counter))
		
		#TODO : multi screens for capturing
		#solution : use classes for each monitors

	def test(self):
		print("key pressed detected")
	
	def thread_function(name):
		logging.info("Thread %s: starting", name)
		time.sleep(2)
		logging.info("Thread %s: finishing", name)		
	
	

#	def getPos(self,event):
#		self.left = event.x
#		self.top = event.y
#		print("x = "+ str(self.left) +" y = "+ str(self.top))
#	def getPos2(self,event):
#		self.width = event.x-self.left
#		self.height = event.y-self.top
#		print("width = " + str(self.width) + "height = " + str(self.height))


def main():
	app = App()
	app.root.mainloop()
	exit(0)

if __name__ == "__main__": main()
