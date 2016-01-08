#!/usr/bin/python
#-*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import time
from collections import deque
from temp_read import * 
import RPi.GPIO as GPIO

LARGE_FONT= ("Verdana", 12)
temperatura=0
time1=0
temperatura2=0
time2=0
brewing_time=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(1,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

def turnHeaters(pinsOn,pinsOff):
	for i in pinsOff:
		GPIO.output(i,GPIO.LOW)
	for j in pinsOn:
		GPIO.output(j,GPIO.HIGH)

def turnOnPump():	
	GPIO.output(16,GPIO.HIGH)

def turnOffPump():
	GPIO.output(16,GPIO.LOW)
	
def bufer(bufer, inputTemp):
		bufer.pop()
		bufer.appendleft(inputTemp)
		print bufer

class Sensor():
	def __init__(self,sensor_addr):
		self.sensor_addr=sensor_addr
	def temp_sensor(self, sensor_addr):
		temp_measured=read_temp(sensor_addr)
		return temp_measured
turnHeaters([],[23,24,25])	
MashSensor=Sensor("28-0215021f66ff")
HLTSensor=Sensor("28-021501c439ff")#("28-021501c439ff")
BrewSensor=Sensor("28-021501c439ff")
class InputVerification():
	def correctInput(self):
		tkMessageBox.showerror(
				"Wrong input",
				"Please check input!")
	def checkInput(self, inputVal):
		if inputVal.isdigit():
			inputVal=int(float(inputVal))
			if inputVal > 100:
				self.correctInput()
			else:
				return True
		else:
			self.correctInput()

class Counter():
	seconds=0
	minutes=0
	hours=0
	elapsed=0
	def __init__(self, start_time):
		self.start_time=start_time
	def count(self, start_time):
		self.refreshed_time=time.time()
		self.seconds=round(float(self.refreshed_time-self.start_time))
		if self.seconds>=60:
			self.start_time=time.time()
			self.seconds=0
			self.minutes=self.minutes+1
			self.elapsed+=1
			if self.minutes>=60:
				self.minutes=0
				self.hours=self.hours+1

class Start():
	def __init__(self, master, *args, **kwargs):
		self.container = Frame(master, width=600,height=600, takefocus=0)
		self.container.pack(side="top", fill="both", expand = True)
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)
		self.show_frame(StartPage)
	def show_frame(self, cont):		
		frame=cont(self.container, self)
		frame.grid(row=0, column=0, sticky="nsew" )
		frame.tkraise()
		
class StartPage(Frame):	
	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		self.controller=controller
		self.pumpVar=0
		label = Label(self, text="Start Page", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		startMashing = Button(self, text="Press to start mashing")
		startMashing.bind("<Return>",lambda event: controller.show_frame(PageOne))
		startMashing.pack()
		startMashing.focus_set()
		startBrewing = Button(self, text="Press to start brewing")
		startBrewing.bind("<Return>",lambda event: controller.show_frame(PageTwo))
		startBrewing.pack()
		self.pumpStart=Button(self, text="Press to start the pump", fg="red")
		self.pumpStart.bind("<Return>", self.startPump)
		self.pumpStart.pack()
		shutDownRPi = Button(self, text="Shutdown")
		shutDownRPi.bind("<Return>", self.shutDown)
		shutDownRPi.pack()
	def shutDown(self, event):
		result=tkMessageBox.askyesno(
			"Shutdown",
			"Are you sure you want to shutdown the machine?"
			)
		if result:
			os.system("sudo shutdown -h now")
	def startPump(self, event):
		self.pumpVar+=1
		if self.pumpVar%2!=0:
			self.pumpStart.configure(text="Press to stop the pump", fg="green")
			turnOnPump()
		else:
			self.pumpStart.configure(text="Press to start the pump", fg="red")
			turnOffPump()		
 
class PageOne(Frame):
	preheated=False
	HLTTemperature=HLTSensor.temp_sensor("28-021501c439ff")
	def __init__(self, parent, controller):
		self.controller=controller
		Frame.__init__(self, parent)
		label = Label(self, text="Mashing", font=LARGE_FONT)
		label.pack()
		rest1Text=Label(self, text="First rest temperature")
		rest1Text.pack()
		self.temp_var = StringVar() 
		temp1= Entry(self, textvariable=self.temp_var)
		temp1.pack()
		temp1.focus_force()
		temp1.selection_range(0, END)			
		temp1.bind("<Return>", self.firstTemp)
		
		rest1Time=Label(self, text="First rest time")
		rest1Time.pack()
		self.time_var = StringVar()
		time1= Entry(self, textvariable=self.time_var)
		time1.pack()
		time1.selection_range(0, END)			
		time1.bind("<Return>", self.firstTime)
		
		rest2Text=Label(self, text="Second rest temperature")
		rest2Text.pack()
		self.temp_var2 = StringVar()
		temp2= Entry(self, textvariable=self.temp_var2)
		temp2.pack()
		temp2.selection_range(0, END)			
		temp2.bind("<Return>", self.secondTemp)
		
		rest2Time=Label(self, text="Second rest time")
		rest2Time.pack()
		self.time_var2 = StringVar()
		time2= Entry(self, textvariable=self.time_var2)
		time2.pack()
		time2.selection_range(0, END)			
		time2.bind("<Return>", self.secondTime)

		self.info=Label(self, text="You can't proceed to mashing yet, preheat first", fg="red")
		self.info.pack()

		self.start = Button(self, text="Start preheating")
		self.start.bind("<Return>", self.preheatInfo)
		self.start.pack()
		
		back = Button(self, text="Back to Home")
		back.bind("<Return>",lambda event: controller.show_frame(StartPage))
		back.pack()
		self.verification=InputVerification()
	def preheatInfo(self,event):
		if self.HLTTemperature<temperatura:
			result=tkMessageBox.askyesno(
        	    "Preheating",
        	    "You are about to preheat HLTank and Boil Kettle.Proceed?")
			if result:
				self.preheatOfHLT()
		else:
			tkMessageBox.showinfo(
				"Preheating",
				"The water is already preheated!")
			self.preheated=True
			self.info.configure(text="You may now proceed, remember to set valves to appropriate position", fg="green", font=LARGE_FONT)
			self.start.configure(text="Start mashing")
			self.start.bind("<Return>", lambda event: self.controller.show_frame(Mashing))
	def preheatDone(self):
		result=tkMessageBox.askyesno(
            "Preheating",
            "Preheating done, make sure the valves are in appropriate position\n Start the pump now?")
		if result:
			self.pumpOff()
	def pumpOff(self):
		turnOnPump()
		result=tkMessageBox.askyesno(
			"Pumping",
			"Stop the pump?")
		if result:
			self.start.configure(text="Start mashing")
			self.start.bind("<Return>", lambda event: self.controller.show_frame(Mashing))
			turnOffPump()
			self.preheated=True
			self.info.configure(text="You may now proceed, remember to set valves to appropriate position", fg="green", font=LARGE_FONT)
	def preheatOfHLT(self):
		preheatTempHLT=temperatura-2
		tempHLT=HLTSensor.temp_sensor("28-021501c439ff")
		turnHeaters([23,24,25],[])
		while(tempHLT<preheatTempHLT):
			tempHLT=HLTSensor.temp_sensor("28-021501c439ff")
			print tempHLT
		turnHeaters([],[23,24,25])
		self.preheatDone()

#	def preheatOfBK(self):
#		BK_Sensor=Sensor("adresss_BK")
#		measured_BK=BK_Sensor.temp_sensor("adresss_BK")
#		pre_BK_temp=temperatura+2
#		print pre_BK_temp
#		if True:
#			self.preheatDone()


	def firstTemp(self, event):
		global temperatura
		temp_var = self.temp_var.get()
		if self.verification.checkInput(temp_var):
			temperatura=int(float(temp_var))
			self.temp_var.set(temperatura)
			event.widget.tk_focusNext().focus()
			return temperatura
	def secondTemp(self,event):
		global temperatura2
		temp_var2 = self.temp_var2.get()
		if self.verification.checkInput(temp_var2):
			temperatura2=int(float(temp_var2))
			event.widget.tk_focusNext().focus()
			return temperatura2		
	def firstTime(self, event):
   		global time1
		time_var=self.time_var.get()
   		if self.verification.checkInput(time_var):
			time1=int(float(time_var))
			event.widget.tk_focusNext().focus()
			return time1
	def secondTime(self, event):
		global time2
		time_var2=self.time_var2.get()
		if self.verification.checkInput(time_var2):
			time2=int(float(time_var2))
			event.widget.tk_focusNext().focus() 

class Mashing(Frame):
	break_var=True	
	secondRest=False
	mashTemperatureBuffer=deque(5*[0], 5)
	HLTTemperatureBuffer=deque(5*[0], 5)
	heatingTime=0
	dt=0
	i=0
	def __init__(self, parent, controller):
		self.controller=controller
		self.temp_set=temperatura
		self.dErrTable=deque(5*[0], 5)
		self.StartTime=time.time()
		self.lastErr=0
		self.lastTime=self.StartTime
		self.time_set=time1
		self.secondRestTime=time2
		self.total_time=time1+time2
		
		Frame.__init__(self, parent)
		self.tempOfMash=StringVar()
		self.tempOfHLT=StringVar()
		self.state=Label(self, text="First rest in progess...", font=LARGE_FONT)
		self.state.grid(row=0, column=1)
		set_temp_info=Label(self, text="Temperature and time of first rest: %d°C for %d minutes" %(temperatura,time1), font=LARGE_FONT)
		set_temp_info.grid(row=1, column=1)
		set_temp_info2=Label(self, text="Temperature and time of second rest: %d°C for %d minutes" %(temperatura2,time2), font=LARGE_FONT)
		set_temp_info2.grid(row=2, column=1)
		temp_info=Label(self, text="Current temperature of the mash tun:", font=LARGE_FONT)
		temp_info.grid(row=4, column=1)
		self.textTempMash = Label(self,text=self.tempOfMash, font=LARGE_FONT)
		self.textTempMash.grid(row=4, column=2)
		
		temp_info=Label(self, text="Current temperature of the HLT:", font=LARGE_FONT)
		temp_info.grid(row=5, column=1)
		self.textTempHLT = Label(self,text=self.tempOfHLT, font=LARGE_FONT)
		self.textTempHLT.grid(row=5, column=2)
				
		time_info=Label(self, text="Time of mashing:", font=LARGE_FONT)
		time_info.grid(row=6, column=1)
		self.timer = Label(self,text='%d:%d:%d' %(0,0,0), font=LARGE_FONT)
		self.timer.grid(row=6, column=2)		
		button = Button(self, text="Stop and back to home")
		button.bind("<Return>", self.exitFcn)		
		button.focus_force()
		button.grid(row=7, column=1)
	
		self.time_control=Counter(self.StartTime)
		self.updateBuffer()
		self.control()
		turnOnPump()
		
	def updateBuffer(self):
		if self.break_var:
			if self.i%2!=0:
				MashTemperature=MashSensor.temp_sensor("28-0215021f66ff")
				bufer(self.mashTemperatureBuffer, MashTemperature)
			else:
				HLTTemperature=HLTSensor.temp_sensor("28-021501c439ff")
				bufer(self.HLTTemperatureBuffer,HLTTemperature)
			self.i+=1
			self.after(200, self.updateBuffer)
	def control(self):
		if (self.break_var) & (self.HLTTemperatureBuffer[0]<90):
			self.time_control.count(self.StartTime)
			tempMeasMash=self.mashTemperatureBuffer[0]
			tempMeasHLT=self.HLTTemperatureBuffer[0]
			self.timer.configure(text='%d:%d:%d' %(self.time_control.hours, self.time_control.minutes,self.time_control.seconds))
			self.textTempMash.configure(text=tempMeasMash)
			self.textTempHLT.configure(text=tempMeasHLT)
			now=time.time()
			dt=now-self.lastTime
			error = self.temp_set-tempMeasHLT
			dErr=(error - self.lastErr)/dt
			self.dErrTable.pop()
			self.dErrTable.appendleft(dErr)
			numerator=0
			for i in range (0,len(self.dErrTable)):
				numerator+=self.dErrTable[i]
				averaged=numerator/5
			
			self.lastErr=error
			self.lastTime=now
			if error > 4:
				turnHeaters([23,24,25],[])
			elif 2<error<=4:  
				turnHeaters([23,24],[25])
			elif(0.1<error<=2):
				if (0<error<=0.4)and(averaged<0)or (error==0):
					turnHeaters([],[23,24,25])
				elif (error>0.25)and(averaged>0):
					turnHeaters([23],[24,25])
			else:
				turnHeaters([],[23,24,25])
			
			if self.secondRest:
				if self.temp_set-1<=tempMeasHLT<=self.temp_set+1:
					heatingTime=self.time_control.elapsed-time1
					self.total_time=self.total_time+heatingTime
					self.secondRest=False
					self.state.configure(text="Second rest in progress...", fg="black")
			if (self.time_control.elapsed==self.time_set)&(self.time_set!=self.total_time):
				self.temp_set=temperatura2
				self.time_set=time2
				self.secondRest=True
				self.state.configure(text="Heating up...", fg="red")
				
			elif (self.time_control.elapsed==self.total_time) & (self.secondRest!=True):
				self.stop()
				self.state.configure(text="Done! :)", fg="green")
			self._timer=self.after(300,self.control)
	def exitFcn(self, event):
		result=tkMessageBox.askyesno(
			"Exit",
			"Are you sure you want to exit?")
		if result:
			self.stop()
			self.controller.show_frame(StartPage)
			
	def stop(self):
		self.break_var=False
		turnHeaters([],[23,24,25])
		turnOffPump()
		
class PageTwo(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		label = Label(self, text="Brewing", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		label2= Label(self, text="Set the time of brewing:")
		label2.pack()
		self.brew_var=StringVar()
		brew_time= Entry(self, textvariable=self.brew_var)
		brew_time.pack()
		brew_time.focus_force()
		brew_time.selection_range(0, END)
		brew_time.bind("<Return>", self.brewingTime)

		button1 = Button(self, text="Start brewing")
		button1.bind("<Return>", lambda event: controller.show_frame(Brewing))
		button1.pack()
		button2 = Button(self, text="Back to Home")
		button2.bind("<Return>", lambda event: controller.show_frame(StartPage))		
		button2.pack()
		self.verification=InputVerification()
	def brewingTime(self, event):
		global brewing_time
		brew_var=self.brew_var.get()
		if self.verification.checkInput(brew_var):
			brewing_time=int(float(brew_var))
			event.widget.tk_focusNext().focus() 

class Brewing(Frame):
	break_var=True
	heating_var=True
	brewTemperatureBuffer=deque(5*[0], 5)
	def __init__(self, parent, controller):
		self.controller=controller
		Frame.__init__(self, parent)
		self.heaters_on=1
		self.StartTime=time.time()
		self.time_set=brewing_time
		self.label = Label(self, text="Heating up...", font=LARGE_FONT)
		self.label.grid(row=1, column=1)
		temp_info=Label(self, text="Current temperature of wort:", font=LARGE_FONT)
		temp_info.grid(row=2, column=1)
		self.current_temp=Label(self, text=" ", font=LARGE_FONT)
		self.current_temp.grid(row=2, column=2)
		brew_time_info=Label(self, text="Set time of brewing:", font=LARGE_FONT)
		brew_time_info.grid(row=3, column=1)
		brew_time_info2=Label(self, text="%d minutes" % brewing_time, font=LARGE_FONT)
		brew_time_info2.grid(row=3, column=2)
		brew_time_elapsed=Label(self, text="Elapsed time of brewing:", font=LARGE_FONT)
		brew_time_elapsed.grid(row=4, column=1)
		self.timer1=Label(self, text="%d:%d:%d" %(0,0,0), font=LARGE_FONT)
		self.timer1.grid(row=4, column=2)
		self.elapsed=Label(self, text="Time of heating up:", font=LARGE_FONT)
		self.elapsed.grid(row=5, column=1)
		self.elapsed_time=Label(self, text="%d minutes %d seconds" %(0,0), font=LARGE_FONT)
		self.elapsed_time.grid(row=5, column=2)
		heater_info=Label(self, text="Number of heaters working to sustain boiling:", font=LARGE_FONT)
		heater_info.grid(row=6, column=1)
		self.heaters=Entry(self, text=self.heaters_on)
		self.heaters.grid(row=6, column=2)
		button = Button(self, text="Stop and back to Home")
		button.bind("<Return>", self.exitFcn)		
		button.grid(row=7, column=1)
		
		self.heaters.focus_force()
		self.heat_time_control=Counter(self.StartTime)
		self.updateBuffer()
		self.control()
	def noOfHeaters(self):
		heaters = self.heaters.get()
		self.heaters_on=heaters
		return self.heaters_on	
	
	def updateBuffer(self):
		if self.break_var:
			BrewTemperature=BrewSensor.temp_sensor("28-021501c439ff")
			bufer(self.brewTemperatureBuffer,BrewTemperature)
			self.after(200, self.updateBuffer)
	
	def control(self):
		if self.break_var:
			temp_meas=self.brewTemperatureBuffer[0]
			self.current_temp.configure(text=temp_meas)
			self.heat_time_control.count(self.StartTime)
			print self.heaters_on
			if self.heating_var:
				turnHeaters([8,7,1],[])
				minutes=self.heat_time_control.minutes
				seconds=self.heat_time_control.seconds
				self.elapsed_time.configure(text='%d minutes %d seconds' %(minutes,seconds))
				self.start_brewing_time=time.time()
				self.brew_time_control=Counter(self.start_brewing_time)
			if temp_meas>20:
				self.heating_var=False
				self.noOfHeaters()
				if self.heaters_on=="1":
					turnHeaters([8],[7,1])
				elif self.heaters_on=="2":
					turnHeaters([8,7],[1])
				elif self.heaters_on=="3":
					turnHeaters([8,7,1],[])
				else:
					turnHeaters([8,7],[1])
				
				self.brew_time_control.count(self.start_brewing_time)
				self.label.configure(text="Brewing in progress...", fg='green')
				self.timer1.configure(text='%d:%d:%d' %(self.brew_time_control.hours, self.brew_time_control.minutes,self.brew_time_control.seconds))
			
				if self.brew_time_control.minutes==self.time_set:
					turnHeaters([], [8,7,1])
					self.break_var=False
					self.label.configure(text="Done! :)", fg="green")
			self._timer=self.after(1000,self.control)
	
	def exitFcn(self, event):
		result=tkMessageBox.askyesno(
			"Exit",
			"Are you sure you want to exit?")
		if result:
			self.stop()
			
	def stop(self):
		self.break_var=False
		turnHeaters([],[8,7,1])
		self.controller.show_frame(StartPage)
	

root=Tk()
root.geometry('600x300+750+100')
#root.attributes('-fullscreen', True)    set to fullscreen
app=Start(root)
root.title("BreWizard")
root.mainloop()

