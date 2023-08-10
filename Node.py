import tkinter as tk
import logging
import json
import cv2

#region <Global VARS>
TITLE_BG_COLOR = "#333333"
TITLE_FONT = ("Open Sans", 12)
TITLE_FG_COLOR = "#FFFFFF"
BODY_COLOR = "#444444"
HIGHLIGHT_OFF_NODE_COLOR ="#111111" 
HIGHLIGHT_ON_NODE_COLOR = "#00FFFF"
HIGHLIGHT_THICKNESS = 1
#endregion


class Node(tk.Frame):
    def __init__(self, graph, *args, **kwargs):
        self.graph = graph
        self.canvas = graph.canvas
        tk.Frame.__init__(self, self.canvas, *args, **kwargs)
        self.config(bg=BODY_COLOR, highlightcolor=HIGHLIGHT_OFF_NODE_COLOR, highlightbackground=HIGHLIGHT_OFF_NODE_COLOR, highlightthickness=HIGHLIGHT_THICKNESS)

        self.titleFrame = tk.Frame(self, bg=TITLE_BG_COLOR)
        self.titleFrame.pack(fill="x", side="top")

        self.title = tk.Label(self.titleFrame, text="Null", bg=TITLE_BG_COLOR, fg=TITLE_FG_COLOR, font=TITLE_FONT, anchor="w", cursor="hand2")
        self.title.pack(fill="x", side="left", padx=5, pady=5)

        self.body = tk.Frame(self, bg=BODY_COLOR)
        self.body.pack(fill="both", expand=True)
    
    def hightlight(self, state):
        if state:
            self.config(highlightcolor=HIGHLIGHT_ON_NODE_COLOR, highlightbackground=HIGHLIGHT_ON_NODE_COLOR)
        else:
            self.config(highlightcolor=HIGHLIGHT_OFF_NODE_COLOR, highlightbackground=HIGHLIGHT_OFF_NODE_COLOR)

class CVNode(Node):
    def __init__(self, graph, execname, *args, **kwargs):
        Node.__init__(self, graph, *args, **kwargs)
                      
        self.data = json.load(open("DATA/cv2.json"))
        self.enums = json.load(open("DATA/enums.json"))
        
        self.execname = execname
        self.values = [] #[self.var1, self.var2]
        self.kwvalues = {}

        self.cvFunctionArgs = []                     # List of NodeInput(IOElements)
        self.cvFunctionOutput = []                   # List of NodeOutput(IOElements)
        
        self.outputConnections = []
        self.inputConnections = []

        self.lastResult = None                       # store last computed result of the function
        self.isLastResultUpdated = False             # flag to check if the last result is updated

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
            output['node_gui'] = NodeOutput(self.body, self, output)
        for input in self.cvFunctionArgs:
            input['node_gui'] = NodeInput(self.body, self, input)
        
        print("Input: {}".format(self.cvFunctionArgs))
        print("Output: {}".format(self.cvFunctionOutput))

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
        results = self.run()
        print("Result type: {}".format(type(results)))
        for outputElemId, outputElem in enumerate(self.cvFunctionOutput):
            for connection in outputElem["node_gui"].connections:
                    connection.send_result(outputElem["name"], result)
                    connection.outputNode.run_chain()
                
        # output.conenssione.nodeoconnesso.run_chain()

    def set_value(self, name, value):
        for input in self.cvFunctionArgs:
            if input["name"] == name:
                input["value"] = value
                break

class IOElement(tk.Frame):
    def __init__(self, parent, node, data, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config(bg=BODY_COLOR)
        
        self.hoveringConnectionWidget = None
        self.connectionLine = None
        self.is_connected = False
        self.waiting_connection = False
        self.connections = []
        
        self.node = node
        self.data = data
        self.name = self.data['name']

        
        self.normal = tk.PhotoImage(file="assets/images/icons/IOMedGrey-16px.png")
        self.hovered = tk.PhotoImage(file="assets/images/icons/IOLightGrey-16px.png")
        self.connected = tk.PhotoImage(file="assets/images/icons/IOGreen-16px.png")
        self.error = tk.PhotoImage(file="assets/images/icons/IORed-16px.png")
        self.canConnect = tk.PhotoImage(file="assets/images/icons/IOBlue-16px.png")



        self.text = tk.Label(self, text="null", bg=BODY_COLOR, fg="#ffffff", font=("Open Sans", 10))
        self.icon = tk.Label(self, image=self.normal, bg=BODY_COLOR)

        self.pack(side="top", fill="x")

        self.icon.bind("<Enter>", self.hover)
        self.icon.bind("<Leave>", self.unhover)
        
        self.icon.bind("<ButtonPress-1>", self.startConnect)
        self.icon.bind("<B1-Motion>", self.moveConnect)
        self.icon.bind("<ButtonRelease-1>", self.releaseConnect)
        
        self.icon.bind("<<TryConnect>>", self.tryConnect)
        self.icon.bind("<<EnterCanConnect>>", self.hoverCanConnect)
        self.icon.bind("<<EnterCannotConnect>>", self.hoverCannotConnect)        
    
    def hover(self, event):
        if not self.is_connected and not self.waiting_connection:
            self.icon.config(image=self.hovered)
    
    def hoverCanConnect(self, event):
        if not self.is_connected and not self.waiting_connection:
            self.icon.config(image=self.canConnect)

    def hoverCannotConnect(self, event):
        if not self.is_connected and not self.waiting_connection:
            self.icon.config(image=self.error)
    
    def unhover(self, event):
        if not self.is_connected and not self.waiting_connection:
            self.icon.config(image=self.normal)
    
    def startConnect(self, event):
        if not self.waiting_connection:
            self.icon.config(image=self.canConnect)
            self.waiting_connection = True
    
    def moveConnect(self,event):
        #draw the line
        x,y = self.getCenterOnCanvas()
        if self.connectionLine:
            self.node.canvas.delete(self.connectionLine)
            self.connectionLine = None
        self.connectionLine = self.node.canvas.create_line(x, y, x+event.x-self.icon.winfo_width()/2, y+event.y-self.icon.winfo_height()/2, fill="white", width=2, smooth=True)
        
        #hover Connection
        hoveringWidget = self.winfo_containing(event.x_root, event.y_root)
        if hoveringWidget != self.hoveringConnectionWidget:
            if self.hoveringConnectionWidget:
                self.hoveringConnectionWidget.event_generate("<Leave>")
            if hasattr(hoveringWidget.master, "data"):
                if self.data['type'] == hoveringWidget.master.data['type']:
                    hoveringWidget.event_generate("<<EnterCanConnect>>")
                else:
                    hoveringWidget.event_generate("<<EnterCannotConnect>>")

            self.hoveringConnectionWidget = hoveringWidget
            #self.hoveringConnectionWidget.event_generate("<<EnterConnect>>")
    
    def releaseConnect(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        widget.event_generate("<<TryConnect>>")
        if not self.is_connected:
            self.icon.config(image=self.normal)
            self.waiting_connection = False
        if self.connectionLine:
            self.node.canvas.delete(self.connectionLine)

        
    
    def getCenterOnCanvas(self):
        canvasX = self.node.canvas.winfo_rootx()
        canvasY = self.node.canvas.winfo_rooty()

        selfX = self.icon.winfo_rootx()
        selfY = self.icon.winfo_rooty()
        
        x = selfX - canvasX + self.icon.winfo_width()/2
        y = selfY - canvasY + self.icon.winfo_height()/2
        
        return (x, y)
    
    def tryConnect(self, e):
        for node in self.node.graph.nodes:
            for port in node.cvFunctionOutput + node.cvFunctionArgs:
                if port["node_gui"].waiting_connection:
                    if port["node_gui"].data["type"] == self.data["type"]:
                        fromIO = self if self.IOtype == "output" else port["node_gui"]
                        toIO = self if self.IOtype == "input" else port["node_gui"]
                        self.node.graph.add_connection(fromIO, toIO)
                        self.is_connected = True
                        self.waiting_connection = False
                        port["node_gui"].is_connected = True
                        port["node_gui"].waiting_connection = False
                    
 
    def setValue(self, value):
        self.data["value"] = value


class NodeInput(IOElement):
    def __init__(self, *args, **kwargs):
        IOElement.__init__(self, *args, **kwargs)
        self.icon.pack(side="left")
        self.IOtype = "input"
        txt = self.name
        self.text.configure(text=txt)
        self.text.pack(side="left")
        
        self.icon.bind("<<Connect>>", self.connect)
        
    def connect(self, event):
        print("Connecting input {}".format(self.name))
        for node in self.node.graph.nodes:
            if node.execname == self.node.execname:
                continue
            for output in node.cvFunctionOutput:
                if output["node_gui"].waiting_connection:
                    self.node.graph.add_connection(self, output["node_gui"])
                    self.connection.inputNode = node
                    self.connection.outputNode = self.node
                    output["node_gui"].waiting_connection = False
                    output["node_gui"].is_connected = True
                    self.is_connected = True
                    output["node_gui"].connection = self.connection
                    output["node_gui"].connection.send_result(output["name"], self.connection.inputNode.last_result)

        print("Input node: {}".format(self.connection.inputNode.execname))
        print("Output node: {}".format(self.connection.outputNode.execname))
        print("Output values: {}".format(self.connection.outputNode.kwvalues))
                    


class NodeOutput(IOElement):
    def __init__(self, *args, **kwargs):
        IOElement.__init__(self, *args, **kwargs)
        self.icon.pack(side="right")
        self.IOtype = "output"

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

        self.line = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=self.width, smooth=True)
    
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
    def __init__(self, nodegraph, fromIO : NodeOutput, toIO : NodeInput):

        self.fromIO = fromIO
        self.toIO = toIO
        self.nodegraph = nodegraph
        
        self.transmittedValue = None
        
        self.line = None
        self.drawLine()

    def drawLine(self):
        startX, startY = self.fromIO.getCenterOnCanvas()
        endX, endY = self.toIO.getCenterOnCanvas()
        
        #self.connectionLine = self.nodegraph.canvas.create_line(startX, startY, endX, endY,  fill="white", width=2, smooth=True)
        line_ids = []
        n = 15
        p = [(startX, startY), (startX + 100, startY), (endX - 100, endY), (endX, endY)]
        for i in range(n+1):
            t = i / n
            x = (p[0][0] * (1-t)**3 + p[1][0] * 3 * t * (1-t)**2 + p[2][0] * 3 * t**2 * (1-t) + p[3][0] * t**3)
            y = (p[0][1] * (1-t)**3 + p[1][1] * 3 * t * (1-t)**2 + p[2][1] * 3 * t**2 * (1-t) + p[3][1] * t**3)

            line_ids.append(self.nodegraph.canvas.create_line(x, y, startX, startY, fill='white', width=2, smooth=1))
            
            startX = x
            startY = y
        
        self.line = line_ids
    
    def updateLine(self):
        for l in self.line:
            self.nodegraph.canvas.delete(l)
        #self.nodegraph.canvas.delete(self.line)
        self.drawLine()
  
    def propagateResult(self, name, result):
        self.toIO.setValue(name, result)
        

    


