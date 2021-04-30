#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

style.use('ggplot')

class GUI(tk.Tk):
    def __init__(self, title='Temp_log', min_size=(1000,630), bg='#131313',
                 fg='white', canvas_colour='white'):
        super().__init__()
        self._graph  = None
        self._fig    = None
        self._canvas = None
        self._initialise_window(title, min_size, bg, fg)
        self._create_canvas(canvas_colour)
        self._create_buttons()

    def _initialise_window(self, title, min_size, bg, fg):
        self.title(title)
        self.minsize(*min_size)
        self['bg'] = bg

    def _create_canvas(self, canvas_colour):
        # Create a blanc initial frame
        self._update_graph(True)
        # Prepare the convas to contain graphs
        self._graph = Figure()
        self._fig = self._graph.add_subplot(111) 
        

    def _create_buttons(self):
        self._create_day_button()
        self._create_week_button()
        self._create_month_button()
        self._create_csv_button()


    def _create_day_button(self):
        ttk.Button(self, text="Day",
                   command=self._draw_day).place(
                   relx=0.03, rely=0.92, relwidth=0.1)

    def _create_week_button(self):
        ttk.Button(self, text="Week",
                   command=self._draw_week).place(
                   relx=0.145, rely=0.92, relwidth=0.1)

    def _create_month_button(self):
        ttk.Button(self, text="Month",
                   command=self._draw_month).place(
                   relx=0.26, rely=0.92, relwidth=0.1)

    def _create_csv_button(self):
        ttk.Button(self, text="Get CSV",
                   command=self._save_csv).place(
                   relx=0.375, rely=0.92, relwidth=0.1)

    def _draw_day(self):
        self._fig.clear()
        self._fig.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        self._update_graph()

    def _draw_week(self):     
        self._fig.clear()
        self._fig.plot([1,2,3,4,5,6,7,8],[2,8,9,3,1,9,3,15])
        self._update_graph()

    def _draw_month(self):     
        self._fig.clear()
        self._fig.plot([1,2,3,4,5,6,7,8],[20,-12,9,8,1,9,3,-6])
        self._update_graph()

    def _save_csv(self):
        print("CSV")

    # I'm re-drawing the canvas each time I'm changing the view but
    # it's a dirty hack that works \__(°_°)__/
    def _update_graph(self, virgin=False):
        # Only happens once at the start to get a clear screen
        if(virgin):
            self._graph = Figure()

        self._canvas = FigureCanvasTkAgg(self._graph, self)
        self._canvas.get_tk_widget().place(relx=0.03, rely=0.052,
                                 relheight=0.85, relwidth=0.9)