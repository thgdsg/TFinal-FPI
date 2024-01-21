import ttkbootstrap as ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser
from PIL import Image, ImageTk, ImageGrab
import cv2 as cv

WIDTH = 750
HEIGHT = 560
file_path = ""
pen_size = 3
pen_color = "black"

# function to open the image file
def open_image():
    global file_path
    file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        global opencvImg
        opencvImg = cv.imread(file_path)
        cv.imshow("Display window", opencvImg)

# function for drawing lines on the opened image
def draw(event):
    global file_path
    if file_path:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")

# function for changing the pen color
def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

# function for erasing lines on the opened image
def erase_lines():
    global file_path
    if file_path:
        canvas.delete("oval")

# the function for saving an image
def save_image():
    global file_path
    if file_path:
        # create a new PIL Image object from the canvas
        image = ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(), canvas.winfo_rooty() + canvas.winfo_height()))
        # open file dialog to select save location and file type
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if file_path:
            if askyesno(title='Save Image', message='Do you want to save this image?'):
                # save the image to a file
                image.save(file_path)

root = ttk.Window(themename="cosmo")
root.title("Image Editor")
root.geometry("510x580+300+110")
root.resizable(0, 0)
icon = ttk.PhotoImage(file='icon.png')
root.iconphoto(False, icon)

# the left frame to contain the 4 buttons
left_frame = ttk.Frame(root, width=200, height=600)
left_frame.pack(side="left", fill="y")

# the right canvas for displaying the drawing
canvas = ttk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()
canvas.bind("<B1-Motion>", draw)

# loading the icons for the 4 buttons
image_icon = ttk.PhotoImage(file = 'add.png').subsample(3, 3)
color_icon = ttk.PhotoImage(file = 'color.png').subsample(3, 3)
erase_icon = ttk.PhotoImage(file = 'erase.png').subsample(3, 3)
save_icon = ttk.PhotoImage(file = 'saved.png').subsample(3, 3)

# button for adding/opening the image file
image_button = ttk.Button(left_frame, image=image_icon, bootstyle="light", command=open_image)
image_button.pack(pady=5)
# button for choosing pen color
color_button = ttk.Button(left_frame, image=color_icon, bootstyle="light", command=change_color)
color_button.pack(pady=5)
# button for erasing the lines drawn over the image file
erase_button = ttk.Button(left_frame, image=erase_icon, bootstyle="light", command=erase_lines)
erase_button.pack(pady=5)
# button for saving the image file
save_button = ttk.Button(left_frame, image=save_icon, bootstyle="light", command=save_image)
save_button.pack(pady=5)

root.mainloop()