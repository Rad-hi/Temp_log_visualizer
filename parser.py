#!/usr/bin/env python3

from Adafruit_IO import Client
import json
import datetime
import pandas as pd
from tkinter import filedialog, messagebox

class parser:
	''' This class contains all file handeling functionalities '''

	FETCHED = False
	# Holds the latest data that have been fetched
	USER 	= ('')*2

	def fetch_data(self, user, feed, key):
		if(not self.FETCHED):
			if((user, key) != self.USER):
				try:
					adafruit_client = Client(user, key)
					all_data = adafruit_client.data(feed) # This is all the existing data in broker
					self._create_dataframe(all_data) # Some smart parsing shall be done !!
					self.FETCHED = True
					self.USER    = (user, key)
				except:
					self._show_message(msg="Unable to fetch!", title="ERROR", kind="err")
			else:
				self._show_message(msg="User's data already fetched!", title="NOTE", kind="info")
		else:
			msg = "Data already exists, do you want to override it?"
			response = self._ask_confirmation(title="Confirmation!", msg=msg)
			if(response is not None and response == "yes"):
				self.FETCHED = False
				self.fetch_data(user, feed, key)

	def _create_dataframe(self, data):

		df = pd.DataFrame()

		for i in range(len(data)-1, -1, -1):
			df_i = pd.DataFrame(json.loads(data[i].value)).T 
			date_ = self._get_datetime(data[i].created_at)
			df_i["Day"] = date_.day
			df_i["Month"] = date_.month
			df_i["Year"] = date_.year
			df_i["Time"] = date_.time()			
			df = df.append(df_i)
		
		self._df = df

		self._show_message(msg="Data fetched successfully!", title="SUCCESS", kind="info")

	def output_csv(self, filename=""):
		if(self.FETCHED): # There's actually data to save
			filename = filedialog.asksaveasfilename(defaultextension='.csv',
												    filetypes=(('CSV Files', '*.csv'),
												     		   ('All Files', '*.*')))
			if(filename):
				self._df.to_csv(filename)
		else:
			self._show_message(msg="No data to save!", title="NOTE", kind="info")

	def load_from_file(self):
		if(self.FETCHED):
			self._show_message(msg="You already have data loaded!", title="WARNING", kind="warn")
	
		filename = filedialog.askopenfilename(defaultextension='.csv',
											  filetypes=(('CSV Files', '*.csv'),
											     		 ('All Files', '*.*')))
		if(filename):
			extension = filename[filename.rfind('.'):]
			if extension != '.csv':
				message = f'Invalid format {extension} - only .csv files allowed.'
				messagebox.showinfo(message=message, title="ERROR")
			else:
				self._load_data(filename)

	def _load_data(self, filename):
		self._df = pd.read_csv(filename, index_col=0)
		self.FETCHED = True

	@staticmethod
	def _show_message(msg, title, kind="info"):
		if(kind == "info"):
			messagebox.showinfo(message=msg, title=title)
		elif(kind == "err"):
			messagebox.showerror(message=msg, title=title)
		else: # "warn"
			messagebox.showwarning(message=msg, title=title)

	@staticmethod
	def _ask_confirmation(title, msg):
		return messagebox.askquestion(title, msg)
	
	@staticmethod
	def _get_datetime(date_str):
		date = date_str[:19].replace("T", " ")
		return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")