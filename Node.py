import tkinter as tk
import logging
import json
import cv2

TITLE_COLOR = "#333333"
BODY_COLOR = "#444444"

class Node(tk.Frame):
    def __init__(self, graph, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg=BODY_COLOR)
        self.parent = parent
        self.graph = graph

        self.titleFrame = tk.Frame(self, bg=TITLE_COLOR)
        self.titleFrame.pack(fill="x", side="top")

        self.title = tk.Label(self.titleFrame, text="Null", bg=TITLE_COLOR, fg="#ffffff", font=("Open Sans", 12), anchor="w")
        self.title.pack(fill="x", side="left", padx=5, pady=5)

        self.body = tk.Frame(self, bg=BODY_COLOR)
        self.body.pack(fill="both", expand=True)

class CVNode(Node):
    def __init__(self, graph, parent, execname, *args, **kwargs):
        Node.__init__(self, graph, parent, *args, **kwargs)

        self.data = json.load(open("DATA/cv2.json"))
        self.enums = json.load(open("DATA/enums.json"))
        
        self.execname = execname
        #self.var1 = 'assets/images/icons/IOGreen-16px.png'
        #self.var2 = 1

        self.values = [] #[self.var1, self.var2]
        self.kwvalues = {}

        self.cvFunctionArgs = []                    # input params type + default
        self.cvFunctionOutput = []                  # output type
        
        self.outputElements = []
        self.inputElements = []

        self.last_result = None

        self.init_node()
        self.init_gui()

    def init_node(self):
        for func in self.data["functions"]:
            if func["name"] == self.execname:
                self.funcdata = func
                break

        for arg in self.funcdata["params"]:
            dd = {
                "name": arg["name"],
                "type": arg["type"],
                "value": arg["default"] if "default" in arg else None
            }
            
            # convert value (string) to tuple
            if dd["type"] == "Point":
                dd["value"] = tuple(map(int, dd["value"].split(",")))

            self.cvFunctionArgs.append(dd)

        for ret in self.funcdata["return"]:
            dd = {
                "name": ret["name"],
                "type": ret["type"]
            }
            self.cvFunctionOutput.append(dd)

            
    def init_gui(self):
        self.title.config(text=self.execname)

        for output in self.cvFunctionOutput:
            output['node_gui'] = NodeOutput(self.body, self, output["name"])
        for input in self.cvFunctionArgs:
            input['node_gui'] = NodeInput(self.body, self, input["name"])

    def run(self):
        print("Running node {}".format(self.execname))
        # print("Values: {}".format(self.values))
        func = getattr(cv2, self.funcdata["name"])
        for i in range(len(self.cvFunctionArgs)):
            if self.cvFunctionArgs[i]["type"] in self.enums:
                self.kwvalues[self.cvFunctionArgs[i]["name"]] = getattr(cv2, self.cvFunctionArgs[i]["value"])
            else:
                self.kwvalues[self.cvFunctionArgs[i]["name"]] = self.cvFunctionArgs[i]["value"]
        print("Kwvalues: {}".format(self.kwvalues))
        res = func(**self.kwvalues)
        # print("Result: {}".format(res))
        self.last_result = res
        return res
    
    def run_chain(self):
        result = self.run()
        print("Result type: {}".format(type(result)))
        for outputElem in self.cvFunctionOutput:
            if outputElem["node_gui"].connection.outputNode is not None:
                outputElem["node_gui"].connection.send_result(outputElem["name"], result)
                outputElem["node_gui"].connection.outputNode.run_chain()
                
        # output.conenssione.nodeoconnesso.run_chain()

    def set_value(self, name, value):
        for input in self.cvFunctionArgs:
            if input["name"] == name:
                input["value"] = value
                break

class IOElement(tk.Frame):
    def __init__(self, parent, node, name, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config(bg=BODY_COLOR)
        self.is_connected = False
        self.waiting_connection = False

        self.node = node
        self.name = name
        
        self.normal = tk.PhotoImage(file="assets/images/icons/IOMedGrey-16px.png")
        self.hovered = tk.PhotoImage(file="assets/images/icons/IOLightGrey-16px.png")
        self.connected = tk.PhotoImage(file="assets/images/icons/IOGreen-16px.png")

        self.connection = Connection()

        self.text = tk.Label(self, text="null", bg=BODY_COLOR, fg="#ffffff", font=("Open Sans", 10))
        self.icon = tk.Label(self, image=self.normal, bg=BODY_COLOR)

        self.pack(side="top", fill="x")

        self.icon.bind("<Enter>", self.hover)
        self.icon.bind("<Leave>", self.unhover)
        self.icon.bind("<ButtonPress-1>", self.connect)
        
    
    def hover(self, event):
        if not self.is_connected and not self.waiting_connection:
            self.icon.config(image=self.hovered)
    
    def unhover(self, event):
        if not self.is_connected and not self.waiting_connection:
            self.icon.config(image=self.normal)
    
    def connect(self, event):
        if not self.waiting_connection:
            self.icon.config(image=self.connected)
            self.waiting_connection = True
        # x = event.widget.winfo_rootx() - self.parent

    


class NodeInput(IOElement):
    def __init__(self, *args, **kwargs):
        IOElement.__init__(self, *args, **kwargs)
        self.icon.pack(side="left")
        
        txt = self.name
        self.text.configure(text=txt)
        self.text.pack(side="left")

        self.icon.bind("<ButtonRelease-1>", self.close_connection)

    def close_connection(self, e):
        for node in self.node.graph.nodes:
            print("Node: {}".format(node.execname))
            if node.execname == self.node.execname:
                continue
            for output in node.cvFunctionOutput:
                if output["node_gui"].waiting_connection:
                    self.connection.inputNode = node
                    self.connection.outputNode = self.node
                    output["node_gui"].waiting_connection = False
                    output["node_gui"].is_connected = True
                    self.is_connected = True
                    output["node_gui"].connection = self.connection

        print("Input node: {}".format(self.connection.inputNode.execname))
        print("Output node: {}".format(self.connection.outputNode.execname))
        print("Output values: {}".format(self.connection.outputNode.kwvalues))
                    


class NodeOutput(IOElement):
    def __init__(self, *args, **kwargs):
        IOElement.__init__(self, *args, **kwargs)
        self.icon.pack(side="right")

        txt = self.name
        self.text.configure(text=txt)
        self.text.pack(side="right")

class ConnectionBezier:
    def __init__(self, canvas, x1, y1, x2, y2, color="#ffffff", width=2):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.color = color
        self.width = width

        self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=self.width, smooth=True)
    
    def create_bezier(self, c1, c2, c3, c4, **kwargs):
        # Start x and y coordinates, when t = 0
        x_start = c1[0]
        y_start = c1[1]

        p = [c1, c2, c3, c4]

        # loops through
        line_ids = []
        n = 50
        for i in range(50):
            t = i / n
            x = (p[0][0] * (1-t)**3 + p[1][0] * 3 * t * (1-t)**2 + p[2][0] * 3 * t**2 * (1-t) + p[3][0] * t**3)
            y = (p[0][1] * (1-t)**3 + p[1][1] * 3 * t * (1-t)**2 + p[2][1] * 3 * t**2 * (1-t) + p[3][1] * t**3)

        line_ids.append(self.create_line(x, y, x_start, y_start, fill='#90A4AE', width=1.5, smooth=1, **kwargs))
        # updates initial values
        x_start = x
        y_start = y

        return line_ids
    
class Connection:
    def __init__(self):
        self.inputValue = None
        self.outputValue = None
        self.inputNode = None
        self.outputNode = None
        self.id_in = None
        self.id_out = None

    
    def setInputNode(self, node):
        self.inputNode = node
    
    def setOutputNode(self, node):
        self.outputNode = node
    
    def setInputValue(self, val):
        self.inputValue = val

    def setOutputValue(self, val):
        self.outputValue = val

    def set_ids(self, id_in, id_out):
        self.id_in = id_in
        self.id_out = id_out

    def send_result(self, name, result):
        # print(self.outputNode.cvFunctionArgs[self.outputNode.inputElements.index(self)]["index"])
        self.outputNode.set_value(name, result)
        # self.outputNode.set_value(1, (5,5))
        # self.outputNode.set_value(2, (2,2))

    


