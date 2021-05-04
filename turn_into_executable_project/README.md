# This project is slightly different from the original one, all to make an executable!

---

## How it's supposed to be done:

Getting an executable file from this on my linux machine (Pop!Os) wasn't easy, but I finally got it to work, and here's how:

First of all, an executable file is an **environement independant** file that, in a system that doesn't have any project dependencies installed, **not even Python**, would run perfectly. In my case, anyone taking my executable file ***dist/Temp_viz*** and running it on a debian machine will "hopefully" get my app popping-up for them.

Now, how to make my project (or any Python project into an executable)?

The first step ,right after getting a working project, is to install pyinstaller:

```
$pip install pyinstaller
```

Then, you go to your project's folder (where the app file is) and you either run:

```
$pyinstaller MyAppName.py 
```

In my case it would be:

```
$pyinstaller main_.py
```

Another option is that you start playing around with the options in the command-line, or even better, write a python script that executes the commands for you, and you just run that python script. I personally created the python script named **execute_for_executable.py** which looks like this:

```python
#!/usr/bin/env python3

# https://pyinstaller.readthedocs.io/en/stable/usage.html
import PyInstaller.__main__

PyInstaller.__main__.run([
	"main_.py",			# Your application that you want to turn into an executable
	"--icon=images/icon.png",	# The path to the icon for your app
	"--name=Temp_viz",		# The name of the executable
	"--onefile"			# whether get a bunch of directories and files or on file 
					# (in this case, one file)
])
```

You can learn more about these options from [where I learned myself](https://pyinstaller.readthedocs.io/en/stable/usage.html).

After running this code, it'll take sometime depending on your dependencies, but after it finishes, you can find your executable  **under the dist/ folder named with the name you've specified for your executable, or your main app's name**.

The build process would produce a **build/** and **dist/** folders, as well as a **YourAppName.spec** file. (I removed the /build folder since it was too big and unnecessary for the executable to run)

Now, to run the executable you have to locate it, and type in the command:

```
$./Path_to_the_location/Executable_name 
```
In my case, I executed:

```
$./dist/Temp_viz
```
> Note the point before the / !

---

## Problems that I faced:

The first problem that I faced was with the Adafruit_IO library, and that's why you see it in this project's folder with a slightly modified name/content and not in the main folder, and I'll tell you why that's the case just now.

When runnin the ```execute_for_executable.py``` script, the building process finished successfully but whenever I ran the executable, I get this error:

```
The 'Adafruit_IO' distribution was not found and is required by the application
```

Which was a strange error since I obviously imported it and got my project working as I expected. 

Briefly, pyinstaller needs to be told where are some libraries sometimes with the ```--hidden-import MODULENAME``` option, but that still didn't solve it. Anyway, I simply couldn't solve this problem with pyinstaller alone so I needed to hack my way out of this problem, and my solution was to copy the Adafrui_IO lib into my folder, change its name to Adafruit_IO**_** and make these changes to its client.py file:

```python
from time import struct_time
import json
#import platform
#####################
## Commented this! ##
#import pkg_resources
##                 ##
#####################

# import logging

import requests

from .errors import RequestError, ThrottlingError
from .model import Data, Feed, Group

#########################################################
## Commented all this and made it static! (down below) ##
##                                                     ##
"""
# set outgoing version, pulled from setup.py
version = pkg_resources.require("Adafruit_IO")[0].version
default_headers = {
    'User-Agent': 'AdafruitIO-Python/{0} ({1}, {2} {3})'.format(version,
                                                                platform.platform(),
                                                                platform.python_implementation(),
                                                                platform.python_version())
}
"""
##						       ##
#########################################################

############################################################
## I figured out these values by adding a print statement ##
##     to the original code, and running my app once!     ##
default_headers= {'User-Agent': 'AdafruitIO-Python/2.5.0 (Linux-5.11.0-7612-generic-x86_64-with-glibc2.29, CPython 3.8.5)'}
##							  ##
############################################################
``` 

Then changed the call to Adafruit_IO in my code to Adafruit_IO**_** !

--

Then, I tried rebuilding the project and now this error is popping:

```
ModuleNotFoundError: No module named ‘babel.numbers’
```

You can find the solution to that in this blog [https://tekrecipes.com/2019/04/17/modulenotfounderror-no-module-named-babel-numbers/](https://tekrecipes.com/2019/04/17/modulenotfounderror-no-module-named-babel-numbers/) but it's a really simple one.

--

And now it works (after rebuilding ofcourse ...)

---

## Running the executable:

Now take the executable file and run it anyway in your Linux machine(Or any other Linux machine).
