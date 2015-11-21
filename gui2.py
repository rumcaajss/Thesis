#!/usr/bin/python
#-*- coding: utf-8 -*-
from Tkinter import *
import time
from temp_read import * 
import RPi.GPIO as GPIO

LARGE_FONT= ("Verdana", 12)
temperatura=0
temperatura2=0
zmierzona_temp=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
class Sensor():
	def __init__(self,sensor_addr):
		self.sensor_addr=sensor_addr
	def temp_sensor(self, sensor_addr):
		temp_measured=read_temp(sensor_addr)
		return temp_measured
class Start():
    def __init__(self, master, *args, **kwargs):
		#__init__(self, *args, **kwargs)
		self.container = Frame(master, width=400,height=400)
		self.container.pack(side="top", fill="both", expand = True)
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)
		self.history = []
		self.show_frame(StartPage)
			
    def show_frame(self, cont):		
		frame=cont(self.container, self)
		frame.grid(row=0, column=0, sticky="nsew")
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
		
		label2=Label(self, text="First rest temperature[deg C]")
		label2.pack()
		self.temp_var = IntVar()
		self.temp1= Entry(self, textvariable=self.temp_var)
		self.temp1.pack()
		self.temp1.focus_force()
		self.temp1.selection_range(0, END)			
		self.temp1.bind("<Return>", self.FirstTemp)
		
		label3=Label(self, text="First rest time[m]")
		label3.pack()
		self.time_var = IntVar()
		self.time1= Entry(self, textvariable=self.time_var)
		self.time1.pack()
		self.time1.selection_range(0, END)			
		self.time1.bind("<Return>", self.FirstTime)
		
		label4=Label(self, text="Second rest temperature[deg C]")
		label4.pack()
		self.temp_var2 = IntVar()
		self.temp2= Entry(self, textvariable=self.temp_var2)
		self.temp2.pack()
		self.temp2.selection_range(0, END)			
		self.temp2.bind("<Return>", self.SecondTemp)
		
		label5=Label(self, text="Second rest time[m]")
		label5.pack()
		self.time_var2 = IntVar()
		self.time2= Entry(self, textvariable=self.time_var2)
		self.time2.pack()
		self.time2.selection_range(0, END)			
		self.time2.bind("<Return>", self.SecondTime)
		
		button1 = Button(self, text="Start")
		button1.bind("<Return>", lambda event: controller.show_frame(Mashing))
		button1.pack()
		
		button2 = Button(self, text="Back to Home")
		button2.bind("<Return>",lambda event: controller.show_frame(StartPage))
		button2.pack()
				
    def FirstTemp(self, event):
		global temperatura
		temp_var = self.temp_var.get()
		temperatura=temp_var
		self.temp_var.set(temperatura)
		
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
		self.controller=controller
		self.startTime=time.time()
		Frame.__init__(self, parent)
		self.temp=StringVar()
		self.ti=0.00
		self.temp_info=Label(self, text="Current temperature of the mash tun:", font=LARGE_FONT)
		self.temp_info.grid(row=0)
		self.text = Label(self,text=self.temp, font=LARGE_FONT)
		self.text.grid(row=0, column=2)	
		self.text2=Label(self, text=self.ti, font=LARGE_FONT)	
		self.text2.grid(row=1, column=1)
		self.break_var=True
		self.GetTemp()		
		button = Button(self, text="Back to Home")
		button.bind("<Return>", self.Stop)		
		button.focus_force()
		button.grid(row=3, column=1)		
			
	def GetTemp(self):
		if self.break_var:
			bu=time.time()
			dt=bu-self.startTime
			if dt==60:
				dt=0
				minutes=minutes+1
				
			self.text2.configure(text=dt)
			obj2=Sensor("28-0215021f66ff")	
			temp_meas=obj2.temp_sensor("28-0215021f66ff")
			self.text.configure(text=temp_meas)
			temp_set=temperatura
			error = temp_set-temp_meas
			print temp_meas
			print temp_set
			print error	
			if error<0:
				GPIO.output(23,GPIO.HIGH)
			else: 
				GPIO.output(23,GPIO.LOW)
			self._timer=self.after(140,self.GetTemp)
			print self.break_var
	def Stop(self, event):
		self.break_var=False
		self.controller.show_frame(StartPage)
		GPIO.output(23, GPIO.HIGH) #setting relay to high(switchin it off)
		print self.break_var 
		
		
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
	
root=Tk()
app=Start(root)
root.title("BrewWizard")
root.mainloop()


