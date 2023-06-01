import numpy as np
import cv2
import tkinter 
from PIL import Image, ImageTk

# Load an color image
func = getattr(cv2, "imread")
img = func('assets/images/icons/IOGreen-16px.png')

img = cv2.imread('assets/images/icons/IOGreen-16px.png')

#Rearrang the color channel
b,g,r = cv2.split(img)
img = cv2.merge((r,g,b))

# A root window for displaying objects
root = tkinter.Tk()  

# Convert the Image object into a TkPhoto object
im = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im) 

# Put it in the display window
tkinter.Label(root, image=imgtk).pack() 

root.mainloop() # Start the GUI