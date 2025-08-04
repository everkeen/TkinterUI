import tkinter as tk


class DockablePanedWindow(tk.PanedWindow):
    """Class representing a dockable paned window."""

    def __init__(self, master: tk.Misc, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.dockable = True
        self.docked = False
