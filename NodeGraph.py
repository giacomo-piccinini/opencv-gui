import tkinter as tk
import sys
from Node import Node, CVNode, Connection
import json
from GUI.NodeSideBar import NodeSideBar

class NodeGraph(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(fill="both", expand=True)
        
        self.init_drawer()


        self.canvas = tk.Canvas(self, bg="#222222")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.config(highlightthickness=0, borderwidth=0)

        self.nodes = []
        self.connections = []

        self.nodeSidebar = NodeSideBar(self)
        self.nodeSidebar.tkraise()

        self.canvas.bind("<ButtonPress-1>", self.canvas_button_left)

    def init_drawer(self):
        self.drawerBar = DrawerBar(self)        
        # for fun in self.drawerBar.elements:
            # fun.bind("<ButtonPress-1>", lambda e: self.add_node(e, str(fun.name)))
            # fun.label.bind("<ButtonPress-1>", lambda e: self.add_node(e, str(fun.name)))
            # print('binded ' + fun.name)       
            
            
    def add_node(self, ev, nodeName):
        print("Adding node: {}".format(nodeName))
        self.selectedNode = None
        node = CVNode(self, nodeName)

        canvasFrame = self.canvas.create_window(200, 200, window=node, anchor="n")
        self.canvas.itemconfig(canvasFrame,width=200)#,height=200)
        
        node.title.bind("<ButtonPress-1>", lambda e: self.select_node(e, node, canvasFrame))
        node.titleFrame.bind("<ButtonPress-1>", lambda e: self.move_node_mouse(e, node, canvasFrame))
        node.title.bind("<Enter>", lambda e: node.title.configure(fg="#2196F3"))
        node.title.bind("<Leave>", lambda e: node.title.configure(fg="white"))       
        
        self.nodes.append(node)
        
    def add_connection(self, fromIO, toIO):
        print("Adding connection: {} -> {}".format(fromIO, toIO))
        newConnection = Connection(self, fromIO, toIO)
        self.connections.append(newConnection)
        fromIO.connections.append(newConnection)
        
        fromIO.node.outputConnections.append(newConnection)
        toIO.node.inputConnections.append(newConnection)
        pass

    def canvas_button_left(self, event):
        self.selectedNode.hightlight(False)
        self.selectedNode = None
        self.nodeSidebar.place_forget()
        
        # delete pending connections
        for node in self.nodes:
            for input in node.inputElements:
                input.waiting_connection = False
            for output in node.outputElements:
                output.waiting_connection = False
    
    def set_highlights(self):
        for node in self.nodes:
            node.hightlight(False)
        self.selectedNode.hightlight(True)
    
    def select_node(self, click_event, node: Node, node_canvas_id):
        self.selectedNode = node
        self.set_highlights()
        self.nodeSidebar.re_place()
        self.nodeSidebar.set_node(node)
    

    def move_node_mouse(self, click_event, node: Node, node_canvas_id):
        node.titleFrame.bind("<B1-Motion>", lambda event: self.move_node(event, click_event, node, node_canvas_id))


    def move_node(self, drag_event, click_event, node, node_canvas_id):
        node_coords = self.canvas.coords(node_canvas_id)
        self.canvas.coords(node_canvas_id, node_coords[0]+drag_event.x-click_event.x, node_coords[1]+drag_event.y-click_event.y)
        for connection in node.inputConnections + node.outputConnections:
            connection.updateLine()

    # def create_connection(self):
    #     for node in self.parent.parent.nodes:
    #         print(node)
    

class DrawerBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg="#777777")
        self.pack(fill=tk.Y, side="left")
        self.parent = parent
        
        self.elements = []
        
        self.label = tk.Label(self, text="Drawer", bg="#777777", fg="white")
        self.label.pack(side="top", fill="x")
        
        self.functions = json.load(open("DATA/cv2.json"))
        
        for function in self.functions['functions']:
            self.elements.append(DrawerElement(self, function['name']))

class DrawerElement(tk.Frame):
    def __init__(self, parent, name, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.config(bg="#777777")
        self.pack(fill=tk.X)

        self.parent = parent
        
        self.name = name
        
        self.label = tk.Label(self, text=name, bg="#777777", fg="white")
        self.label.pack(side="left", fill="x")
        
        self.bind("<ButtonPress-1>", self.add_node)
        self.label.bind("<ButtonPress-1>", self.add_node)

    def add_node(self, e):
        self.parent.parent.add_node(e, self.name)