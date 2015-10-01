#!/usr/bin/python
#-*- coding: iso-8859-1 -*-

import Tkinter as tk 
LARGE_FONT= ("Verdana", 12)
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
		label = tk.Label(self, text="Start Page", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		button = tk.Button(self, text="Press to start mashing")
		button.bind("<Return>",lambda event: controller.show_frame(PageOne))
		button.pack()
		button.focus_set()
		button2 = tk.Button(self, text="Pressto start brewing")
		button2.bind("<Return>",lambda event: controller.show_frame(PageTwo))
		button2.pack()
 
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Mashing", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.rest_var = tk.StringVar()
	self.rest_no= tk.Entry(self, textvariable=self.rest_var)
	self.rest_no.pack()
	self.rest_no.focus()
	self.rest_no.bind("<Return>", self.ConvertToNumber)
	
	
        button1 = tk.Button(self, text="Back to Home")
        button1.bind("<Return>",lambda event: controller.show_frame(StartPage))
        button1.pack()
    def ConvertToNumber(self,rest_var):
		number = int(float(self.rest_var.get()))
		print (number +2)

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

app = Start()
app.title("BrewMaster")
app.mainloop()
