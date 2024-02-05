# Tkinter is a library used to create GUI's in python
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
# Time is a library used to give time/date information
import time

# TODO: Delete this line, it's just so the IDE will stop bugging me about unused imports
time.time()

# The root is the base for everything in Tkinter
root = tk.Tk()


class PageObject:

    def __init__(self, title: str, geometry: str or list, resizable: list, background: str = False):
        """
        pageObject creates a new Tkinter page
        :param title: Title of the page
        :param geometry: Either preset (small, medium, large) or custom [x_axis, y_axis]
        :param resizable: Can the user resize the window
        """

        # Create a new frame, ngl I can't remember what this is for
        self.frame = ttk.Frame(root)
        # Set to have grid positioning
        self.frame.grid()

        # Set the name to the given title
        root.title(title)

        # Set the page size, either a preset or custom
        if geometry.lower() == "small":
            root.geometry("360x240")
        elif geometry.lower() == "medium":
            root.geometry("450x300")
        elif geometry.lower() == "large":
            root.geometry("600x400")
        else:
            root.geometry(geometry)

        # Set whether the page can be resized (X axis, Y axis)
        root.resizable(resizable[0], resizable[1])

        # Set it so that Ctrl+W always closes the app
        self.frame.bind_all(sequence="<Control-w>", func=exit)

        if background:
            self.frame.config(bg = background)

    def add_hotkey(self, sequence, func):
        """
        Add a whole frame key bind
        :param sequence: '<MODIFIER-KEY>'
        :param func: function to be executed on sequence
        """
        self.frame.bind_all(sequence=sequence, func=func)

    def create_button_on_page(self, text: str, command, column: int, row: int, span: int) -> tk.Button:
        """
        Create a new button on the page
        :param text: Text displayed on button
        :param command: Function called on press
        :param column: Column for button
        :param row: Row for button
        :param span: Span (width) of button
        :return: ttk.Button
        """
        button = ttk.Button(self.frame, text=text, command=command)
        button.grid(column=column, row=row, columnspan=span, padx=8, pady=8)
        return button

    def create_label_on_page(self, text: str, column: int, row: int, span: int) -> tk.Label:
        """
        Create a new label on the page
        :param text: Text displayed on label
        :param column: Column for label
        :param row: Row for label
        :param span: Span (width) of label
        :return: ttk.Label
        """
        label = ttk.Label(self.frame, text=text)
        label.grid(column=column, row=row, columnspan=span, padx=1, pady=1)
        return label

    def create_entry_box_on_page(self, result: tk.StringVar, column: int, row: int, span: int, disguise: bool = False) -> tk.Entry:
        """
        Create a new entry box on page
        :param result: tk.StringVar to store result of entry box
        :param column: Column for entry box
        :param row: Row for entry box
        :param span: Span (width) of entry box
        :param disguise: Disguise entry as * character, default False
        :return: tk.Entry
        """

        entry = ttk.Entry(self.frame, textvariable=result)
        entry.grid(column=column, row=row, columnspan=span, padx=1, pady=1)

        if disguise:
            entry.config(show="*")

        return entry

    def create_listbox_on_page(self, column: int, row: int, span: int) -> tk.Listbox:
        """
        Create a new listbox
        :param column: Column for listbox
        :param row: Row for listbox
        :param span: Span (width) of listbox
        :return: tk.Listbox
        """
        listbox = tk.Listbox(self.frame)
        listbox.grid(column=column, row=row, columnspan=span, padx=0, pady=1)

        return listbox

    def delete_page(self) -> None:
        """
        This deletes the frame and all the items on it
        :return: None
        """
        for item in self.frame.winfo_children():
            item.destroy()
        for item in root.winfo_children():
            item.destroy()
        self.frame.destroy()


def login_page() -> None:
    """
    This is the login page
    :return: None
    """

    # Setup login page parameters
    login = PageObject(title="Login", geometry="small", resizable=[True, True])

    def clear_entry_box(targets: list = ('username', 'password')):
        """
        Clear given entry box(es), this is a terrible way of doing it
        :param targets: List of entry boxes to clear
        """
        if 'username' in targets:
            username_entry_box.delete(0, tk.END)
        if 'password' in targets:
            password_entry_box.delete(0, tk.END)

    def entry_meets_requirements(*event):
        """
        Validate if username and password are valid
        :param event: discarded, only here to handle hotkey
        """
        username_text = username_entry_box.get()
        password_text = password_entry_box.get()

        clear_entry_box(['password'])

        if len(username_text) != 0 and len(password_text) >= 8:
            # TODO: Decide on validation flow
            print("HAVEN'T IMPLEMENTED THIS BIT YET")
            login.delete_page()
            main_page(username_text)

        elif len(username_text) == 0 and len(password_text) == 0:
            showerror("Missing Input", "Username and Password not given")
            login.delete_page()
            main_page(username_text)
        elif len(username_text) == 0:
            showerror("Missing Input", "Username not given")
        elif len(password_text) == 0:
            showerror("Missing Input", "Password not given")
        elif len(password_text) < 8:
            showerror("Password Too Short", "Password must be at least 8 characters long")

    # Username prompt and handler
    login.create_label_on_page(text="Username:", column=1, row=1, span=2)
    username = tk.StringVar()
    username_entry_box = login.create_entry_box_on_page(result=username, column=3, row=1, span=3)
    # Set focus to username entry box
    username_entry_box.focus()

    # Password prompt and handler
    login.create_label_on_page(text="Password:", column=1, row=2, span=2)
    password = tk.StringVar()
    password_entry_box = login.create_entry_box_on_page(result=password, column=3, row=2, span=3, disguise=True)
    # Make Ret submit
    password_entry_box.bind("<Return>", entry_meets_requirements)

    # Submit button
    login.create_button_on_page(text="submit", command=entry_meets_requirements, column=2, row=3, span=2)

    # Clear button
    login.create_button_on_page(text="clear", command=clear_entry_box, column=4, row=3, span=2)

    # Hotkey assigning Ctrl+Ret to validate login
    login.add_hotkey(sequence="<Control-Return>", func=entry_meets_requirements)


def main_page(username):
    main = PageObject(title="MQTT Basic GUI", geometry='small', resizable=[True, True])

    # TODO: Add content for main page
    main.create_label_on_page(text=f"Username: {username}", column=1, row=1, span=2)
    print("MAIN PAGE UNDER CONSTRUCTION")
    showerror(title="MAIN PAGE UNDER CONSTRUCTION", message="Please wait for the main page to be completed")


if __name__ == "__main__":
    login_page()
    root.mainloop()
