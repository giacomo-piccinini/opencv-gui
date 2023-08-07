import tkinter as tk
from Node import Node, CVNode
from GUI.NodeSideBar import NodeSideBar

class NodeGraph(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self, bg="#222222")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.config(highlightthickness=0, borderwidth=0)

        self.nodes = []

        # spawn imread node
        self.node = CVNode(self, self.canvas, 'imread')
        self.selectedNode = None
        self.node.cvFunctionArgs[0]["value"] = "/home/mattia/opencv-gui/assets/images/test/skyfhd.jpg"

        self.e1 = self.canvas.create_window(200, 200, window=self.node, anchor="n")
        self.canvas.itemconfig(self.e1,width=200,height=200)

        self.nodes.append(self.node)

        # spawn blur node
        self.node2 = CVNode(self, self.canvas, 'blur')
        self.selectedNode = None

        self.e2 = self.canvas.create_window(600, 300, window=self.node2, anchor="n")
        self.canvas.itemconfig(self.e2,width=200,height=200)


        self.nodeSidebar = NodeSideBar(self)
        self.nodeSidebar.tkraise()

        self.canvas.bind("<ButtonPress-1>", self.canvas_button_left)

        self.node.title.bind("<ButtonPress-1>", lambda e: self.select_node(e, self.node, self.e1))
        self.node.titleFrame.bind("<ButtonPress-1>", lambda e: self.move_node_mouse(e, self.node, self.e1))
        self.node.title.bind("<Enter>", lambda e: self.node.title.configure(fg="#2196F3"))
        self.node.title.bind("<Leave>", lambda e: self.node.title.configure(fg="white"))       
        
        self.node2.title.bind("<Enter>", lambda e: self.node2.title.configure(fg="2196F3"))
        self.node2.title.bind("<Leave>", lambda e: self.node2.title.configure(fg="white"))
        self.node2.title.bind("<ButtonPress-1>", lambda e: self.move_node_mouse(e, self.node2, self.e2))
        self.node2.titleFrame.bind("<ButtonPress-1>", lambda e: self.move_node_mouse(e, self.node2, self.e2))

        self.nodes.append(self.node2)
       


    def canvas_button_left(self, event):
        self.selectedNode = None
        self.nodeSidebar.place_forget()
        
        # delete pending connections
        for node in self.nodes:
            for input in node.inputElements:
                input.waiting_connection = False
            for output in node.outputElements:
                output.waiting_connection = False
    
    def select_node(self, click_event, node: Node, node_canvas_id):
        self.nodeSidebar.re_place()
        self.nodeSidebar.set_node(node)        

    def move_node_mouse(self, click_event, node: Node, node_canvas_id):
        node.titleFrame.bind("<B1-Motion>", lambda event: self.move_node(event, click_event, node, node_canvas_id))


    def move_node(self, drag_event, click_event, node, node_canvas_id):
        node_coords = self.canvas.coords(node_canvas_id)
        self.canvas.coords(node_canvas_id, node_coords[0]+drag_event.x-click_event.x, node_coords[1]+drag_event.y-click_event.y)

    # def create_connection(self):
    #     for node in self.parent.parent.nodes:
    #         print(node)