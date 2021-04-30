#!/usr/bin/env python3

from GUI import GUI

class main_:
    def __init__(self, *args, **kwargs):
        self._initialise_display(*args, **kwargs)
        self._update_display()
        self._gui.mainloop()

    def _initialise_display(self, *args, **kwargs):
        self._gui = GUI(*args, **kwargs)

    def _update_display(self):
        self._gui.after(1, self._update_display) # Loop forever

if __name__ == '__main__':
    main_()