import tkinter as tk
import cv2
import json
from PIL import Image, ImageTk


class NodeSideBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, bg="#444444", **kwargs)
        self.parent = parent
        self.node = None
        self.width = 200

        self.enums_data = json.load(open("DATA/enums.json"))
        self.entries = []

        self.playFrame = tk.Frame(self, bg="#444444")
        self.playFrame.pack()
        self.playimg = tk.PhotoImage(file="assets/images/icons/collaps_arrow_left_16px.png")
        self.playIcon = tk.Label(self.playFrame, image=self.playimg, bg="#444444")
        self.playIcon.pack()

        self.dragHandle = tk.Frame(self, bg="#444444", width=6, cursor="sb_h_double_arrow")
        self.dragHandle.pack(fill="y", side="left")

        self.contentFrame = tk.Frame(self, bg="#444444")
        self.contentFrame.pack(fill="both", expand=True, side="left")

        self.previewCollapsable = tk.Frame(self.contentFrame, bg="#444444")
        self.previewCollapsable.pack(fill="x", side="top", padx=5, pady=5)

        self.previewItem = tk.Frame(self.previewCollapsable, bg="#444444")
        self.previewItem.pack(fill="x")

        self.arrow_right_image = tk.PhotoImage(file="assets/images/icons/collaps_arrow_left_16px.png")
        self.arrow_down_image = tk.PhotoImage(file="assets/images/icons/collaps_arrow_down_16px.png")

        self.previewImage = tk.Label(self.previewItem, image=self.arrow_right_image, bg="#444444")
        self.previewImage.pack(fill="x", side="left")

        self.previewTitle = tk.Label(self.previewItem, text="Preview", bg="#444444", fg="#ffffff", font=("Open Sans", 12))
        self.previewTitle.pack(fill="x", side="left")

        self.img = cv2.imread('assets/images/test/skyfhd.jpg')
        self.im = Image.fromarray(self.img)
        self.imgtk = ImageTk.PhotoImage(image=self.im) 

        self.preview = tk.Label(self.previewCollapsable, image=self.imgtk, bg="#999999", fg="#ffffff", font=("Open Sans", 12))
        self.preview.pack(fill="x", side="top", padx=5, pady=5)

        self.previewCollapsable.bind("<ButtonPress-1>", self.toggle_preview)

        self.paramsFrame = tk.Frame(self.contentFrame, bg="#444444")
        # self.paramsFrame.pack(fill="both", expand=True, side="left")
        # self.paramsLabel = tk.Label(self.paramsFrame, text="null", bg="#444444", fg="#ffffff", font=("Open Sans", 12))
        # self.paramsLabel.pack(fill="x", side="left")

        self.dragHandle.bind("<Enter>", self.dragHandleHover)
        self.dragHandle.bind("<Leave>", self.dragHandleUnhover)
        self.dragHandle.bind("<B1-Motion>", self.dragHandleMove)

        self.playIcon.bind("<ButtonPress-1>", self.run_nodes)

        self.bind("<Configure>", self.update_sidebar)

        


    def dragHandleHover(self, event):
        self.dragHandle.config(bg="#0070FF")

    def dragHandleUnhover(self, event):
        self.dragHandle.config(bg="#444444")

    def dragHandleMove(self, event):
        self.width = self.width - event.x
        self.place(x = self.parent.winfo_width() - self.width, y = 0, width = self.width, height = self.parent.winfo_height())
        print(self.width)

    def toggle_preview(self, event):
        if self.previewItem.winfo_height() == 0:
            self.previewItem.pack(fill="both", expand=True)
        else:
            self.previewItem.pack_forget()

    def show_node(self, node):
        self.node = node

    def re_place(self):
        self.place(x = self.parent.winfo_width() - self.width, y = 0, width = self.width, height = self.parent.winfo_height())

    def update_sidebar(self, event):
        #resize the image to be contained in the preview mantaining the aspect ratio
        maxw = self.preview.winfo_width()
        maxh = self.preview.winfo_height()
        w = self.img.shape[1]
        h = self.img.shape[0]

        # print("maxw: " + str(maxw) + " maxh: " + str(maxh) + " w: " + str(w) + " h: " + str(h))

        rimg = []
        #if w > h:
        rimg = cv2.resize(self.img, (maxw, int(maxw*h/w)))
        #else:
        #    rimg = cv2.resize(self.img, (int(maxh*w/h), maxh))

        b,g,r = cv2.split(rimg)
        ruimg = cv2.merge((r,g,b))
        self.im = Image.fromarray(ruimg)
        self.imgtk = ImageTk.PhotoImage(image=self.im)
        self.preview.config(image=self.imgtk)
    
    def update_sidebar_content(self, event):
        self.entries.clear()
        self.img = self.node.run()

        # clear actual content
        for w in self.paramsFrame.winfo_children():
            w.destroy()

        # add new params
        for i, input in enumerate(self.node.cvFunctionArgs):
            txt = input["name"]
            txt_label = tk.Label(self.paramsFrame, text=txt, bg="#444444", fg="#ffffff", font=("Open Sans", 12))
            txt_label.pack()
            is_enum = False

            self.entries.append(tk.StringVar(self, name=input["name"]))
            if input["value"] is not None:
                self.setvar(name=input["name"], value=input["value"])
            # if input["type"] == "enum":
            for enum in self.enums_data["enums"]:
                if input["type"] == enum["name"]:
                    # self.entries.append(tk.StringVar())
                    # self.entries[i].set(input["value"])
                    menu = tk.ttk.Combobox(self.paramsFrame, textvariable=self.entries[i])
                    # menu["values"] = self.enums_data["enums"]["values"]
                    values_list = []
                    for val in enum["values"]:
                        values_list.append(val)
                    menu["values"] = tuple(values_list)
                    # print(menu["values"])
                    menu["state"] = 'readonly'
                    menu.pack()
                    menu.bind("<<ComboboxSelected>>", lambda e: self.set_combo_value(e, input, i))
                    is_enum = True
            if not is_enum:
                # self.entries.append(tk.StringVar())
                entry = tk.Entry(self.paramsFrame, textvariable=self.entries[i])
                btn = tk.Button(self.paramsFrame, text='OK', command = lambda: self.set_button_value(input, i))
                entry.pack()
                btn.pack()
            

        
        self.paramsFrame.pack()
        for input in self.node.cvFunctionArgs:
            print(input["value"]) 


    def set_node(self, node):
        self.node = node
        #self.previewTitle.config(text=node.title.cget("text"))
        self.update_sidebar_content(None)

    def run_nodes(self, event):
        # for node in self.parent.nodes:
        #     result = node.run()
        #     i = 0               # output value index
        #     for output in node.outputElements:
        #         output.connection.outputNode.values[i] = result.copy()

        self.parent.nodes[0].run_chain()

    
    def set_combo_value(self, event, input, id):
        print("Index: {}".format(id))
        val = self.getvar(name=input["name"])
        # print("Value: {}".format(val))
        input["value"] = val
        # print("Assigned value: {}".format(input["value"]))
        self.node.values[id] = getattr(cv2, input["value"])
        print(self.node.values[id])
        self.node.kwvalues[input["name"]] = getattr(cv2, input["value"])
        print(self.node.kwvalues[input["name"]])
        
    def set_button_value(self, input, id):
        print(input["name"])
        input["value"] = self.getvar(name=input["name"])
        print(input["value"])
        self.node.values[id] = getattr(cv2, input["value"])
        print(self.node.values[id])
        self.node.kwvalues[input["name"]] = getattr(cv2, input["value"])
        print(self.node.kwvalues[input["name"]])
        
