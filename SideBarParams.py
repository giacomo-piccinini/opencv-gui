import tkinter as tk
from tkinter import ttk
import pyglet




SIDEBAR_BG_COLOR2 = "#373737"
FIELDS_BG_COLOR = "#1D1D1D"
FIELDS_BORDER_COLOR = "#454545"
FIELD_SEPARATOR_COLOR = "#FFFFFF"

HELPER_TEXT_BG = "#373737"


class DataField(tk.Frame):
    def __init__(self, parent, helper=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, bg=SIDEBAR_BG_COLOR2, **kwargs)

        self.configure(bg=FIELDS_BG_COLOR, bd=1, relief="solid", highlightcolor=FIELDS_BORDER_COLOR, highlightbackground=FIELDS_BORDER_COLOR, highlightthickness=1)

        self.fieldIconFrame = tk.Frame(self, bg=FIELDS_BG_COLOR)
        self.fieldIconFrame.pack(side="right", fill="y", padx=3, pady=3)

        self.fieldIcon = tk.PhotoImage(file="assets/images/icons/folderIcon.png")
        self.icon = tk.Label(self.fieldIconFrame, image=self.fieldIcon, bg=FIELDS_BG_COLOR, fg="white")
        self.icon.pack()
        if helper:
            self.helperTextstr = helper
            self.helperText = tk.Label(self, text=self.helperTextstr, bg=HELPER_TEXT_BG, fg="white")
            self.helperText.pack(side="left", padx=5)

        self.field = tk.Entry(self, bg=FIELDS_BG_COLOR, fg="white", bd=0, highlightthickness=0, insertbackground="white")
        self.field.pack(side="right", fill="y", padx=5)

        self.pack(fill="x", expand=True)

class ComboField(tk.Frame):
    def __init__(self, parent, values, helper=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, bg=SIDEBAR_BG_COLOR2, **kwargs)

        self.val = tk.StringVar()

        self.configure(bg=FIELDS_BG_COLOR, bd=1, relief="solid", highlightcolor=FIELDS_BORDER_COLOR, highlightbackground=FIELDS_BORDER_COLOR, highlightthickness=1)

        #self.fieldIconFrame = tk.Frame(self, bg=FIELDS_BG_COLOR)
        #self.fieldIconFrame.pack(side="right", fill="y", padx=3, pady=3)

        self.fieldIcon = tk.PhotoImage(file="assets/images/icons/folderIcon.png")

        self.indicator_img = tk.PhotoImage(file="assets/images/icons/combodrop.png")

        #self.icon = tk.Label(self.fieldIconFrame, image=self.fieldIcon, bg=FIELDS_BG_COLOR, fg="white")
        #self.icon.pack()
        if helper:
            self.helperTextstr = helper
            self.helperText = tk.Label(self, text=self.helperTextstr, bg=HELPER_TEXT_BG, fg="white")
            self.helperText.pack(side="left", padx=5)

        self.field = tk.OptionMenu(self, self.val, *values)
        self.field.configure(indicatoron=0, bd=0, highlightthickness=0, image=self.indicator_img, compound='right', bg=FIELDS_BG_COLOR, fg="white", activebackground=FIELDS_BG_COLOR, activeforeground="white")
         
        self.field.pack(side="right", fill="y", padx=3)

        self.pack(fill="x", expand=True)

class GenericField(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, bg=SIDEBAR_BG_COLOR2, **kwargs)

        self.contentFrame = tk.Frame(self, bg=SIDEBAR_BG_COLOR2)
        self.contentFrame.pack(fill="both", expand=True, padx=10, pady=5)

        self.iconFrame = tk.Frame(self.contentFrame, bg=SIDEBAR_BG_COLOR2)
        self.iconFrame.pack(side="right", fill="y", padx=5)

        self.restoreIconImage = tk.PhotoImage(file="assets/images/icons/restoreDefaultIcon.png")

        self.restoreIcon = tk.Label(self.iconFrame, image=self.restoreIconImage, bg=SIDEBAR_BG_COLOR2, fg="white")
        self.restoreIcon.pack(side='left')

        self.dataFrame = tk.Frame(self.contentFrame)
        self.dataFrame.pack(side="right", fill="y", padx=5)

        self.separator = tk.Frame(self.contentFrame, bg=FIELD_SEPARATOR_COLOR, width=1)
        self.separator.pack(side="right", fill="y", padx=5, pady=3)

        self.labelFrame = tk.Frame(self.contentFrame, bg=SIDEBAR_BG_COLOR2)
        self.labelFrame.pack(side="right", fill="y")

        self.label = tk.Label(self.labelFrame, text="filename", bg=SIDEBAR_BG_COLOR2, fg="white")
        self.label.pack(side="right", padx=5)

        self.infoFrame = tk.Frame(self.contentFrame, bg=SIDEBAR_BG_COLOR2)
        self.infoFrame.pack(side="left", fill="y", padx=5)

        self.infoIconImage = tk.PhotoImage(file="assets/images/icons/infoIcon.png")

        self.infoIcon = tk.Label(self.infoFrame, image=self.infoIconImage, bg=SIDEBAR_BG_COLOR2, fg="white", cursor="hand2")
        self.infoIcon.pack(side='left')

        self.pack(side='top',fill="x")

class FilePickerField(GenericField):
    def __init__(self, parent, data, *args, **kwargs):
        GenericField.__init__(self, parent, *args, **kwargs)

        self.iconFolder = tk.PhotoImage(file="assets/images/icons/folderIcon.png")

        self.filepick = DataField(self.dataFrame)

        self.data = data

        if data['value']:
            self.filepick.field.insert(0, data['value'])
        
        self.filepick.icon.config(image=self.iconFolder)

        self.label.config(text=data['name'])

        self.filepick.field.bind("<Return>", self.return_pressed_in_field)
    
    def return_pressed_in_field(self, event):
        self.data['value'] = self.filepick.field.get()


    def set_data(self, data):
        self.filepick.field.delete(0, 'end')
        self.filepick.field.insert(0, data)


class IntField(GenericField):
    def __init__(self, parent, *args, **kwargs):
        GenericField.__init__(self, parent, *args, **kwargs)

        self.iconFolder = tk.PhotoImage(file="assets/images/icons/sliderIcon.png")

        self.intVal = DataField(self.dataFrame)

        self.intVal.icon.config(image=self.iconFolder)

        self.label.config(text="testvar")

class ComboboxField(GenericField):
    def __init__(self, parent, data, params=None, *args, **kwargs):
        GenericField.__init__(self, parent, *args, **kwargs)
        self.data = data
        self.params = params

        self.iconFolder = tk.PhotoImage(file="assets/images/icons/combodrop.png")

        self.intVal = ComboField(self.dataFrame, self.params)
        self.intVal.val.set(self.data['value'])

        self.label.config(text=self.data['name'])

        self.intVal.val.trace('w', self.update_data)

    def update_data(self, *args):
        self.data['value'] = self.intVal.val.get()



class SizeField(GenericField):
    def __init__(self, parent, name, *args, **kwargs):
        GenericField.__init__(self, parent, *args,**kwargs)

        self.name = name

        self.dataIcon = tk.PhotoImage(file="assets/images/icons/sliderIcon.png")

        self.widthField = DataField(self.dataFrame, helper="width")
        self.heightField = DataField(self.dataFrame, helper="height")

        self.widthField.icon.config(image=self.dataIcon)
        self.heightField.icon.config(image=self.dataIcon)

        self.label.config(text=self.name)

        self.widthField.field.config(validate='focusout',validatecommand=self.invalid_command)
        self.heightField.field.config(validate='focusout',validatecommand=self.invalid_command)

        self.widthField.field.bind("<FocusOut>", self.update_size)
        self.widthField.field.bind("<Return>", self.return_pressed_in_field)
    
    def return_pressed_in_field(self, event):
        print("return pressed")
        self.label.focus_set()

    def invalid_command(self):
        print("invalid command")
    
    def update_size(self, event):
        print("update size")
        self.label.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    FilePickerField(root)
    IntField(root)
    SizeField(root)
    ComboboxField(root)
    #root.geometry("800x600")
    #root.state('zoomed')

    # ubuntu
    #root.attributes('-zoomed', True)
    root.mainloop()