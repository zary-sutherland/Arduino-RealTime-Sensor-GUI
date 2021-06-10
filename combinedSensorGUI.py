# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 14:18:34 2020

@author: Sutherland
"""

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams.update(
    {
        'text.usetex': False,
        'font.family': 'stixgeneral',
        'mathtext.fontset': 'stix',
    }
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import serial
import time 
import math 
from tkinter import ttk 
import pandas as pd
from datetime import datetime

LARGEFONT =("Verdana", 35) 
arduinoSerial = serial.Serial('COM4', 115200);
class tkinterApp(tk.Tk): 
    
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
        
        # creating a container 
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True) 

        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 
        # initializing frames to an empty array 
        self.frames = {} 

        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartPage, Page1, Page2): 

            frame = F(container, self) 

            # initializing frame of that object from 
            # startpage, page1, page2 respectively with 
            # for loop 
            self.frames[F] = frame 

            frame.grid(row = 0, column = 0, sticky ="nsew") 

        self.show_frame(StartPage) 

    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise()

# first window frame startpage 

class StartPage(tk.Frame): 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        
        # label of frame Layout 2 
        label = ttk.Label(self, text ="HOME", font = LARGEFONT) 
        
        # putting the grid in its place by using 
        # grid 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 

        button1 = ttk.Button(self, text ="MPU6050", 
        command = lambda : controller.show_frame(Page1)) 
    
        # putting the button in its place by 
        # using grid 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 

        ## button to show frame 2 with text layout2 
        button2 = ttk.Button(self, text ="DHT11", 
        command = lambda : controller.show_frame(Page2)) 
    
        # putting the button in its place by 
        # using grid 
        button2.grid(row = 2, column = 1, padx = 10, pady = 10) 
        


# second window frame page1 
class Page1(tk.Frame): 
    
    def __init__(self, parent, controller): 
        
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Live MPU6050 Tilt Angles", font = LARGEFONT) 
        label.grid(row = 0, column = 2, padx = 10, pady = 10) 

        # button to show frame 2 with text 
        # layout2 
        button1 = ttk.Button(self, text ="StartPage", 
                            command = lambda : controller.show_frame(StartPage)) 
    
        # putting the button in its place 
        # by using grid 
        button1.grid(row = 2, column = 1, padx = 10, pady = 10) 

        # button to show frame 2 with text 
        # layout2 
        button2 = ttk.Button(self, text ="DHT11", 
                            command = lambda : controller.show_frame(Page2)) 
    
        # putting the button in its place by 
        # using grid 
        button2.grid(row = 3, column = 1, padx = 10, pady = 10)        
        start = ttk.Button(self, text="start", command=lambda: self.startPlot())
        start.grid(row = 4, column = 1, padx = 10, pady = 10)
        stop = ttk.Button(self, text="Stop", command=lambda: self.stopPlot())
        stop.grid(row = 5, column = 1, padx = 10, pady = 10)
        data = '';
        cond = False  
        self.parent = parent
        fig = Figure()
        self.ax = fig.add_subplot(111, polar=True)
        self.ax.set_title('Roll Tilt Angle', y=1.08)
        self.ax.set_theta_zero_location('N')
        # ax.set_theta_direction(-1) #make the plot clockwise
        self.ax.set_yticks([])
        self.ax.set_xticks(np.pi/180. * np.linspace(180,  -180, 8, endpoint=False))
        self.ax.set_thetalim(-np.pi, np.pi)
        self.canvasA = FigureCanvasTkAgg(fig,master=self)
        self.canvasA.get_tk_widget().grid(row = 1, column = 1, padx = 10, pady = 10)
        self.canvasA.draw()
        
        
    def plotData(self):
        global cond
        if (cond == True):
            data = arduinoSerial.readline().decode('UTF-8')
            if data.split(' ', 1)[0] == 'X':
                roll = data.split(' ')[1]
                pitch = data.split(' ')[3]
                print('Roll:  '+roll+'  |  '+'Pitch:  '+pitch)
                roll = float(roll)
                pitch = float(pitch)
                labels = str(roll)+'°'
                ln, = self.ax.plot((0, math.radians(roll)), (0,1), lw=2, color="red")
                self.canvasA.draw()
                ln.remove()
            self.after(200, lambda: self.plotData())
            
    def startPlot(self):
        global cond
        cond = True
        if arduinoSerial.is_open:
            arduinoSerial.write('MPU6050'.encode('UTF-8'))
            self.plotData()
        else:
            arduinoSerial.open()
            arduinoSerial.write('MPU6050'.encode('UTF-8'))
            self.plotDate()
        
    def stopPlot(self):
        global cond
        cond = False
        self.arduinoSerial.close()


# third window frame page2 
class Page2(tk.Frame): 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text ="Real Time Temperature and Humidity", font = LARGEFONT) 
        label.grid(row = 0, column = 4, padx = 10, pady = 10) 

        # button to show frame 2 with text 
        # layout2 
        button1 = ttk.Button(self, text ="MPU6050", 
                            command = lambda : controller.show_frame(Page1)) 
    
        # putting the button in its place by 
        # using grid 
        button1.grid(row = 1, column = 1, padx = 10, pady = 10) 

        # button to show frame 3 with text 
        # layout3 
        button2 = ttk.Button(self, text ="Startpage", 
                            command = lambda : controller.show_frame(StartPage)) 
    
        # putting the button in its place by 
        # using grid 
        button2.grid(row = 2, column = 1, padx = 10, pady = 10) 
        start = ttk.Button(self, text="start", command=lambda: self.startPlot())
        start.grid(row = 4, column = 1, padx = 10, pady = 10)
        stop = ttk.Button(self, text="Stop", command=lambda: self.stopPlot())
        stop.grid(row = 5, column = 1, padx = 10, pady = 10)
        data = '';
        cond = False  
        fig = Figure()
        self.ax1 = fig.add_subplot(311)
        self.ax2 = fig.add_subplot(313)
        fig.subplots_adjust(bottom=0.2)
        self.ax1.set_title('Real Time Temperature')
        self.ax2.set_title('Real Time Humidity')
        self.ax1.set_xlabel('Timestamp')
        self.ax1.set_ylabel('Temperature in °C')
        self.ax2.set_xlabel('Timestamp')
        self.ax2.set_ylabel('Humidity in % of Relative Humdity')
        self.ax1.tick_params('x', labelrotation=45)
        self.ax2.tick_params('x', labelrotation=45)
        self.temp_df = pd.DataFrame(columns=['Timestamp', 'Temperature'])
        self.humidity_df = pd.DataFrame(columns=['Timestamp', 'Humidity'])
        self.canvasB = FigureCanvasTkAgg(fig,master=self)
        self.canvasB.get_tk_widget().grid(row = 1, column = 1, padx = 10, pady = 10)
        self.canvasB.draw()
        
    def plotData(self):
        global cond
        if (cond == True):
            data = arduinoSerial.readline().decode('UTF-8')
            if data.split(' ', 1)[0] == 'Temperature':
                temperature = data.split(' ')[1]
                humidity = data.split(' ')[3]
                print('Temp:  '+temperature+'  |  '+'Humidity:  '+humidity)
                if len(self.temp_df) < 100:
                    self.time = datetime.now()
                    self.temp_df.loc[len(self.temp_df)] = [self.time, temperature] 
                    self.humidity_df.loc[len(self.humidity_df)] = [self.time, humidity]
                else:
                    self.temp_df.drop(index=0, inplace=True)
                    self.humidity_df.drop(index=0, inplace=True)
                    self.temp_df.index = range(len(self.temp_df))
                    self.humidity_df.index = range(len(self.humidity_df))
                
                self.ln1, = self.ax1.plot(self.temp_df.Timestamp, self.temp_df.Temperature)
                self.ln2, = self.ax2.plot(self.humidity_df.Timestamp, self.humidity_df.Humidity)
                self.canvasB.draw()
                self.ln1.remove()
                self.ln2.remove()            
        self.after(200, lambda: self.plotData())
                
    def startPlot(self):
        global cond
        cond = True
        if arduinoSerial.is_open:
            arduinoSerial.write('DHT11'.encode('UTF-8'))
            self.plotData()
        else:
            arduinoSerial.open()
            arduinoSerial.write('DHT11'.encode('UTF-8'))
            self.plotDate()
            
    def stopPlot(self):
        global cond
        cond = False
        arduinoSerial.close()
        
# Driver Code 
app = tkinterApp() 
app.mainloop() 
