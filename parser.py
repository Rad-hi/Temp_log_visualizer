#!/usr/bin/env python3

from Adafruit_IO import Client
import json
import datetime
import pandas as pd

class parser:
	"""
	def __init__():
		pass
	"""
	
	def fetch_data(self, user, feed, key):
		adafruit_client = Client(user, key)
		all_data = adafruit_client.data(feed) # This is all the existing data in broker
		for data in all_data:
			print(data.value)

	def load_data(self):
		pass

	def output_csv(self, filename):
		pass

	def _create_dataframe(self, data):
		pass


"""
	@classmethod
	def from_file(cls, filename='', *args, **kwargs):
    	if not filename:
			filename = filedialog.askopenfilename(defaultextension='.obj',
			        filetypes=(('CSV Files', '*.csv'),
			                   ('All Files', '*.*')))
			extension = filename[filename.rfind('.'):]
			if extension != '.csv':
				message = f'Invalid format {extension} - only .csv files allowed.'
				messagebox.showinfo(message=message, title="ERROR")
		return cls(filename, *args, **kwargs)
"""