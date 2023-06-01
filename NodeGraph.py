import tkinter as tk
from Node import Node, CVNode, IMREADNode
from GUI.NodeSideBar import NodeSideBar

class NodeGraph(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self, bg="#222222")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.config(highlightthickness=0, borderwidth=0)

        self.node = IMREADNode(self.canvas, 'imread')
        self.selectedNode = None

        self.e1 = self.canvas.create_window(200, 200, window=self.node, anchor="n")
        self.canvas.itemconfig(self.e1,width=200,height=200)

        self.nodeSidebar = NodeSideBar(self)
        self.nodeSidebar.tkraise()

        self.canvas.bind("<ButtonPress-1>", self.canvas_button_left)

        self.node.title.bind("<ButtonPress-1>", self.move_node_mouse)


    def canvas_button_left(self, event):
        self.selectedNode = None
        self.nodeSidebar.place_forget()

    def move_node_mouse(self, event2):
        self.node.title.bind("<B1-Motion>", lambda event: self.move_node(event, event2))
        self.nodeSidebar.re_place()
        self.nodeSidebar.set_node(self.node)

    def move_node(self, event, start):
        act = self.canvas.coords(self.e1)
        self.canvas.coords(self.e1, act[0]+event.x, act[1]+event.y)