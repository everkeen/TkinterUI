import tkinter as tk


class DockablePanedWindow(tk.PanedWindow):
    """Class representing a dockable paned window."""

    _var: tk.StringVar

    def __init__(self, master: tk.Misc, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.dockable = True
        self.docked = False
        self._var = tk.StringVar(value="Horizontal")
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate widgets in the dockable window."""
        for widget in self.winfo_children():
            widget.destroy()

        align_dropdown = tk.OptionMenu(self, self._var, "Horizontal", "Vertical")
        align_dropdown.pack(fill=tk.X, padx=5, pady=5)
        self.add(align_dropdown)
        self._var.trace_add("write", self._on_align_change)

    def _on_align_change(self, *args):
        """Handle changes in alignment."""
        if self._var.get() == "Horizontal":
            self.configure(orient=tk.HORIZONTAL)
        else:
            self.configure(orient=tk.VERTICAL)
