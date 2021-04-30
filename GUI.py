#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

style.use('ggplot')

class GUI(tk.Tk):
    ''' This is the showroom, where all graphic elements are created '''
    COMMON_Y_POS  = 0.925
    COMMON_X_POS  = 0.865
    CURRENT_GRAPH = None
    def __init__(self, title='Temp_log', min_size=(1120,630), bg='#131313',
                 fg='white', canvas_colour='white'):
        super().__init__()
        self._initialise_window(title, min_size, bg, fg)
        self._create_canvas(canvas_colour)
        self._create_buttons()

    def _initialise_window(self, title, min_size, bg, fg):
        self.title(title)
        self.minsize(*min_size)
        self['bg'] = bg

    def _create_canvas(self, canvas_colour):
        # Create a blanc initial frame
        self._update_graph(virgin=True)
        # Prepare the canvas to contain graphs
        self._graph = Figure()
        self._fig = self._graph.add_subplot(111) 
        

    def _create_buttons(self):
        self._create_day_button()
        self._create_week_button()
        self._create_month_button()
        self._create_get_csv_button()
        self._create_load_csv_button()
        self._create_fetching_controls()

    def _create_day_button(self):
        ttk.Button(self, text="Day",
                   command=self._draw_day).place(
                   relx=0.03, rely=self.COMMON_Y_POS, relwidth=0.1)

    def _create_week_button(self):
        ttk.Button(self, text="Week",
                   command=self._draw_week).place(
                   relx=0.145, rely=self.COMMON_Y_POS, relwidth=0.1)

    def _create_month_button(self):
        ttk.Button(self, text="Month",
                   command=self._draw_month).place(
                   relx=0.26, rely=self.COMMON_Y_POS, relwidth=0.1)

    def _create_get_csv_button(self):
        ttk.Button(self, text="Get CSV",
                   command=self._save_csv).place(
                   relx=self.COMMON_X_POS, rely=0.052, relwidth=0.1)

    def _create_load_csv_button(self):
        ttk.Button(self, text="Load CSV",
                   command=self._load_csv).place(
                   relx=self.COMMON_X_POS, rely=0.122, relwidth=0.1)

    def _create_fetching_controls(self):
        self.FEED = tk.StringVar()
        self.KEY  = tk.StringVar()
        feed_entry = ttk.Entry(self, textvariable=self.FEED).place(
                               relx=self.COMMON_X_POS, 
                               rely=0.252,
                               relwidth=0.1)

        key_entry = ttk.Entry(self, textvariable=self.KEY, show="*")
        key_entry.place(relx=self.COMMON_X_POS, rely=0.312, relwidth=0.1)
        key_entry.bind('<Return>',self._authenticate) # Could be entered with an enter key press
        ttk.Button(self, text="Fetch data",
                   command=self._authenticate).place(
                   relx=self.COMMON_X_POS+0.03, 
                   rely=0.372, relwidth=0.07)

    def _draw_day(self):
        if(self.CURRENT_GRAPH != "D"): # To prevent redrawing the same thing
            self._fig.clear()
            self._fig.plot([1,2,3,4,5,6,7,8],[5,6,1,None,5,9,3,5])
            self._update_graph()
            self.CURRENT_GRAPH = "D"

    def _draw_week(self):
        if(self.CURRENT_GRAPH != "W"):     
            self._fig.clear()
            self._fig.plot([1,2,3,4,5,6,7,8],[2,8,9,3,1,9,3,15])
            self._update_graph()
            self.CURRENT_GRAPH = "W"

    def _draw_month(self):     
        if(self.CURRENT_GRAPH != "M"):
            self._fig.clear()
            self._fig.plot([1,2,3,4,5,6,7,8],[20,-12,9,8,1,9,3,-6])
            self._update_graph()
            self.CURRENT_GRAPH = "M"

    def _save_csv(self):
        print("Save CSV")

    def _load_csv(self):
        print("Load CSV")

    def _authenticate(self, *args):
        ''' A connection to the adafruit API shall be tested here '''
        print(f"Key: {self.KEY.get()}")
        if(self.FEED.get() == "Radhi"):
            if(self.KEY.get() == "1234"):
                print("Access granted!")
            else:
                print("You're not allowed here!")
                self.KEY.set("")

    # I'm re-drawing the canvas each time I'm changing the view but
    # it's a dirty hack that works \__(°_°)__/
    def _update_graph(self, virgin=False):
        # Only happens once at the start to get a clear screen
        if(virgin):
            self._graph = Figure()

        _canvas = FigureCanvasTkAgg(self._graph, self)
        _canvas.get_tk_widget().place(relx=0.03, rely=0.052,
                                      relheight=0.85, relwidth=0.8)
