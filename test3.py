import tkinter as tk
from PIL import ImageGrab,ImageTk
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(2) # windows 10

class ToolWin(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self._offsetx = 0
        self._offsety = 0
        self.wm_attributes('-topmost',1)
        self.penSelect = tk.BooleanVar()
        self.overrideredirect(1)
        self.geometry('200x200')
        self.penModeId = None
        self.bind('<ButtonPress-1>',self.clickTool) 
        self.bind('<B1-Motion>',self.moveTool) # bind move event

        draw = tk.Checkbutton(self,text="Pen",command=self.penDraw,variable=self.penSelect)
        draw.pack()
        cancel = tk.Button(self,text="Quit",command=root.destroy)
        cancel.pack()

    def moveTool(self,event):
        self.geometry("200x200+{}+{}".format(self.winfo_pointerx()-self._offsetx,self.winfo_pointery()-self._offsety))

    def clickTool(self,event):
        self._offsetx = event.x
        self._offsety = event.y

    def penDraw(self):
        if self.penSelect.get():
            self.penModeId = root.bind("<B1-Motion>",Draw)
        else:
            root.unbind('<B1-Motion>',self.penModeId)

def Draw(event):# r = 3
    fullCanvas.create_oval(event.x-3,event.y-3,event.x+3,event.y+3,fill="black")

def showTool(): # the small tool window
    toolWin = ToolWin()
    toolWin.mainloop()

root = tk.Tk()
root.state('zoomed')
root.overrideredirect(1)

fullCanvas = tk.Canvas(root)
background = ImageTk.PhotoImage(ImageGrab.grab(all_screens=True)) # show the background,make it "draw on the screen".
fullCanvas.create_image(0,0,anchor="nw",image=background)
fullCanvas.pack(expand="YES",fill="both")

root.after(100,showTool)

root.mainloop()