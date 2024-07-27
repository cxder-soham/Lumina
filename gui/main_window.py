import tkinter as tk
from tkinter import filedialog, simpledialog
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
from image_processing.editor import ImageEditor
from .toolbar import ToolBar


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme="darkly") 
        self.current_theme = "darkly" 
        self.root.title('Photoshop Clone')
        self.root.geometry('1200x800')

        self.image = None
        self.image_path = None
        self.draw = None
        self.undo_stack = []
        self.redo_stack = []

        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
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

        filters_menu = tk.Menu(menubar, tearoff=0)
        filters_menu.add_command(label="Blur", command=self.apply_blur)
        filters_menu.add_command(label="Sharpen", command=self.apply_sharpen)
        filters_menu.add_command(
            label="Brightness", command=self.apply_brightness)
        filters_menu.add_command(label="Contrast", command=self.apply_contrast)
        menubar.add_cascade(label="Filters", menu=filters_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        menubar.add_cascade(label="View", menu=view_menu)

        self.current_tool = 'brush'
        self.prev_x = None
        self.prev_y = None

    def toggle_theme(self):
        if self.current_theme == "darkly":
            self.style.theme_use("cosmo")
            self.current_theme = "cosmo"
        else:
            self.style.theme_use("darkly")
            self.current_theme = "darkly"

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.image_path = file_path
            self.image = Image.open(file_path)
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)
            self.clear_history()

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
            self.push_undo()
            editor = ImageEditor(self.image_path)
            editor.crop(10, 10, 200, 200)  # Example coordinates
            editor.save('cropped.png')
            self.image = Image.open('cropped.png')
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)

    def resize_image(self):
        if self.image:
            self.push_undo()
            editor = ImageEditor(self.image_path)
            editor.resize(400, 400)  # Example size
            editor.save('resized.png')
            self.image = Image.open('resized.png')
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)

    def rotate_image(self):
        if self.image:
            self.push_undo()
            editor = ImageEditor(self.image_path)
            editor.rotate(90)  # Example rotation
            editor.save('rotated.png')
            self.image = Image.open('rotated.png')
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)

    def start_paint(self, event):
        self.push_undo()
        self.prev_x, self.prev_y = event.x, event.y

    def paint(self, event):
        if self.image and self.draw:
            x, y = event.x, event.y
            if self.current_tool == 'brush':
                self.draw.line([self.prev_x, self.prev_y, x, y],fill=self.toolbar.brush_color, width=self.toolbar.brush_size)
            elif self.current_tool == 'eraser':
                self.draw.line([self.prev_x, self.prev_y, x, y],fill='white', width=self.toolbar.eraser_size)
            self.prev_x, self.prev_y = x, y
            self.display_image()

    def apply_filter(self, filter_func):
        if self.image:
            self.push_undo()
            self.image = filter_func(self.image)
            self.display_image()

    def apply_blur(self):
        self.apply_filter(lambda img: img.filter(ImageFilter.GaussianBlur(2)))

    def apply_sharpen(self):
        self.apply_filter(lambda img: img.filter(ImageFilter.SHARPEN))

    def apply_brightness(self):
        factor = simpledialog.askfloat(
            "Brightness", "Enter brightness factor (1.0 = original):", minvalue=0.0, maxvalue=10.0, initialvalue=1.0)
        if factor is not None:
            self.apply_filter(
                lambda img: ImageEnhance.Brightness(img).enhance(factor))

    def apply_contrast(self):
        factor = simpledialog.askfloat(
            "Contrast", "Enter contrast factor (1.0 = original):", minvalue=0.0, maxvalue=10.0, initialvalue=1.0)
        if factor is not None:
            self.apply_filter(
                lambda img: ImageEnhance.Contrast(img).enhance(factor))

    def push_undo(self):
        self.undo_stack.append(self.image.copy())
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.image.copy())
            self.image = self.undo_stack.pop()
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)

    def clear_history(self):
        self.undo_stack.clear()
        self.redo_stack.clear()
