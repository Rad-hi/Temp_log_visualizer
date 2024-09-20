#!/usr/bin/env python3

from parser import parser

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from tkcalendar import DateEntry

from calendar import monthrange

import numpy as np

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

style.use('ggplot')

class MyDateEntry(DateEntry):
    ''' Create a custom date entry that modifies the drop_down method
        and makes it auto-adjust to not get out of the screen when intersecting '''
    def __init__(self, master=None, align='left', **kw):
        DateEntry.__init__(self, master, **kw)
        self.align = align

    def drop_down(self):
        """Display or withdraw the drop-down calendar depending on its current state."""
        if self._calendar.winfo_ismapped():
            self._top_cal.withdraw()
        else:
            self._validate_date()
            date = self.parse_date(self.get())
            h = self._top_cal.winfo_reqheight()
            w = self._top_cal.winfo_reqwidth()
            x_max = self.winfo_screenwidth()
            y_max = self.winfo_screenheight()
            # default: left-aligned drop-down below the entry
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            if x + w > x_max:  # the drop-down goes out of the screen
                # right-align the drop-down
                x += self.winfo_width() - w
            if y + h > y_max:  # the drop-down goes out of the screen
                # bottom-align the drop-down
                y -= self.winfo_height() + h
            if self.winfo_toplevel().attributes('-topmost'):
                self._top_cal.attributes('-topmost', True)
            else:
                self._top_cal.attributes('-topmost', False)
                self._top_cal.geometry('+%i+%i' % (x, y))
                self._top_cal.deiconify()
                self._calendar.focus_set()
                self._calendar.selection_set(date)

class GUI(tk.Tk):
    ''' This is the showroom '''
    
    BACKGROUND_COLOR    = '#131313'
    COMMON_Y_POS        = 0.925
    COMMON_X_POS        = 0.865
    # Holds an indicator on the current graph being drawn
    CURRENT_GRAPH       = None  
    # Holds the latest state of the max, min, mean checkbuttons 
    MAX_MIN_MEAN        = (0)*3 
    # Holds the latest picked date
    DATE                = ('')*3
    # Holds the latest state of the max_col, min_col, mean_col
    COLORS              = ('')*3

    def __init__(self, title='Temp_log', min_size=(1020,560),
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
        self._create_date_picker()
        self._create_get_csv_button()
        self._create_load_csv_button()
        self._create_fetching_controls()
        self._create_mx_mi_mn_checkbuttons()
        self._create_color_pickers()

    def _create_day_button(self):
        ttk.Button(self, text="Day", command=self._draw_day)\
           .place(relx=0.03, rely=self.COMMON_Y_POS, relwidth=0.1)

    def _create_week_button(self):
        ttk.Button(self, text="Week", command=self._draw_week)\
           .place(relx=0.135, rely=self.COMMON_Y_POS, relwidth=0.1)

    def _create_month_button(self):
        ttk.Button(self, text="Month", command=self._draw_month)\
           .place(relx=0.239, rely=self.COMMON_Y_POS, relwidth=0.1)

    def _create_mx_mi_mn_checkbuttons(self): # Add commands to update the graph automatically ?
        tk.Label(self, text="Choose value(s) to graph:", 
                 bg=self.BACKGROUND_COLOR, fg="white")\
          .place(relx=0.355, rely=self.COMMON_Y_POS, relheight=0.048)

        self._check_Max  = tk.IntVar()
        ttk.Checkbutton(self, text="Max", variable=self._check_Max, 
                        onvalue=True, offvalue=False)\
           .place(relx=0.515, rely=self.COMMON_Y_POS, relheight=0.042, relwidth=0.05)
        
        self._check_Min  = tk.IntVar()
        ttk.Checkbutton(self, text="Min", variable=self._check_Min, 
                        onvalue=True, offvalue=False)\
           .place(relx=0.57, rely=self.COMMON_Y_POS, relheight=0.042, relwidth=0.05)
        
        self._check_Mean = tk.IntVar()
        ttk.Checkbutton(self, text="Mean", variable=self._check_Mean, 
                        onvalue=True, offvalue=False)\
           .place(relx=0.624, rely=self.COMMON_Y_POS, relheight=0.042, relwidth=0.05)

    def _create_color_pickers(self):
        self.max_color  = tk.StringVar()
        self._max_btn   = tk.Button(self, text="", command=self._pick_color_max, relief='flat')
        self._max_btn.place(relx=0.515, rely=self.COMMON_Y_POS+0.05, relheight=0.015, relwidth=0.05)

        self.min_color  = tk.StringVar()
        self._min_btn   = tk.Button(self, text="", command=self._pick_color_min, relief='flat')
        self._min_btn.place(relx=0.57, rely=self.COMMON_Y_POS+0.05, relheight=0.015, relwidth=0.05)
        
        self.mean_color = tk.StringVar()
        self._mean_btn  = tk.Button(self, text="", command=self._pick_color_mean, relief='flat')
        self._mean_btn.place(relx=0.624, rely=self.COMMON_Y_POS+0.05, relheight=0.015, relwidth=0.05)

        self._reset_color_pickers()

    def _pick_color_max(self):
        self._pick_color("max")
    
    def _pick_color_min(self):
        self._pick_color("min")

    def _pick_color_mean(self):
        self._pick_color("mean")    

    def _pick_color(self, picker):
        col = colorchooser.askcolor(initialcolor='#000000') # Change color here
        # print(col[1]) # Returns a tuple --> ((255, 255, 255),'#ffffff')
        
        # If a user cancels in the middle of choosing a color, an empty string is returned
        if(col[1]):  
            if(picker == "max"):        
                self.max_color.set(col[1])
                self._max_btn['bg']  = col[1]
            elif(picker == "min"):
                self.min_color.set(col[1])
                self._min_btn['bg']  = col[1]
            else:
                self.mean_color.set(col[1])
                self._mean_btn['bg'] = col[1]
   
    def _get_colors(self):
        return self.max_color.get(), self.min_color.get(), self.mean_color.get()

    def _reset_color_pickers(self, mx="#50514f", mi="#cb904d", mn="#71a2b6"):
        # Default plotting colors
        self.max_color.set(mx)
        self.min_color.set(mi)
        self.mean_color.set(mn)
        self._max_btn['bg']  = mx
        self._min_btn['bg']  = mi
        self._mean_btn['bg'] = mn

    def _create_date_picker(self):
        tk.Label(self, text="Choose date:", 
                 bg=self.BACKGROUND_COLOR, fg="white")\
          .place(relx=0.685, rely=self.COMMON_Y_POS, relheight=0.048)

        self._calendar = MyDateEntry(self, borderwidth=1, width=6)
        self._calendar.place(relx=0.772, rely=self.COMMON_Y_POS, relheight=0.04)

    def _create_get_csv_button(self):
        ttk.Button(self, text="Save as CSV", command=self._save_csv)\
           .place(relx=self.COMMON_X_POS, rely=0.052, relwidth=0.1)

    def _create_load_csv_button(self):
        ttk.Button(self, text="Load CSV", command=self._load_csv)\
           .place(relx=self.COMMON_X_POS, rely=0.122, relwidth=0.1)

    def _create_fetching_controls(self):
        ttk.Separator(self, orient='horizontal')\
           .place(relx=self.COMMON_X_POS, rely=0.202, relwidth=0.1)
        
        ''' Create 3 entries for the USER, KEY, and FEED to fetch data from.
            Each entry is associated with a label that describes what it is,
            and each entry is binded to the enter key for automatic passage 
            to the next, "UX-ish" '''

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
        self._assign_drawing("D")

    def _draw_week(self):
        self._assign_drawing("W")

    def _draw_month(self):
        self._assign_drawing("M")

    def _assign_drawing(self, picker):
        mx, mi, mn    = self._get_checks()
        d, m, y       = self._get_date()
        cmx, cmi, cmn = self._get_colors()
        if(self._parser.FETCHED and\
          (self.CURRENT_GRAPH != picker or\
          (mx, mi, mn) != self.MAX_MIN_MEAN or\
          (d, m, y) != self.DATE or\
          (cmx, cmi, cmn) != self.COLORS)):
            
            self._draw(self._parser._df, (mx, mi, mn), kind=picker, date=(d, m, y))
            self.CURRENT_GRAPH = picker
            self.MAX_MIN_MEAN = (mx, mi, mn)
            self.DATE = (d, m, y)
            self.COLORS = (cmx, cmi, cmn)

    # Data ; values(max, min, mean) ; kind=day/week/month ; date(day, month, year)
    def _draw(self, data, values, kind="D", date=(0, 0, 0)):
        mx_mi_mn = ["mx", "mi", "mn"]
        colours_ = list(self._get_colors())
        day, month, year = date
        self._fig.clear()

        if(kind == "D"): # Plotting a day
            for i, value in enumerate(values):
                if value:
                    printable = data.loc[(data["Day"] == day) &\
                                         (data["Month"] == month) &\
                                         (data["Year"] == year)]
                    self._fig.plot(printable[mx_mi_mn[i]], color=colours_[i])
        
        elif(kind == "W"): # Plotting a week 
            days_in_month = self._days_in_month(year=year, month=month)
            if(days_in_month - day <= 0):
                # Since a week starting at the 30th of january isn't [30, 31, 32, 33, ..]
                # days_to_plot are calculated to solve this specific problem
                days_to_plot  = [x for x in range(day, days_in_month+1)]\
                               +[x for x in range(1, 7-days_in_month+day+1)]
            else:
                days_to_plot = [x for x in range(day, day+7)]
            possible_months = list((month, month+1))

            for i, value in enumerate(values):
                if value:
                    printable = data[(data["Day"].isin(days_to_plot)) &\
                                     (data["Month"].isin(possible_months)) &\
                                     (data["Year"]== year)]
                    # The hour indexing isn't unique so if we plot according to it
                    # we end up with a messed up plot, so we need numeric indexing
                    printable.reset_index(inplace=True) 
                    self._fig.plot(printable[mx_mi_mn[i]], color=colours_[i])            
        
        else: # Plotting a month
            for i, value in enumerate(values):
                if value:
                    printable = data[(data["Month"] == month) &\
                                         (data["Year"]== year)]
                    # The hour indexing isn't unique so if we plot according to it
                    # we end up with a messed up plot, so we need numeric indexing
                    printable.reset_index(inplace=True) 
                    self._fig.plot(printable[mx_mi_mn[i]], color=colours_[i])
        
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

    @staticmethod
    def _days_in_month(year="1998", month="1"):
        return monthrange(year, month)[1]

    def _authenticate(self, *args):
        user, feed, key = self._get_inputs()   
        if(len(user) and len(feed) and len(key)):
            self._parser.fetch_data(user, feed, key)
            self._reset_inputs()
        else:
            self._show_message("Please fill in your data", "ERROR", "info")

    def _reset_inputs(self):
        self.USER.set("")
        self.FEED.set("")
        self.KEY.set("") 


    def _get_inputs(self):
        return self.USER.get(), self.FEED.get(), self.KEY.get()

    def _get_checks(self):
        return self._check_Max.get(), self._check_Min.get(), self._check_Mean.get()

    def _get_date(self):
        m, d, y = self._calendar.get().split('/')
        # Don't think we'll read anything after 2050, or before 1950 \__(°~°)__/
        if(int(y) < 50): 
            y = "20"+y
        else:
            y = "19"+y
        return int(d), int(m), int(y)

    def _save_csv(self):
        self._parser.output_csv()

    def _load_csv(self):
        self._parser.load_from_file()

    @staticmethod
    def _show_message(msg, title, kind="info"):
        if(kind == "info"):
            messagebox.showinfo(message=msg, title=title)
        elif(kind == "err"):
            messagebox.showerror(message=msg, title=title)
        else: # "warn"
            messagebox.showwarning(message=msg, title=title)
