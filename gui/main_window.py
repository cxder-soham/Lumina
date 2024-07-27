import tkinter as tk
from tkinter import filedialog, Menu
from PIL import Image, ImageTk, ImageDraw
from image_processing.editor import ImageEditor
from .toolbar import ToolBar


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Photoshop Clone')
        self.root.geometry('800x600')

        self.image = None
        self.image_path = None
        self.draw = None

        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonPress-1>', self.start_paint)

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Crop", command=self.crop_image)
        edit_menu.add_command(label="Resize", command=self.resize_image)
        edit_menu.add_command(label="Rotate", command=self.rotate_image)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.toolbar = ToolBar(root, self)
        menubar.add_cascade(label="Tools", menu=self.toolbar.menu)

        self.current_tool = 'brush'
        self.prev_x = None
        self.prev_y = None

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.image_path = file_path
            self.image = Image.open(file_path)
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[(
                "PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"), ("Bitmap files", "*.bmp")])
            if file_path:
                self.image.save(file_path)

    def display_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def crop_image(self):
        if self.image:
            editor = ImageEditor(self.image_path)
            editor.crop(10, 10, 200, 200)  # Example coordinates
            editor.save('cropped.png')
            self.image = Image.open('cropped.png')
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)

    def resize_image(self):
        if self.image:
            editor = ImageEditor(self.image_path)
            editor.resize(400, 400)  # Example size
            editor.save('resized.png')
            self.image = Image.open('resized.png')
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)

    def rotate_image(self):
        if self.image:
            editor = ImageEditor(self.image_path)
            editor.rotate(90)  # Example rotation
            editor.save('rotated.png')
            self.image = Image.open('rotated.png')
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)

    def start_paint(self, event):
        self.prev_x, self.prev_y = event.x, event.y

    def paint(self, event):
        if self.image and self.draw:
            x, y = event.x, event.y
            if self.current_tool == 'brush':
                self.draw.line([self.prev_x, self.prev_y, x, y],
                               fill=self.toolbar.brush_color, width=self.toolbar.brush_size)
            elif self.current_tool == 'eraser':
                self.draw.line([self.prev_x, self.prev_y, x, y],
                               fill='white', width=self.toolbar.eraser_size)
            self.prev_x, self.prev_y = x, y
            self.display_image()
