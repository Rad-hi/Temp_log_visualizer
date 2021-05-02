#!/usr/bin/env python3

from parser import parser

import tkinter as tk
from tkinter import ttk

import numpy as np

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

style.use('ggplot')

class GUI(tk.Tk):
    ''' This is the showroom, where all graphic elements are created '''
    BACKGROUND_COLOR    = '#131313'
    COMMON_Y_POS        = 0.925
    COMMON_X_POS        = 0.865
    # Holds an indicator on the current graph being drawn
    CURRENT_GRAPH       = None  
    # Holds the latest state of the max, min, mean checkbuttons 
    MAX_MIN_MEAN        = (0)*3 
    def __init__(self, title='Temp_log', min_size=(1120,630),
                 fg='white', canvas_colour='white'):
        super().__init__()
        self._initialise_window(title, min_size, fg)
        self._create_canvas(canvas_colour)
        self._create_widgets()
        self._parser = parser()

    def _initialise_window(self, title, min_size, fg):
        self.title(title)
        self.minsize(*min_size)
        self['bg'] = self.BACKGROUND_COLOR

    def _create_canvas(self, canvas_colour):
        # Create a blanc initial frame
        self._update_graph(virgin=True)
        # Prepare the canvas to contain graphs
        self._graph = Figure(figsize=(12, 6), dpi=90)
        self._fig = self._graph.add_subplot(111) 
        

    def _create_widgets(self):
        self._create_day_button()
        self._create_week_button()
        self._create_month_button()
        self._create_get_csv_button()
        self._create_load_csv_button()
        self._create_fetching_controls()
        self._create_mx_mi_mn_checkbuttons()

    def _create_day_button(self):
        ttk.Button(self, text="Day", command=self._draw_day)\
           .place(relx=0.03, rely=self.COMMON_Y_POS, relwidth=0.1)

    def _create_week_button(self):
        ttk.Button(self, text="Week", command=self._draw_week)\
           .place(relx=0.145, rely=self.COMMON_Y_POS, relwidth=0.1)

    def _create_month_button(self):
        ttk.Button(self, text="Month", command=self._draw_month)\
           .place(relx=0.26, rely=self.COMMON_Y_POS, relwidth=0.1)

    def _create_mx_mi_mn_checkbuttons(self): # Add commands to update the graph automatically ?
        tk.Label(self, text="Choose value(s) to graph:", 
                 bg=self.BACKGROUND_COLOR, fg="white")\
          .place(relx=0.375, rely=self.COMMON_Y_POS, relheight=0.048)

        self._check_Max  = tk.IntVar()
        ttk.Checkbutton(self, text="Max", variable=self._check_Max, 
                        onvalue=True, offvalue=False)\
           .place(relx=0.545, rely=self.COMMON_Y_POS, relheight=0.042, relwidth=0.05)
        
        self._check_Min  = tk.IntVar()
        ttk.Checkbutton(self, text="Min", variable=self._check_Min, 
                        onvalue=True, offvalue=False)\
           .place(relx=0.6, rely=self.COMMON_Y_POS, relheight=0.042, relwidth=0.05)
        
        self._check_Mean = tk.IntVar()
        ttk.Checkbutton(self, text="Mean", variable=self._check_Mean, 
                        onvalue=True, offvalue=False)\
           .place(relx=0.655, rely=self.COMMON_Y_POS, relheight=0.042, relwidth=0.05)


    def _create_get_csv_button(self):
        ttk.Button(self, text="Get CSV", command=self._save_csv)\
           .place(relx=self.COMMON_X_POS, rely=0.052, relwidth=0.1)

    def _create_load_csv_button(self):
        ttk.Button(self, text="Load CSV", command=self._load_csv)\
           .place(relx=self.COMMON_X_POS, rely=0.122, relwidth=0.1)

    def _create_fetching_controls(self):
        ttk.Separator(self, orient='horizontal')\
           .place(relx=self.COMMON_X_POS, rely=0.202, relwidth=0.1)
        
        ''' Create 3 entries for the USER, KEY, and FEED to fetch data from.
            Each entry is associated with a label that describes what it is,
            and each entry is binded to the enter key for passage to the next "UX-ish" '''

        tk.Label(self, text="AIO User", bg=self.BACKGROUND_COLOR, fg="white")\
          .place(relx=self.COMMON_X_POS, rely=0.23, relwidth=0.1, relheight=0.02)
        self.USER = tk.StringVar()
        user_entry = ttk.Entry(self, textvariable=self.USER)
        user_entry.place(relx=self.COMMON_X_POS, rely=0.252, relwidth=0.1)
        user_entry.bind('<Return>', lambda e=None: feed_entry.focus())

        tk.Label(self,text="AIO Feed", bg=self.BACKGROUND_COLOR, fg="white")\
          .place(relx=self.COMMON_X_POS, rely=0.29, relwidth=0.1, relheight=0.02)
        self.FEED = tk.StringVar()
        feed_entry = ttk.Entry(self, textvariable=self.FEED)
        feed_entry.place(relx=self.COMMON_X_POS, rely=0.312, relwidth=0.1)
        feed_entry.bind('<Return>', lambda e=None: key_entry.focus())

        tk.Label(self,text="AIO Key", bg=self.BACKGROUND_COLOR, fg="white")\
          .place(relx=self.COMMON_X_POS, rely=0.35, relwidth=0.1, relheight=0.02)
        self.KEY  = tk.StringVar()
        key_entry = ttk.Entry(self, textvariable=self.KEY, show="*")
        key_entry.place(relx=self.COMMON_X_POS, rely=0.372, relwidth=0.1)
        key_entry.bind('<Return>',self._authenticate)
        
        ttk.Button(self, text="Fetch data", command=self._authenticate)\
           .place(relx=self.COMMON_X_POS+0.03, rely=0.432, relwidth=0.07)


    def _draw_day(self):
        mx, mi, mn = self._get_checks()
        # To prevent redrawing the same thing
        if(self._parser.FETCHED and\
          (self.CURRENT_GRAPH != "D" or\
          (mx, mi, mn) != self.MAX_MIN_MEAN)): 
          
            self._draw(self._parser._df, (mx, mi, mn))
            self.CURRENT_GRAPH = "D"
            self.MAX_MIN_MEAN = (mx, mi, mn)

    ''' Draw week and month are for now static and do nothing '''
    def _draw_week(self):
        mx, mi, mn = self._get_checks()
        if(self.CURRENT_GRAPH != "W" or (mx, mi, mn) != self.MAX_MIN_MEAN):     
            self._fig.clear()
            self._fig.plot([1,2,3,4,5,6,7,8],[2,8,9,3,1,9,3,15])
            self._update_graph()
            self.CURRENT_GRAPH = "W"
            self.MAX_MIN_MEAN = (mx, mi, mn)

    def _draw_month(self):
        mx, mi, mn = self._get_checks()  
        if(self.CURRENT_GRAPH != "M" or (mx, mi, mn) != self.MAX_MIN_MEAN):
            self._fig.clear()
            self._fig.plot([1,2,3,4,5,6,7,8],[20,-12,9,8,1,9,3,-6])
            self._update_graph()
            self.CURRENT_GRAPH = "M"
            self.MAX_MIN_MEAN = (mx, mi, mn)

    ''' Should decide on the df format before working the savings '''
    def _save_csv(self):
        self._parser.output_csv("_save_csv")

    def _load_csv(self):
        self._parser = parser.from_file()

    def _authenticate(self, *args):
        ''' A connection to the adafruit API shall be tested here '''
        # Just try to connect and if an error occured report it
        user, feed, key = self._get_inputs()   
        if(len(user) and len(feed) and len(key)):
            self._parser.fetch_data(user, feed, key)
            self._reset_inputs()
        else:
            print("Type in Something")

    def _reset_inputs(self):
        self.USER.set("")
        self.FEED.set("")
        self.KEY.set("") 

    def _get_inputs(self):
        return self.USER.get(), self.FEED.get(), self.KEY.get()

    def _get_checks(self):
        return self._check_Max.get(), self._check_Min.get(), self._check_Mean.get()

    def _draw(self, data, values):
        mx_mi_mn = ["mx", "mi", "mn"]
        colours_ = ['#131313', (0,1,0), (0,0,1)] #customize these!?
        self._fig.clear()
        for i, value in enumerate(values):
            if value:
                # Deprecated, but works! .. well couldn't solve it for now...
                self._fig.plot(data["Hour"], data[mx_mi_mn[i]], color=colours_[i]) 
        self._update_graph()
        
    # I'm re-creating the canvas each time I'm changing the view but
    # it's a dirty hack that works \__(°_°)__/
    def _update_graph(self, virgin=False):
        # Only happens once at the start to get a clear screen
        if(virgin):
            self._graph = Figure()

        _canvas = FigureCanvasTkAgg(self._graph, self)
        _canvas.get_tk_widget()\
               .place(relx=0.03, rely=0.052, relheight=0.85, relwidth=0.8)
