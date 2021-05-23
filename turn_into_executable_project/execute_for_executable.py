#!/usr/bin/env python3

# https://pyinstaller.readthedocs.io/en/stable/usage.html
import PyInstaller.__main__

PyInstaller.__main__.run([
	"main_.py", 			# Your application that you want to turn into an executable
	"--icon=images/icon.ico",	# The path to the icon for your app
	"--name=Temp_viz",		# The name of the executable
	"--onefile"			# whether get a bunch of directories and files or on file 
					# (in this case, one file)
])
