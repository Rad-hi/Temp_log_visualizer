#!/usr/bin/env python3

from GUI import GUI

class Controller:
    def __init__(self, *args, **kwargs):
        self._initialise_display(*args, **kwargs)
        self._update_display()
        self._gui.mainloop()

    def _initialise_display(self, *args, **kwargs):
        self._gui = GUI(*args, **kwargs)

    def _update_display(self):
        self._gui.after(1, self._update_display) # continue looping

if __name__ == '__main__':
    Controller()