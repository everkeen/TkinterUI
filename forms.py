"""Module for Tkinter UI forms."""

from typing import Any
import tkinter as tk
from tkinter import filedialog, colorchooser
import ast

__all__ = ["Form"]


class Form(tk.Frame):
    """Class representing a form in the Tkinter UI."""

    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.master = master


class FormElement(tk.Frame):
    """Base class for an element in the form."""

    _var: tk.Variable

    def __init__(self, master: tk.Misc, default: Any | None = None):
        super().__init__(master)
        self.master = master
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets of the form element.
        WARNING: This method should clear all children of the element.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @property
    def value(self):
        """Get the value of the form element."""
        return self._var.get() if hasattr(self, "_var") else None

    @value.setter
    def value(self, new_value: Any):
        """Set the value of the form element."""
        if hasattr(self, "_var"):
            self._var.set(new_value)
        else:
            raise AttributeError("This form element does not have a variable to set.")


class StringForm(FormElement):
    """Class for a string input form element."""

    def __init__(self, master: tk.Misc, default: str | None = None):
        super().__init__(master, default)
        self._var = tk.StringVar(value=default)

    def regen_widgets(self):
        """Regenerate the widgets for the string input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the string value of the form element."""
        return super().value

    @value.setter
    def value(self, new_value: str | None):
        """Set the string value of the form element."""
        super().value = new_value


class IntForm(FormElement):
    """Class for an integer input form element."""

    def __init__(self, master: tk.Misc, default: int | None = None):
        super().__init__(master, default)
        self._var = tk.IntVar(value=default)

    def regen_widgets(self):
        """Regenerate the widgets for the integer input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the integer value of the form element."""
        return super().value

    @value.setter
    def value(self, new_value: int | None):
        """Set the integer value of the form element."""
        super().value = new_value


class FloatForm(FormElement):
    """Class for a float input form element."""

    def __init__(self, master: tk.Misc, default: float | None = None):
        super().__init__(master, default)
        self._var = tk.DoubleVar(value=default)

    def regen_widgets(self):
        """Regenerate the widgets for the float input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the float value of the form element."""
        return super().value

    @value.setter
    def value(self, new_value: float | None):
        """Set the float value of the form element."""
        super().value = new_value


class BoolForm(FormElement):
    """Class for a boolean input form element."""

    def __init__(self, master: tk.Misc, default: bool | None = None):
        super().__init__(master, default)
        self._var = tk.BooleanVar(value=default)

    def regen_widgets(self):
        """Regenerate the widgets for the boolean input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.checkbutton = tk.Checkbutton(self, variable=self._var)
        self.checkbutton.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the boolean value of the form element."""
        return super().value

    @value.setter
    def value(self, new_value: bool | None):
        """Set the boolean value of the form element."""
        super().value = new_value


class ListForm(FormElement):
    """Class for a list input form element."""

    def __init__(self, master: tk.Misc, default: list | None = None):
        super().__init__(master, default)
        self._var = tk.StringVar(value=",".join(default) if default else "")

    def regen_widgets(self):
        """Regenerate the widgets for the list input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the list value of the form element."""
        return self._var.get().split(",") if self._var.get() else []

    @value.setter
    def value(self, new_value: list | None):
        """Set the list value of the form element."""
        if new_value is not None:
            self._var.set(",".join(new_value))
        else:
            self._var.set("")


class DictForm(FormElement):
    """Class for a dictionary input form element."""

    def __init__(self, master: tk.Misc, default: dict | None = None):
        super().__init__(master, default)
        self._var = tk.StringVar(value=str(default) if default else "{}")

    def regen_widgets(self):
        """Regenerate the widgets for the dictionary input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the dictionary value of the form element."""
        return ast.literal_eval(self._var.get()) if self._var.get() else {}

    @value.setter
    def value(self, new_value: dict | None):
        """Set the dictionary value of the form element."""
        if new_value is not None:
            self._var.set(str(new_value))
        else:
            self._var.set("{}")


class ChoiceForm(FormElement):
    """Class for a choice input form element."""

    def __init__(self, master: tk.Misc, choices: list[str], default: str | None = None):
        super().__init__(master, default)
        self._var = tk.StringVar(value=default if default else choices[0])
        self.choices = choices

    def regen_widgets(self):
        """Regenerate the widgets for the choice input."""
        for widget in self.winfo_children():
            widget.destroy()
        if not isinstance(self.choices, list) or not self.choices:
            raise ValueError("Choices must be a non-empty list.")
        if not isinstance(self._var, tk.StringVar):
            raise TypeError("Variable must be a StringVar.")
        self.option_menu = tk.OptionMenu(self, self._var, *self.choices)
        self.option_menu.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the selected choice value."""
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        """Set the selected choice value."""
        if new_value in self.choices:
            self._var.set(new_value)
        else:
            raise ValueError(f"Value '{new_value}' is not in the choices.")

    def add_choice(self, choice: str):
        """Add a new choice to the choice input."""
        if choice not in self.choices:
            self.choices.append(choice)
            self.option_menu["menu"].add_command(
                label=choice, command=lambda value=choice: self._var.set(value)
            )
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' already exists.")

    def remove_choice(self, choice: str):
        """Remove a choice from the choice input."""
        if choice in self.choices:
            self.choices.remove(choice)
            menu = self.option_menu["menu"]
            menu.delete(choice)
            if self._var.get() == choice:
                self._var.set(self.choices[0] if self.choices else "")
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' does not exist.")

    def clear_choices(self):
        """Clear all choices from the choice input."""
        self.choices.clear()
        self._var.set("")
        self.option_menu["menu"].delete(0, "end")
        self.regen_widgets()


class MultiChoiceForm(FormElement):
    """Class for a multi-choice input form element."""

    def __init__(
        self, master: tk.Misc, choices: list[str], default: list[str] | None = None
    ):
        super().__init__(master, default)
        self._var = tk.StringVar(value=",".join(default) if default else "")
        self.choices = choices

    def regen_widgets(self):
        """Regenerate the widgets for the multi-choice input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        for choice in self.choices:
            self.listbox.insert(tk.END, choice)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    @property
    def value(self):
        """Get the selected choices."""
        return [self.listbox.get(i) for i in self.listbox.curselection()]

    @value.setter
    def value(self, new_value: list[str] | None):
        """Set the selected choices."""
        if new_value is not None:
            for i in range(self.listbox.size()):
                if self.listbox.get(i) in new_value:
                    self.listbox.select_set(i)
                else:
                    self.listbox.select_clear(i)
        else:
            self.listbox.select_clear(0, tk.END)
            self._var.set("")
        self._var.set(",".join(self.value))
        self.regen_widgets()
        if not isinstance(self.choices, list) or not self.choices:
            raise ValueError("Choices must be a non-empty list.")
        if not isinstance(self._var, tk.StringVar):
            raise TypeError("Variable must be a StringVar.")
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    def _on_select(self, _):
        """Handle selection changes in the listbox."""
        selected = self.value
        self._var.set(",".join(selected))
        if not selected:
            self._var.set("")
        else:
            self._var.set(",".join(selected))
        self.regen_widgets()

    def add_choice(self, choice: str):
        """Add a new choice to the multi-choice input."""
        if choice not in self.choices:
            self.choices.append(choice)
            self.listbox.insert(tk.END, choice)
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' already exists.")

    def remove_choice(self, choice: str):
        """Remove a choice from the multi-choice input."""
        if choice in self.choices:
            self.choices.remove(choice)
            index = self.listbox.get(0, tk.END).index(choice)
            self.listbox.delete(index)
            if self._var.get() == choice:
                self._var.set(self.choices[0] if self.choices else "")
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' does not exist.")

    def clear_choices(self):
        """Clear all choices from the multi-choice input."""
        self.choices.clear()
        self.listbox.delete(0, tk.END)
        self._var.set("")
        self.regen_widgets()


class FileForm(FormElement):
    """Class for a file input form element."""

    def __init__(self, master: tk.Misc, default: str | None = None):
        super().__init__(master, default)
        self._var = tk.StringVar(value=default if default else "")

    def regen_widgets(self):
        """Regenerate the widgets for the file input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.button = tk.Button(self, text="Browse", command=self.browse_file)
        self.button.pack(pady=5)

    def browse_file(self):
        """Open a file dialog to select a file."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self._var.set(file_path)

    @property
    def value(self):
        """Get the file path value of the form element."""
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        self._var.set(new_value if new_value else "")
        self.regen_widgets()

    def clear(self):
        """Clear the file input."""
        self._var.set("")
        self.regen_widgets()

    def reset(self):
        """Reset the file input to its default state."""
        self.clear()


class DirectoryForm(FileForm):
    """Class for a directory input form element."""

    def browse_file(self):
        """Open a directory dialog to select a directory."""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self._var.set(dir_path)

    @property
    def value(self):
        """Get the directory path value of the form element."""
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        self._var.set(new_value if new_value else "")
        self.regen_widgets()


class PathForm(FormElement):
    """Class for a path input form element."""

    def __init__(self, master: tk.Misc, default: str | None = None):
        super().__init__(master, default)
        self._var = tk.StringVar(value=default if default else "")

    def regen_widgets(self):
        """Regenerate the widgets for the path input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.button = tk.Button(self, text="Browse", command=self.browse_file)
        self.button.pack(pady=5)

    def browse_file(self):
        """Open a file dialog to select a file or directory."""
        file_path = filedialog.askopenfilename() or filedialog.askdirectory()
        if file_path:
            self._var.set(file_path)

    @property
    def value(self):
        """Get the path value of the form element."""
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        self._var.set(new_value if new_value else "")
        self.regen_widgets()


class RadioForm(FormElement):
    """Class for a radio button input form element."""

    def __init__(self, master: tk.Misc, choices: list[str], default: str | None = None):
        super().__init__(master, default)
        self._var = tk.StringVar(value=default if default else choices[0])
        self.choices = choices

    def regen_widgets(self):
        """Regenerate the widgets for the radio button input."""
        for widget in self.winfo_children():
            widget.destroy()
        for choice in self.choices:
            rb = tk.Radiobutton(self, text=choice, variable=self._var, value=choice)
            rb.pack(anchor=tk.W)

    @property
    def value(self):
        """Get the selected radio button value."""
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        """Set the selected radio button value."""
        if new_value in self.choices:
            self._var.set(new_value)
        else:
            raise ValueError(f"Value '{new_value}' is not in the choices.")

    def add_choice(self, choice: str):
        """Add a new choice to the radio button input."""
        if choice not in self.choices:
            self.choices.append(choice)
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' already exists.")

    def remove_choice(self, choice: str):
        """Remove a choice from the radio button input."""
        if choice in self.choices:
            self.choices.remove(choice)
            if self._var.get() == choice:
                self._var.set(self.choices[0] if self.choices else "")
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' does not exist.")

    def clear_choices(self):
        """Clear all choices from the radio button input."""
        self.choices.clear()
        self._var.set("")
        self.regen_widgets()


class ColorForm(FormElement):
    """Class for a color input form element."""

    def __init__(self, master: tk.Misc, default: str | None = None):
        super().__init__(master, default)
        self._var = tk.StringVar(value=default if default else "#FFFFFF")

    def regen_widgets(self):
        """Regenerate the widgets for the color input."""
        for widget in self.winfo_children():
            widget.destroy()
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.button = tk.Button(self, text="Select Color", command=self.select_color)
        self.button.pack(pady=5)

    def select_color(self):
        """Open a color dialog to select a color."""
        color = colorchooser.askcolor(color=self._var.get())
        if color[1]:
            self._var.set(color[1])

    @property
    def value(self):
        """Get the selected color value."""
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        self._var.set(new_value if new_value else "#FFFFFF")
        self.regen_widgets()

class ColorPickerForm(ColorForm):
    """Class for a color picker input form element."""

    def regen_widgets(self):
        """Regenerate the widgets for the color picker input."""
        super().regen_widgets()
        self.color_display = tk.Label(self, bg=self._var.get(), width=20, height=2)
        self.color_display.pack(pady=5)
        self._var.trace_add("write", self.update_color_display)

    def update_color_display(self, *_):
        """Update the color display when the variable changes."""
        self.color_display.config(bg=self._var.get())
