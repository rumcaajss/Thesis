#!/usr/bin/python
#-*- coding: iso-8859-1 -*-

import Tkinter as tk 
LARGE_FONT= ("Verdana", 12)
class Start(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

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
		button.focus_set()
		button.pack()

		button2 = tk.Button(self, text="Pressto start brewing")
		button2.bind("<Return>",lambda event: controller.show_frame(PageTwo))
		button2.pack()
 


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Mashing", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

	button1 = tk.Button(self, text="Page Two",
        command=lambda: controller.show_frame(PageTwo))
        button1.pack()

        button1 = tk.Button(self, text="Back to Home")
        button1.bind("<Return>",lambda event: controller.show_frame(StartPage))
        button1.pack()

       

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
