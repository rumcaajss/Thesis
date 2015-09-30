#!/usr/bin/python
#-*- coding: iso-8859-1 -*-

import Tkinter
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

MATRIX = [[1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'*', 'D']]
ROW = [17,27,22,10]
COL = [25,8,7,1]
for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j],1)
for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
def checkButton():
	try:
		while(True):
			for j in range(4):
				GPIO.output(COL[j],0)
				for i in range(4):
					if GPIO.input(ROW[i])==0:
						return MATRIX[i][j]
						time.sleep(0.2)
						while(GPIO.input(ROW[i])==0):
							pass
				GPIO.output(COL[j],1)
	except KeyboardInterrupt:
		GPIO.cleanup()

pressed = checkButton()

class simpleapp(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent=parent
        self.initialize()

    def initialize(self):
	self.grid()
	self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here")
        button = Tkinter.Button(self,text=u"Click",command=self.OnButtonClick)
        button.grid(column=1,row=0)
	self.labelVariable = Tkinter.StringVar()
        label=Tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2, sticky='EW')
        self.labelVariable.set(pressed)

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        
    def OnButtonClick(self):
        self.labelVariable.set(self.entryVariable.get()+"(You clicked)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        
    def OnPressEnter(self,event):
        self.labelVariable.set(self.entryVariable.get()+"(you entered)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)

if __name__=="__main__":
    app = simpleapp(None)
    app.title('my app')
    app.mainloop()
    



    
