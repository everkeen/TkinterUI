"""Module for Tkinter UI forms."""

from typing import Any
import tkinter as tk
from tkinter import filedialog, colorchooser
import ast
import enum
from http import client as httpclient
import logging
import json

__all__ = ["Form"]


class SubmitMode(enum.Enum):
    """Enum for form submission modes."""

    HTTP_POST = "http_post"
    HTTP_PUT = "http_put"
    HTTP_DELETE = "http_delete"
    HTTP_PATCH = "http_patch"
    RUN_CODE = "run_code"
    LOG = "log"


class Form(tk.Frame):
    """Class representing a form in the Tkinter UI."""

    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.master = master
        self._elements = []

    def add_element(self, element: "FormElement"):
        """Add a form element to the form."""
        self._elements.append(element)
    
    def add_elements(self, *elements: "FormElement"):
        """Add multiple form elements to the form."""
        for element in elements:
            self.add_element(element)

    def process_form(self) -> dict[str, Any]:
        """Process the form and return a dictionary of element names and values."""
        results = {}
        for element in self._elements:
            print(
                f"Processing element: {element.name if hasattr(element, 'name') else element.__class__.__name__}"
            )
            # Check if the element has a name and value before adding
            if isinstance(element, FormElement) and element.name:
                try:
                    results[element.name] = element.value
                except AttributeError as e:
                    logging.error(f"TKUI: Error getting value for {element.name}: {e}")
        return results

    def submit(
        self, mode: SubmitMode = SubmitMode.HTTP_POST, url_file_code: str | None = None
    ):
        """Submit the form data based on the specified mode."""
        data = self.process_form()
        if not url_file_code and mode != SubmitMode.LOG:
            raise ValueError("url_file_code must be provided for non-log submission.")
        match mode:
            case SubmitMode.HTTP_POST:
                if not url_file_code:
                    raise ValueError(
                        "url_file_code must be provided for non-log submission."
                    )
                conn = httpclient.HTTPConnection(host=url_file_code)
                try:
                    conn.request("POST", "/", body=json.dumps(data))
                    response = conn.getresponse()
                    return response.read()
                except Exception as e:
                    raise RuntimeError(f"Error occurred during HTTP POST: {e}") from e
                finally:
                    conn.close()
            case SubmitMode.HTTP_PUT:
                if not url_file_code:
                    raise ValueError(
                        "url_file_code must be provided for non-log submission."
                    )
                conn = httpclient.HTTPConnection(host=url_file_code)
                try:
                    conn.request("PUT", "/", body=json.dumps(data))
                    response = conn.getresponse()
                    return response.read()
                except Exception as e:
                    raise RuntimeError(f"Error occurred during HTTP PUT: {e}") from e
                finally:
                    conn.close()
            case SubmitMode.HTTP_DELETE:
                if not url_file_code:
                    raise ValueError(
                        "url_file_code must be provided for non-log submission."
                    )
                conn = httpclient.HTTPConnection(host=url_file_code)
                try:
                    conn.request("DELETE", "/", body=json.dumps(data))
                    response = conn.getresponse()
                    return response.read()
                except Exception as e:
                    raise RuntimeError(f"Error occurred during HTTP DELETE: {e}") from e
                finally:
                    conn.close()
            case SubmitMode.HTTP_PATCH:
                if not url_file_code:
                    raise ValueError(
                        "url_file_code must be provided for non-log submission."
                    )
                conn = httpclient.HTTPConnection(host=url_file_code)
                try:
                    conn.request("PATCH", "/", body=json.dumps(data))
                    response = conn.getresponse()
                    return response.read()
                except Exception as e:
                    raise RuntimeError(f"Error occurred during HTTP PATCH: {e}") from e
                finally:
                    conn.close()
            case SubmitMode.RUN_CODE:
                if not url_file_code:
                    raise ValueError(
                        "url_file_code must be provided for non-log submission."
                    )
                globals_dict = {
                    "data": data,
                }
                globals_dict.update(data)  # Add form data to globals
                # ban_regex: str = (
                #     r"(?i)import|from|exec|eval|__import__|globals|locals|locals\(\)|globals\(\)|compile"  # if re.search(ban_regex, url_file_code) is not None:
                # )
                #     raise ValueError("The provided code contains banned keywords.")
                try:
                    exec(url_file_code, globals_dict)
                    return globals_dict.get("result", None)
                except Exception as e:
                    raise RuntimeError(f"Error occurred while running code: {e}") from e
            case SubmitMode.LOG:
                logging.info("TKUI: Form submitted with data: %s", data)


class FormElement(tk.Frame):
    """Base class for an element in the form."""

    _var: tk.Variable | None = None

    def __init__(self, master: tk.Misc, name: str, default: Any | None = None):
        super().__init__(master)
        self.master = master
        self.name = name

    def regen_widgets(self):
        """Regenerate the widgets of the form element.
        WARNING: This method should clear all children of the element.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @property
    def value(self):
        """Get the value of the form element."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        # Ensure _var is a valid Tkinter variable before calling .get()
        return self._var.get() if hasattr(self, "_var") else None

    @value.setter
    def value(self, new_value: Any):
        """Set the value of the form element."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        if hasattr(self, "_var") and self._var is not None:
            self._var.set(new_value)
        else:
            raise AttributeError("This form element does not have a variable to set.")


class StringForm(FormElement):
    """Class for a string input form element."""

    def __init__(self, master: tk.Misc, name: str, default: str | None = None):
        # Initialize the variable before calling super().__init__
        self._var = tk.StringVar(value=default if default is not None else "")
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the string input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)


class IntForm(FormElement):
    """Class for an integer input form element."""

    def __init__(self, master: tk.Misc, name: str, default: int | None = None):
        # Initialize the variable before calling super().__init__
        self._var = tk.IntVar(value=default if default is not None else 0)
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the integer input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)


class FloatForm(FormElement):
    """Class for a float input form element."""

    def __init__(self, master: tk.Misc, name: str, default: float | None = None):
        # Initialize the variable before calling super().__init__
        self._var = tk.DoubleVar(value=default if default is not None else 0.0)
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the float input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)


class BoolForm(FormElement):
    """Class for a boolean input form element."""

    def __init__(self, master: tk.Misc, name: str, default: bool | None = None):
        # Initialize the variable before calling super().__init__
        self._var = tk.BooleanVar(value=default if default is not None else False)
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the boolean input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.checkbutton = tk.Checkbutton(self, variable=self._var)
        self.checkbutton.pack(fill=tk.X, padx=5, pady=5)


class ListForm(FormElement):
    """Class for a list input form element."""

    def __init__(self, master: tk.Misc, name: str, default: list | None = None):
        # Initialize the variable before calling super().__init__
        value = ",".join(map(str, default)) if default is not None else ""
        self._var = tk.StringVar(value=value)
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the list input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the list value of the form element."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        # Safely split the string value
        return self._var.get().split(",") if self._var.get() else []

    @value.setter
    def value(self, new_value: list | None):
        """Set the list value of the form element."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        # Handle new_value=None by setting the variable to an empty string
        if new_value is not None:
            self._var.set(",".join(map(str, new_value)))
        else:
            self._var.set("")


class DictForm(FormElement):
    """Class for a dictionary input form element."""

    def __init__(self, master: tk.Misc, name: str, default: dict | None = None):
        # Initialize the variable before calling super().__init__
        self._var = tk.StringVar(value=str(default) if default is not None else "{}")
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the dictionary input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the dictionary value of the form element."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        # Use ast.literal_eval for safe evaluation of the string as a dict
        try:
            return ast.literal_eval(self._var.get())
        except (ValueError, SyntaxError):
            return {}

    @value.setter
    def value(self, new_value: dict | None):
        """Set the dictionary value of the form element."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        if new_value is not None:
            self._var.set(str(new_value))
        else:
            self._var.set("{}")


class ChoiceForm(FormElement):
    """Class for a choice input form element."""

    def __init__(
        self, master: tk.Misc, name: str, choices: list[str], default: str | None = None
    ):
        if not isinstance(choices, list) or not choices:
            raise ValueError("Choices must be a non-empty list.")
        # Initialize the variable before calling super().__init__
        value = default if default in choices else choices[0]
        self._var = tk.StringVar(value=value)
        self.choices = choices
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the choice input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        # Ensure choices is a non-empty list
        if not self.choices:
            return
        if not isinstance(self._var, tk.StringVar):
            raise TypeError("Variable must be a StringVar.")
        self.option_menu = tk.OptionMenu(self, self._var, *self.choices)
        self.option_menu.pack(fill=tk.X, padx=5, pady=5)

    @property
    def value(self):
        """Get the selected choice value."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        """Set the selected choice value."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        # Handle new_value=None by setting to the first choice
        if new_value in self.choices:
            self._var.set(new_value)
        elif new_value is None and self.choices:
            self._var.set(self.choices[0])
        else:
            raise ValueError(f"Value '{new_value}' is not in the choices.")

    def add_choice(self, choice: str):
        """Add a new choice to the choice input."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        if choice not in self.choices:
            self.choices.append(choice)
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' already exists.")

    def remove_choice(self, choice: str):
        """Remove a choice from the choice input."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        if choice in self.choices:
            self.choices.remove(choice)
            if self.choices and self._var.get() == choice:
                self._var.set(self.choices[0])
            elif not self.choices:
                self._var.set("")
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' does not exist.")

    def clear_choices(self):
        """Clear all choices from the choice input."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.choices.clear()
        self._var.set("")
        self.regen_widgets()


class MultiChoiceForm(FormElement):
    """Class for a multi-choice input form element."""

    def __init__(
        self,
        master: tk.Misc,
        name: str,
        choices: list[str],
        default: list[str] | None = None,
    ):
        # Initialize the variable before calling super().__init__
        value = ",".join(map(str, default)) if default is not None else ""
        self._var = tk.StringVar(value=value)
        self.choices = choices
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the multi-choice input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self.choices is None:
            return
        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        for choice in self.choices:
            self.listbox.insert(tk.END, choice)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Bind the selection event
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    def _on_select(self, _):
        """Handle selection changes in the listbox."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        selected = self.value
        self._var.set(",".join(selected))

    @property
    def value(self):
        """Get the selected choices."""
        if not hasattr(self, "listbox") or self.listbox is None:
            return []
        return [self.listbox.get(i) for i in self.listbox.curselection()]

    @value.setter
    def value(self, new_value: list[str] | None):
        """Set the selected choices."""
        if not hasattr(self, "listbox") or self.listbox is None:
            return

        self.listbox.select_clear(0, tk.END)
        if new_value is not None:
            for choice in new_value:
                try:
                    index = self.choices.index(choice)
                    self.listbox.select_set(index)
                except ValueError:
                    # Ignore choices that don't exist
                    pass
        self._on_select(None)


class FileForm(FormElement):
    """Class for a file input form element."""

    def __init__(self, master: tk.Misc, name: str, default: str | None = None):
        # Initialize the variable before calling super().__init__
        self._var = tk.StringVar(value=default if default is not None else "")
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the file input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.button = tk.Button(self, text="Browse", command=self.browse_file)
        self.button.pack(pady=5)

    def browse_file(self):
        """Open a file dialog to select a file."""
        file_path = filedialog.askopenfilename()
        if file_path and self._var is not None:
            self._var.set(file_path)

    @property
    def value(self):
        """Get the file path value of the form element."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self._var.set(new_value if new_value is not None else "")
        self.regen_widgets()

    def clear(self):
        """Clear the file input."""
        if self._var is not None:
            self._var.set("")
        self.regen_widgets()

    def reset(self):
        """Reset the file input to its default state."""
        self.clear()


class DirectoryForm(FileForm):
    """Class for a directory input form element."""

    def __init__(self, master: tk.Misc, name: str, default: str | None = None):
        super().__init__(master, name, default)

    def browse_file(self):
        """Open a directory dialog to select a directory."""
        dir_path = filedialog.askdirectory()
        if dir_path and self._var is not None:
            self._var.set(dir_path)


class PathForm(FormElement):
    """Class for a path input form element."""

    def __init__(self, master: tk.Misc, name: str, default: str | None = None):
        # Initialize the variable before calling super().__init__
        self._var = tk.StringVar(value=default if default is not None else "")
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the path input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.button = tk.Button(self, text="Browse", command=self.browse_file)
        self.button.pack(pady=5)

    def browse_file(self):
        """Open a file dialog to select a file or directory."""
        file_path = filedialog.askopenfilename() or filedialog.askdirectory()
        if file_path and self._var is not None:
            self._var.set(file_path)

    @property
    def value(self):
        """Get the path value of the form element."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self._var.set(new_value if new_value is not None else "")
        self.regen_widgets()


class RadioForm(FormElement):
    """Class for a radio button input form element."""

    def __init__(
        self, master: tk.Misc, name: str, choices: list[str], default: str | None = None
    ):
        if not isinstance(choices, list) or not choices:
            raise ValueError("Choices must be a non-empty list.")
        # Initialize the variable before calling super().__init__
        value = default if default in choices else choices[0]
        self._var = tk.StringVar(value=value)
        self.choices = choices
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the radio button input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        for choice in self.choices:
            rb = tk.Radiobutton(self, text=choice, variable=self._var, value=choice)
            rb.pack(anchor=tk.W)

    @property
    def value(self):
        """Get the selected radio button value."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        """Set the selected radio button value."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        # Handle new_value=None by setting to the first choice
        if new_value in self.choices:
            self._var.set(new_value)
        elif new_value is None and self.choices:
            self._var.set(self.choices[0])
        else:
            raise ValueError(f"Value '{new_value}' is not in the choices.")

    def add_choice(self, choice: str):
        """Add a new choice to the radio button input."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        if choice not in self.choices:
            self.choices.append(choice)
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' already exists.")

    def remove_choice(self, choice: str):
        """Remove a choice from the radio button input."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        if choice in self.choices:
            self.choices.remove(choice)
            if self.choices and self._var.get() == choice:
                self._var.set(self.choices[0])
            elif not self.choices:
                self._var.set("")
            self.regen_widgets()
        else:
            raise ValueError(f"Choice '{choice}' does not exist.")

    def clear_choices(self):
        """Clear all choices from the radio button input."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.choices.clear()
        self._var.set("")
        self.regen_widgets()


class ColorForm(FormElement):
    """Class for a color input form element."""

    def __init__(self, master: tk.Misc, name: str, default: str | None = None):
        # Initialize the variable before calling super().__init__
        self._var = tk.StringVar(value=default if default is not None else "#FFFFFF")
        super().__init__(master, name, default)
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the color input."""
        for widget in self.winfo_children():
            widget.destroy()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.entry = tk.Entry(self, textvariable=self._var)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.button = tk.Button(self, text="Select Color", command=self.select_color)
        self.button.pack(pady=5)

    def select_color(self):
        """Open a color dialog to select a color."""
        if self._var is None:
            return
        color = colorchooser.askcolor(color=self._var.get())
        if color[1]:
            self._var.set(color[1])

    @property
    def value(self):
        """Get the selected color value."""
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        return self._var.get()

    @value.setter
    def value(self, new_value: str | None):
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self._var.set(new_value if new_value is not None else "#FFFFFF")
        self.regen_widgets()


class ColorPickerForm(ColorForm):
    """Class for a color picker input form element."""

    def __init__(self, master: tk.Misc, name: str, default: str | None = None):
        super().__init__(master, name, default)
        # Note: self._var is already initialized by ColorForm's __init__
        self.regen_widgets()

    def regen_widgets(self):
        """Regenerate the widgets for the color picker input."""
        super().regen_widgets()
        if self._var is None:
            raise AttributeError("This form element does not have a variable.")
        self.color_display = tk.Label(self, bg=self._var.get(), width=20, height=2)
        self.color_display.pack(pady=5)
        self._var.trace_add("write", self.update_color_display)

    def update_color_display(self, *_):
        """Update the color display when the variable changes."""
        if self._var is None:
            return
        self.color_display.config(bg=self._var.get())
