#!/usr/bin/python
#-*- coding: utf-8 -*-

import Tkinter as tk
from temp_read import * 
LARGE_FONT= ("Verdana", 12)
temperatura=0
class Start(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, width=400,height=400)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
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
		self.temp1.focus()			
		self.temp1.bind("<Return>", self.FirstTemp)
		label3=tk.Label(self, text="First rest time")
		label3.pack()
		self.time_var = tk.IntVar()
		self.time1= tk.Entry(self, textvariable=self.time_var)
		self.time1.pack()
		self.time1.focus()			
		self.time1.bind("<Return>", self.FirstTime)
		button1 = tk.Button(self, text="Back to Home")
		button1.bind("<Return>",lambda event: controller.show_frame(StartPage))
		button1.pack()
		print files
    def FirstTemp(self, event):
		global temperatura
		temp_var = self.temp_var.get()+read_temp("28-0215021f66ff")
		self.temp_var.set(temp_var)
		temperatura=temp_var
		return temperatura
    def Temp(self):
	    x=self.temp_var.get()
	    print x
    def FirstTime(self, event):
        time_var=self.time_var.get()+2
        self.time_var.set(time_var)
 

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

class control():
	def __init__(self,sensor_addr):
		self.sensor_addr=sensor_addr
	def temp_1(self, sensor_addr):
		temp_measured=read_temp(sensor_addr)
		temp_set=temperatura
		print temp_set
		print temp_measured
		print temp_set-temp_measured
		app.after(200,obj.temp_1(sensor_addr))		
obj=control("28-0215021f66ff")

app = Start()
app.title("BrewWizard")
app.after(200,obj.temp_1("28-0215021f66ff"))
app.mainloop()

