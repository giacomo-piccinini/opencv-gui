import tkinter as tk
from tkinter import ttk

from NodeGraph import NodeGraph


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.nodegraph = NodeGraph(self)
    
        self.pack(fill="both", expand=True)
        
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    #root.geometry("800x600")
    # root.state('zoomed')

    # ubuntu
    root.attributes('-zoomed', True)
    root.mainloop()