#!/usr/bin/env python3

from GUI import GUI

class main_:
    ''' Class that launches everything '''

    def __init__(self, *args, **kwargs):
        self._initialise_gui(*args, **kwargs)
        self._update_display()
        self._gui.mainloop()

    def _initialise_gui(self, *args, **kwargs):
        self._gui = GUI(*args, **kwargs)

    def _update_display(self):
        self._gui.after(1, self._update_display) # Loop forever

if __name__ == '__main__':
    main_()