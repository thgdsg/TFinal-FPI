import math
import ttkbootstrap as ttk
from tkinter import Label, filedialog
from tkinter.messagebox import askyesno
from PIL import ImageGrab, Image, ImageTk
import cv2 as cv
import numpy as np
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import matplotlib.pyplot as plt
import skimage as ski
import sintese as sint

WIDTH = 750
HEIGHT = 560
file_path = ""
pen_size = 3
pen_color = "black"
h = 10
samples = 100
crop_img = np.zeros((h*2,(h*2)+samples, 3),  dtype = "uint8")

# function to open the image file
def open_image():
    global file_path
    file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        global opencvImg
        opencvImg = cv.imread(file_path)
        cv.imshow("Imagem", opencvImg)
        cv.setMouseCallback("Imagem", mouse_drawing)

def mouse_drawing(event, x, y, flags, params):
    global r, c, img, x_antigo, y_antigo, snake
    if event == cv.EVENT_LBUTTONDOWN:
        img = ski.util.img_as_float(opencvImg)
        img = img[:, :, ::-1]
        x_antigo = x
        y_antigo = y

    if event == cv.EVENT_LBUTTONUP:
        c = np.linspace(x_antigo, x, samples)
        r = np.linspace(y_antigo, y, samples)
        init = np.array([r, c]).T
        snake = active_contour(gaussian(img, 3, preserve_range=False),
                       init, boundary_condition='fixed',
                       alpha=0.1, beta=20.0, w_line=-1, w_edge=5, gamma=0.1)

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.imshow(img, cmap=plt.cm.gray)
        ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
        ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
        ax.set_xticks([]), ax.set_yticks([])
        ax.axis([0, img.shape[1], img.shape[0], 0])
        
        for p in range(len(snake)-4):
            y = int(snake[p][0])
            x = int(snake[p][1])
            radians = math.atan2((y-snake[p+4][0]), (x-snake[p+4][1]))
            degrees = math.degrees(radians)
            sample = opencvImg[y-h:y+h, x-h:x+h]
            image_center = tuple(np.array(sample.shape[1::-1]) / 2)
            rot_mat = cv.getRotationMatrix2D(image_center, degrees, 1.0)
            result = cv.warpAffine(sample, rot_mat, sample.shape[1::-1], flags=cv.INTER_LINEAR)
            for i in range(2*h):
                for j in range(int(3*h/4)):
                    if np.any(result[i][j]>20):
                        crop_img[i, j+p] = result[i][int(h/4)+j]
         
        (height, width) = crop_img.shape[:2]
        cv.imshow("cropped", cv.resize(crop_img, (width*2,height*2)))
        
        plt.show()
    if event == cv.EVENT_RBUTTONDOWN:
        img = ski.util.img_as_float(opencvImg)
        img = img[:, :, ::-1]

        s = np.linspace(0, 2*np.pi, 400)
        r = y + 20*np.sin(s)
        c = x + 20*np.cos(s)
        init = np.array([r, c]).T

        snake = active_contour(gaussian(img, 3, preserve_range=False),
                            init, alpha=0.015, beta=20, gamma=0.001)

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.imshow(img, cmap=plt.cm.gray)
        ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
        ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
        ax.set_xticks([]), ax.set_yticks([])
        ax.axis([0, img.shape[1], img.shape[0], 0])

        plt.show()


# function for drawing lines on the opened image
def draw(event):
    global file_path
    if file_path:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        
        canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")

# function for changing the pen color
def sintetiza_textura():
    imagem = Image.fromarray(opencvImg)
    tamanho_bloco = int(imagem.width / 8)
    novatextura = sint.quilt(imagem,tamanho_bloco,8,"Cut")
    novatextura.show()
    pass

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
color_icon = ttk.PhotoImage(file = 'faztextura.png').subsample(3, 3)
erase_icon = ttk.PhotoImage(file = 'erase.png').subsample(3, 3)
save_icon = ttk.PhotoImage(file = 'saved.png').subsample(3, 3)

# button for adding/opening the image file
image_button = ttk.Button(left_frame, image=image_icon, bootstyle="light", command=open_image)
image_button.pack(pady=5)
# button for choosing pen color
color_button = ttk.Button(left_frame, image=color_icon, bootstyle="light", command=sintetiza_textura)
color_button.pack(pady=5)
# button for erasing the lines drawn over the image file
erase_button = ttk.Button(left_frame, image=erase_icon, bootstyle="light", command=erase_lines)
erase_button.pack(pady=5)
# button for saving the image file
save_button = ttk.Button(left_frame, image=save_icon, bootstyle="light", command=save_image)
save_button.pack(pady=5)

root.mainloop()