from tkinter import *
from tkinter import ttk

root_window = Tk()
style = ttk.Style()

photo = """
R0lGODlhDQAQAPQAAFw1Zl42Z2A6amE6amI7a2I8a2I8bKeHqK6BqbSLsLWLsLuV
t7ufu7yfu72hvL6ivb6ivr+jvsKgvsWlwseow8iqxcmrxs+1zNC2zdO70dS90tW9
0tW+0wAAAAAAAAAAACH5BAEAAB0ALAAAAAANABAAAAVMYCd2QFmOKJltGZCOwMZt
7kvKtH3P9RvzutgmZ4tdiL6NBUkyGTaSjMHkEjgyGcuiwnIIRoWIJUG2eFPhCYJy
fhUkmLbNcPjqRL1RCAA7
"""

photo = PhotoImage(data=photo)
l = ttk.Label(root_window, image=photo).grid()

style.element_create('Mystyle.TCombobox.downarrow', 'image', photo)
style.layout(
    'Mystyle.TCombobox', [(
        'Combobox.field', {
            'sticky': NSEW,
            'children': [(
                'Mystyle.TCombobox.downarrow', {
                    'side': 'right',
                    'sticky': NSEW
                }
            ), (
                'Combobox.padding', {
                    'expand': '1',
                    'sticky': NSEW,
                    'children': [(
                        'Combobox.textarea', {
                            'sticky': NSEW
                        }
                    )]
                }
            )]
        }
    )]
)

cbo = ttk.Combobox(root_window, values=('one', 'two', 'three'), style='Mystyle.TCombobox')
cbo.grid()

root_window.mainloop()