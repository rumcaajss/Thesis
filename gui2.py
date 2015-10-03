#!/usr/bin/python
#-*- coding: utf-8 -*-

import Tkinter as tk
from temp_read import * 
import RPi.GPIO as GPIO
LARGE_FONT= ("Verdana", 12)
temperatura=0
temperatura2=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
class Start(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, width=400,height=400)
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

        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		self.controller=controller
		label = tk.Label(self, text="Start Page", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		button = tk.Button(self, text="Press to start mashing")
		button.bind("<Return>",lambda event: controller.show_frame(PageOne))
		button.pack()
		button.focus_set()
		button2 = tk.Button(self, text="Press to start brewing")
		button2.bind("<Return>",lambda event: controller.show_frame(PageTwo))
		button2.pack()
 
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
		self.controller=controller
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Mashing", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		
		label2=tk.Label(self, text="First rest temperature")
		label2.pack()
		self.temp_var = tk.IntVar()
		self.temp1= tk.Entry(self, textvariable=self.temp_var)
		self.temp1.pack()
		self.temp1.focus_force()
		self.temp1.selection_range(0, tk.END)			
		self.temp1.bind("<Return>", self.FirstTemp)
		
		label3=tk.Label(self, text="First rest time")
		label3.pack()
		self.time_var = tk.IntVar()
		self.time1= tk.Entry(self, textvariable=self.time_var)
		self.time1.pack()
		self.time1.selection_range(0, tk.END)			
		self.time1.bind("<Return>", self.FirstTime)
		
		label4=tk.Label(self, text="Second rest temperature")
		label4.pack()
		self.temp_var2 = tk.IntVar()
		self.temp2= tk.Entry(self, textvariable=self.temp_var2)
		self.temp2.pack()
		self.temp2.selection_range(0, tk.END)			
		self.temp2.bind("<Return>", self.SecondTemp)
		
		label5=tk.Label(self, text="Second rest time")
		label5.pack()
		self.time_var2 = tk.IntVar()
		self.time2= tk.Entry(self, textvariable=self.time_var2)
		self.time2.pack()
		self.time2.selection_range(0, tk.END)			
		self.time2.bind("<Return>", self.SecondTime)
		
		button1 = tk.Button(self, text="Start")
		button1.bind("<Return>",lambda event: controller.show_frame(Mashing))
		button1.pack()
		
		button2 = tk.Button(self, text="Back to Home")
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
class Mashing(tk.Frame):
	def __init__(self, parent, controller):
		window=tk.Frame.__init__(self, parent)
		self.temp=tk.IntVar()
		label = tk.Label(self,text=self.temp, font=LARGE_FONT)
		label.pack(pady=10, padx=10) 
		#self.window.after(2000,_thread_start_new_thread, self.GetTemp())
		
		
		button = tk.Button(self, text="Back to Home")
		button.bind("<Return>", lambda event: controller.show_frame(StartPage))		
		button.pack()
	#def GetTemp(self):
		#temp=read_temp("28-0215021f66ff")
		#self.temp.set(str(temp)   

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Brewing", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		button1 = tk.Button(self, text="Page One",
		command=lambda: controller.show_frame(PageOne))
		button1.pack()
		button2 = tk.Button(self, text="Back to Home")
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
	print temp_meas
	print temp_set
	print error
	if error < 10:
		GPIO.output(23,GPIO.HIGH)
	else: 
		GPIO.output(23,GPIO.LOW)
	app.after(6000,control)		

app = Start()


app.title("BrewWizard")
app.after(6000,control)
app.update_idletasks()
app.mainloop()


