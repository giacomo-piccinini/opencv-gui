import tkinter as tk
import json
import cv2

TITLE_COLOR = "#333333"
BODY_COLOR = "#444444"

class Node(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg=BODY_COLOR)
        self.parent = parent

        self.titleFrame = tk.Frame(self, bg=TITLE_COLOR)
        self.titleFrame.pack(fill="x", side="top")

        self.title = tk.Label(self.titleFrame, text="Null", bg=TITLE_COLOR, fg="#ffffff", font=("Open Sans", 12), anchor="w")
        self.title.pack(fill="x", side="left", padx=5, pady=5)

        self.body = tk.Frame(self, bg=BODY_COLOR)
        self.body.pack(fill="both", expand=True)


class CVNode(Node):
    def __init__(self, parent, *args, **kwargs):
        Node.__init__(self, parent, *args, **kwargs)
        self.cvFunction = None
        self.cvFunctionArgs = None
        self.inputElements = []
        self.outputElements = []

class IMREADNode(CVNode):
    def __init__(self, parent, execname, *args, **kwargs):
        CVNode.__init__(self, parent, *args, **kwargs)

        self.data = json.load(open("DATA/cv2.json"))

        self.execname = execname

        self.var1 = 'assets/images/icons/IOGreen-16px.png'
        self.var2 = 1

        self.values = [self.var1, self.var2]

        self.cvFunctionArgs = []
        self.cvFunctionOutput = []

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
                "type": arg["name"],
                "value": arg["default"] if "default" in arg else None
            }
            self.cvFunctionArgs.append(dd)  
        for ret in self.funcdata["return"]:
            dd = {
                "type": ret["type"]
            }
            self.cvFunctionOutput.append(dd)

    def init_gui(self):
        self.title.config(text=self.execname)
        for output in self.cvFunctionOutput:
            self.outputElements.append(NodeOutput(self.body))
        for input in self.cvFunctionArgs:
            self.inputElements.append(NodeInput(self.body))


    def run(self):
        func = getattr(cv2, self.funcdata["name"])
        res = func(*self.values)
        self.last_result = res
        return res
    
    def run_chain(self):
        self.run()
        output.conenssione.nodeoconnesso.run_chain()


class IOElement(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg=BODY_COLOR)
        self.connected = False
        self.normal = tk.PhotoImage(file="assets/images/icons/IOMedGrey-16px.png")
        self.hovered = tk.PhotoImage(file="assets/images/icons/IOLightGrey-16px.png")
        self.connected = tk.PhotoImage(file="assets/images/icons/IOGreen-16px.png")

        self.text = tk.Label(self, text="null", bg=BODY_COLOR, fg="#ffffff", font=("Open Sans", 10))
        self.icon = tk.Label(self, image=self.normal, bg=BODY_COLOR)

        self.pack(side="top", fill="x")

        self.icon.bind("<Enter>", self.hover)
        self.icon.bind("<Leave>", self.unhover)
        self.icon.bind("<ButtonPress-1>", self.connect)
    
    def hover(self, event):
        self.icon.config(image=self.hovered)
    
    def unhover(self, event):
        self.icon.config(image=self.normal)
    
    def connect(self, event):
        self.icon.config(image=self.connected)
        x = event.widget.winfo_rootx() - self.parent
class NodeInput(IOElement):
    def __init__(self, *args, **kwargs):
        IOElement.__init__(self, *args, **kwargs)
        self.icon.pack(side="left")
        self.text.pack(side="left")


class NodeOutput(IOElement):
    def __init__(self, *args, **kwargs):
        IOElement.__init__(self, *args, **kwargs)
        self.icon.pack(side="right")
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