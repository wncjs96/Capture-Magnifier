from tkinter import *
from pynput import mouse

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
		#TODO Calibrate
		self.bCalibrate = Button(self.frame, text="CALIBRATE", command=self.calibrate)
		self.bShowBorder = Button(self.frame, text="CALIBRATE DONE", command=self.showBorder)
		self.bQuit = Button(self.frame, text="QUIT", command=self.root.quit)

		self.bCalibrate.grid(row=0, column=0)
		self.bShowBorder.grid(row=0, column=1)
		self.bQuit.grid(row=0, column=2)
		
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
			self.bCalibrate['state'] = NORMAL
			#self.delimiter.geometry(f"{self.width}x{self.height}")
			print("width = " + str(self.width) + " height = " + str(self.height))
			return False
		
	def calibrate(self):
		# disable the button during the calibration
		self.bCalibrate['state'] = DISABLED
		#self.root.bind("<ButtonPress-1>", self.getPos)
		#self.root.bind("<ButtonRelease-1>", self.getPos2)
		
		#blocking
		#with mouse.Listener(on_click=self.on_click) as listener:listener.join()
		#nonblocking
		listener = mouse.Listener(on_click=self.on_click)
		listener.start()
		#listener.wait()
		#print('wait done')
	def makeNewFrame(self,top,left,width,height):
		self.delimiter = Tk() 
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
		
	def showBorder(self):
		# instead of making a new frame each time, just show the hidden border
		#self.makeNewFrame(self.top, self.left, self.width, self.height)
		self.delimiter.deiconify()
		self.delimiter.geometry(f"+{self.left}+{self.top}")
		self.delimiter.geometry(f"{self.width}x{self.height}")
		if (self.border.winfo_exists()):
			self.border.pack_forget()
		self.border = Frame(self.delimiter, width=self.width, height=self.height, borderwidth=10, relief=RAISED)
		self.border.configure(background='white')
		self.border.pack_propagate(False)
		self.border.pack()

	def getPos(self,event):
		self.left = event.x
		self.top = event.y
		print("x = "+ str(self.left) +" y = "+ str(self.top))
	def getPos2(self,event):
		self.width = event.x-self.left
		self.height = event.y-self.top
		print("width = " + str(self.width) + "height = " + str(self.height))


def main():
	app = App()
	app.root.mainloop()

	return

if __name__ == "__main__": main()
