import tkinter as tk
import cv2
from PIL import Image, ImageTk


class NodeSideBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, bg="#444444", **kwargs)
        self.parent = parent
        self.node = None
        self.width = 200

        self.dragHandle = tk.Frame(self, bg="#444444", width=6, cursor="sb_h_double_arrow")
        self.dragHandle.pack(fill="y", side="left")

        self.contentFrame = tk.Frame(self, bg="#444444")
        self.contentFrame.pack(fill="both", expand=True, side="left")

        self.previewCollapsable = tk.Frame(self.contentFrame, bg="#444444")
        self.previewCollapsable.pack(fill="x", side="top", padx=5, pady=5)

        self.previewItem = tk.Frame(self.previewCollapsable, bg="#444444")
        self.previewItem.pack(fill="x")

        self.arrow_right_image = tk.PhotoImage(file="assets\images\icons\collaps_arrow_left_16px.png")
        self.arrow_down_image = tk.PhotoImage(file="assets\images\icons\collaps_arrow_down_16px.png")

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

        self.dragHandle.bind("<Enter>", self.dragHandleHover)
        self.dragHandle.bind("<Leave>", self.dragHandleUnhover)
        self.dragHandle.bind("<B1-Motion>", self.dragHandleMove)

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

        print("maxw: " + str(maxw) + " maxh: " + str(maxh) + " w: " + str(w) + " h: " + str(h))

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
        self.img = self.node.run()
    
    def set_node(self, node):
        self.node = node
        #self.previewTitle.config(text=node.title.cget("text"))
        self.update_sidebar_content(None)