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



class simpleapp(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent=parent
        self.initialize()

    def initialize(self):
		self.grid()
		self.mashVariable = Tkinter.StringVar()
		mash=Tkinter.Label(self,textvariable=self.mashVariable,anchor="w",fg="white",bg="green")
		mash.grid(column=0,row=0,columnspan=20, sticky='EW')
		self.brewVariable = Tkinter.StringVar()
		brew=Tkinter.Label(self,textvariable=self.brewVariable,anchor="w",fg="white",bg="green")
		brew.grid(column=0,row=1,columnspan=20, sticky='EW')
		self.mashVariable.set('Press A to start mashing')
		self.brewVariable.set('Press B to start brewing')
	
		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,False)
		self.update()
        #self.geometry(self.geometry())
		self.geometry('400x200+30+40')
        
    def OnButtonClick(self):
        self.mashVariable.set(self.entryVariable.get()+"(You clicked)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        
    def OnPressEnter(self,event):
        self.mashVariable.set(self.entryVariable.get()+"(you entered)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)

if __name__=="__main__":
	app = simpleapp(None)
	app.title('Brew wizard')
	app.mainloop()




    
