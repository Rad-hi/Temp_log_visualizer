#!/usr/bin/env python3

from Adafruit_IO import Client
import json
import datetime
import pandas as pd
from tkinter import filedialog

class parser:

	def __init__(self, filename='', fetched=False):
		self.FETCHED = fetched
		self.filename = filename
		if(filename):
			self._load_data()

	def fetch_data(self, user, feed, key):
		if(not self.FETCHED):
			try:
				adafruit_client = Client(user, key)
				all_data = adafruit_client.data(feed) # This is all the existing data in broker
				self._create_dataframe(all_data) # Some smart parsing shall be done !!
				self.FETCHED = True
			except:
				print("Invalid info") # MessageBox info. make it visual!
		else:
			print("Already fetched!")# MessageBox info. make it visual!

	def _create_dataframe(self, data):

		df = pd.DataFrame()

		for d in data:
			df_i = pd.DataFrame(json.loads(d.value)).T 

			date_ = self._get_datetime(d.created_at)
			df_i["Day"] = date_.day
			df_i["Month"] = date_.month
			df_i["Year"] = date_.year
			df_i["Time"] = date_.time()

			df_i.reset_index(inplace=True)
			df_i = df_i.rename(columns = {'index':'Hour'})
			
			df = df.append(df_i, ignore_index=True)

		self._df = df

		print("Done parsing!")
		print(self._df.head())

	@staticmethod
	def _get_datetime(date_str):
		date = date_str[:19].replace("T", " ")
		return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

	def _load_data(self):
		self._df = pd.read_csv(self.filename)
		self.FETCHED = True

	def output_csv(self, filename):
		self._df.to_csv(f"{filename}.csv")


	@classmethod
	def from_file(cls, filename='', *args, **kwargs):
		if not filename:
			filename = filedialog.askopenfilename(defaultextension='.csv',
												  filetypes=(('CSV Files', '*.csv'),
												     		 ('All Files', '*.*')))
			extension = filename[filename.rfind('.'):]
			if extension != '.csv':
				message = f'Invalid format {extension} - only .csv files allowed.'
				messagebox.showinfo(message=message, title="ERROR")
		return cls(filename, *args, **kwargs)
