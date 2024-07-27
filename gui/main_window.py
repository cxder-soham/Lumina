import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
from image_processing.editor import ImageEditor

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Photoshop Clone')
        self.root.geometry('800x600')

        self.image = None
        self.image_path = None
        self.image_stack = []
        self.redo_stack = []

        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

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
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        menubar.add_cascade(label="Edit", menu=edit_menu)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.image_path = file_path
            self.image = Image.open(file_path)
            self.image_stack = [self.image.copy()]
            self.redo_stack = []
            self.display_image()

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"), ("Bitmap files", "*.bmp")])
            if file_path:
                self.image.save(file_path)

    def display_image(self):
        image = self.image.copy()
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def crop_image(self):
        if self.image:
            left = simpledialog.askinteger("Input", "Left:")
            top = simpledialog.askinteger("Input", "Top:")
            right = simpledialog.askinteger("Input", "Right:")
            bottom = simpledialog.askinteger("Input", "Bottom:")
            if None not in (left, top, right, bottom):
                self.image_stack.append(self.image.copy())
                editor = ImageEditor(self.image)
                editor.crop(left, top, right, bottom)
                self.image = editor.image
                self.display_image()

    def resize_image(self):
        if self.image:
            width = simpledialog.askinteger("Input", "Width:")
            height = simpledialog.askinteger("Input", "Height:")
            if None not in (width, height):
                self.image_stack.append(self.image.copy())
                editor = ImageEditor(self.image)
                editor.resize(width, height)
                self.image = editor.image
                self.display_image()

    def rotate_image(self):
        if self.image:
            degrees = simpledialog.askinteger("Input", "Degrees:")
            if degrees is not None:
                self.image_stack.append(self.image.copy())
                editor = ImageEditor(self.image)
                editor.rotate(degrees)
                self.image = editor.image
                self.display_image()

    def undo(self):
        if len(self.image_stack) > 1:
            self.redo_stack.append(self.image_stack.pop())
            self.image = self.image_stack[-1].copy()
            self.display_image()

    def redo(self):
        if self.redo_stack:
            self.image_stack.append(self.redo_stack.pop())
            self.image = self.image_stack[-1].copy()
            self.display_image()
