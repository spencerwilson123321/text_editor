
from tkinter import Tk, Text, Frame, END, Label, CENTER, Entry, BOTTOM, TOP
from sys import argv
from os.path import isfile


class FilenamePrompt(Frame):

    def __init__(self, parent=None, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.label = Label(self, text="Enter Filename:", background="white")
        self.label.pack(side=TOP)
        self.entry = Entry(self)
        self.entry.bind("<Return>", self.set_filename)
        self.entry.pack(side=BOTTOM)

    def show(self):
        self.configure(border=True)
        self.entry.focus_set()
        self.label.pack(side=TOP)
        self.entry.pack(side=BOTTOM)
        self.place(relx=0.5, rely=0.5, anchor="center")
    
    def hide(self):
        self.destroy()

    def set_filename(self, event):
        filename = self.entry.get()
        self.parent.current_file_name = filename
        self.parent.on_save(None)
        self.hide()


class OpenFilePrompt(Frame):

    def __init__(self, parent=None, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.label = Label(self, text="Open File:", background="white")
        self.label.pack(side=TOP)
        self.entry = Entry(self)
        self.entry.bind("<Return>", self.set_filename)
        self.entry.pack(side=BOTTOM)

    def show(self):
        self.configure(border=True)
        self.entry.focus_set()
        self.label.pack(side=TOP)
        self.entry.pack(side=BOTTOM)
        self.place(relx=0.5, rely=0.5, anchor="center")
    
    def hide(self):
        self.destroy()

    def set_filename(self, event):
        filename = self.entry.get()
        try:
            self.parent.open_file(filename)
        except FileNotFoundError:
            return
        self.parent.current_file_name = filename
        self.hide()


class TextEditor(Frame):


    def __init__(self, parent):
        super().__init__(parent)
        self.current_file_name = None
        self.filename_label = Label(master=self, text="", height=1)
        self.filename_label.pack(side=TOP)
        self.text_area = Text(self)
        self.text_area.bind("<Control-s>", self.on_save)
        self.text_area.bind("<Control-o>", self.on_open)
        self.text_area.bind("<Control-q>", self.on_quit)
        self.text_area.bind("<Button-1>", self.onclick_text_area)
        self.text_area.pack(anchor=CENTER, expand=True, fill="both")
        self.open_file_prompt = OpenFilePrompt(parent=self, master=self.text_area, height=100, width=300, background="white", padx=10, pady=10, borderwidth=2, relief="solid")
        self.filename_prompt = FilenamePrompt(parent=self, master=self.text_area, height=100, width=300, background="white", padx=10, pady=10, borderwidth=2, relief="solid")
        self.pack(expand=True, fill="both")

    def on_save(self, event):
        if self.current_file_name is None:
            self.filename_prompt = FilenamePrompt(parent=self, master=self.text_area, height=100, width=300, background="red", padx=10, pady=10, borderwidth=2, relief="solid")
            self.filename_prompt.show()
            return None
        self.filename_label.configure(text=self.current_file_name)
        with open(self.current_file_name, "w") as f:
            text = self.text_area.get("1.0", END)
            f.write(text)
    
    def on_open(self, event):
        self.open_file_prompt = OpenFilePrompt(parent=self, master=self.text_area, height=100, width=300, background="blue", padx=10, pady=10, borderwidth=2, relief="solid")
        self.open_file_prompt.show()
    
    def on_quit(self, event):
        self.master.destroy()

    def onclick_text_area(self, event):
        if self.filename_prompt is not None:
            self.filename_prompt.destroy()
        if self.open_file_prompt is not None:
            self.open_file_prompt.destroy()

    def open_file(self, filename):
        # 1. Check that the file exists.
        if not isfile(filename):
            raise FileNotFoundError
        # 2. Open the file.
        with open(filename) as f:
            text = f.read()
            # Clear the current text.
            self.text_area.delete("1.0", END)
            # Set the current text and filename.
            self.text_area.insert("1.0", text)
            self.set_current_file(filename)

    def set_current_file(self, filename):
        self.filename_label.config(text=filename)
        self.current_file_name = filename


if __name__ == "__main__":

    window = Tk()
    window.geometry("800x500")

    editor = TextEditor(window)
    editor.pack()
    if len(argv) == 2:
        editor.open_file(argv[1])

    window.mainloop()
