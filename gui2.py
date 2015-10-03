#!/usr/bin/python
#-*- coding: utf-8 -*-
from Tkinter import *
#import Tkinter as tk
from temp_read import * 
import RPi.GPIO as GPIO
#import thread
LARGE_FONT= ("Verdana", 12)
temperatura=0
temperatura2=0
zmierzona_temp=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)

class Start():
    def __init__(self, master, *args, **kwargs):
        #__init__(self, *args, **kwargs)
        container = Frame(master, width=400,height=400)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, Mashing):
			frame = F(container, self)		
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")
			self.show_frame(StartPage)
			
			
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(Frame):
    def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		self.controller=controller
		label = Label(self, text="Start Page", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		button = Button(self, text="Press to start mashing")
		button.bind("<Return>",lambda event: controller.show_frame(PageOne))
		button.pack()
		button.focus_set()
		button2 = Button(self, text="Press to start brewing")
		button2.bind("<Return>",lambda event: controller.show_frame(PageTwo))
		button2.pack()
 
class PageOne(Frame):
    def __init__(self, parent, controller):
		self.controller=controller
		Frame.__init__(self, parent)
		label = Label(self, text="Mashing", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		
		label2=Label(self, text="First rest temperature")
		label2.pack()
		self.temp_var = IntVar()
		self.temp1= Entry(self, textvariable=self.temp_var)
		self.temp1.pack()
		self.temp1.focus_force()
		self.temp1.selection_range(0, END)			
		self.temp1.bind("<Return>", self.FirstTemp)
		
		label3=Label(self, text="First rest time")
		label3.pack()
		self.time_var = IntVar()
		self.time1= Entry(self, textvariable=self.time_var)
		self.time1.pack()
		self.time1.selection_range(0, END)			
		self.time1.bind("<Return>", self.FirstTime)
		
		label4=Label(self, text="Second rest temperature")
		label4.pack()
		self.temp_var2 = IntVar()
		self.temp2= Entry(self, textvariable=self.temp_var2)
		self.temp2.pack()
		self.temp2.selection_range(0, END)			
		self.temp2.bind("<Return>", self.SecondTemp)
		
		label5=Label(self, text="Second rest time")
		label5.pack()
		self.time_var2 = IntVar()
		self.time2= Entry(self, textvariable=self.time_var2)
		self.time2.pack()
		self.time2.selection_range(0, END)			
		self.time2.bind("<Return>", self.SecondTime)
		
		button1 = Button(self, text="Start")
		button1.bind("<Return>",lambda event: controller.show_frame(Mashing))
		button1.pack()
		
		button2 = Button(self, text="Back to Home")
		button2.bind("<Return>",lambda event: controller.show_frame(StartPage))
		button2.pack()
    def FirstTemp(self, event):
		global temperatura
		temp_var = self.temp_var.get()
		self.temp_var.set(temp_var)
		temperatura=temp_var
		event.widget.tk_focusNext().focus()
		return temperatura
    def SecondTemp(self,event):
	    global temperatura2
	    temp_var2 = self.temp_var2.get()
	    self.temp_var2.set(temp_var2)
	    temperatura2=temp_var2
	    event.widget.tk_focusNext().focus()
	    return temperatura2
    def FirstTime(self, event):
        time_var=self.time_var.get()+2
        self.time_var.set(time_var)
        event.widget.tk_focusNext().focus()
    def SecondTime(self, event):
		time_var2=self.time_var2.get()+2
		self.time_var2.set(time_var2)
		event.widget.tk_focusNext().focus()
class Mashing(Frame):
	def __init__(self, parent, controller):
		window=Frame.__init__(self, parent)
		self.temp=StringVar()
		self.text = Label(self,text=self.temp, font=LARGE_FONT)
		self.text.pack(pady=10, padx=10) 
		self.GetTemp()		
		button = Button(self, text="Back to Home")
		button.bind("<Return>", lambda event: controller.show_frame(StartPage))		
		button.pack()
	def GetTemp(self):
		self.text.configure(text=read_temp("28-0215021f66ff"))
		self._timer=root.after(500,self.GetTemp)   
		
class PageTwo(Frame):
    def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		label = Label(self, text="Brewing", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		button1 = Button(self, text="Page One",
		command=lambda: controller.show_frame(PageOne))
		button1.pack()
		button2 = Button(self, text="Back to Home")
		button2.bind("<Return>", lambda event: controller.show_frame(StartPage))		
		button2.pack()

class Sensor():
	def __init__(self,sensor_addr):
		self.sensor_addr=sensor_addr
	def temp_sensor(self, sensor_addr):
		temp_measured=read_temp(sensor_addr)
		return temp_measured		
def control():
	obj=Sensor("28-0215021f66ff")	
	temp_meas=obj.temp_sensor("28-0215021f66ff")
	temp_set=temperatura
	error = temp_set-temp_meas
	global zmierzona_temp
	zmierzona_temp=temp_meas
	print temp_meas
	print temp_set
	print error
	if error < 10:
		GPIO.output(23,GPIO.HIGH)
	else: 
		GPIO.output(23,GPIO.LOW)
	root.after(2000,control)		
root=Tk()
app=Start(root)
root.title("BrewWizard")
#root.after(2000,control)
#root.after(2000, GetTemp)
root.update_idletasks()
root.mainloop()


