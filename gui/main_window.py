import tkinter as tk
from tkinter import filedialog, simpledialog, Toplevel, HORIZONTAL, X, messagebox
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
from image_processing.editor import ImageEditor
from .toolbar import ToolBar


class MainWindow:
    def __init__(self, root):
        self.tk_image = None
        self.root = root
        self.style = Style(theme="darkly")
        self.current_theme = "darkly"
        self.root.title('bit')
        self.root.geometry('1200x800')

        self.image = None
        self.original_image = None
        self.image_path = None
        self.image_stack = []
        self.redo_stack = []

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.crop_area = None
        self.draw = None

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

        self.crop_option = tk.StringVar(value="dimensions")

        edit_menu = tk.Menu(menubar, tearoff=0)
        crop_menu = tk.Menu(edit_menu, tearoff=0)

        edit_menu.add_command(label="Resize", command=self.resize_image)
        edit_menu.add_command(label="Rotate", command=self.rotate_image)
        edit_menu.add_command(label="Undo(Ctrl+Z)", command=self.undo)
        edit_menu.add_command(label="Redo(Ctrl+Y)", command=self.redo)
        crop_menu.add_radiobutton(label="Dimensions", variable=self.crop_option, value="dimensions")
        crop_menu.add_radiobutton(label="Freeform", variable=self.crop_option, value="freeform")
        edit_menu.add_cascade(label="Select Crop Type", menu=crop_menu)
        edit_menu.add_command(label="Apply Crop", command=self.crop_image)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Bind keyboard shortcuts
        root.bind("<Control-z>", self.undo)
        root.bind("<Control-y>", self.redo)

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
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"),
                                                                ("Bitmap files", "*.bmp")])
            if file_path:
                self.image.save(file_path)

    def display_image(self):
        image = self.image.copy()
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def crop_image(self):
        if self.image:
            editor = ImageEditor(self.image_path)
            editor.crop(10, 10, 200, 200)  # Example coordinates
            editor.save('cropped.png')
            self.image = Image.open('cropped.png')
            self.original_image = self.image.copy()
            self.display_image()
            self.draw = ImageDraw.Draw(self.image)
            if self.crop_option.get() == "dimensions":
                self.crop_dimensions()
            else:
                self.crop_freeform()

    def crop_dimensions(self):
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

    def crop_freeform(self):
        if self.image:
            self.canvas.bind("<ButtonPress-1>", self.on_crop_start)
            self.canvas.bind("<B1-Motion>", self.on_crop_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_crop_end)
            self.crop_area = None
            self.canvas.delete("crop_rectangle")

    def on_crop_start(self, event):
        if self.image:
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)
            if self.rect:
                self.canvas.delete(self.rect)
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                     outline="red", tag="crop_rectangle")

    def on_crop_drag(self, event):
        if self.image:
            cur_x = self.canvas.canvasx(event.x)
            cur_y = self.canvas.canvasy(event.y)
            self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_crop_end(self, event):
        if self.image and self.rect:
            end_x = self.canvas.canvasx(event.x)
            end_y = self.canvas.canvasy(event.y)
            left = int(min(self.start_x, end_x))
            top = int(min(self.start_y, end_y))
            right = int(max(self.start_x, end_x))
            bottom = int(max(self.start_y, end_y))

            self.image_stack.append(self.image.copy())
            editor = ImageEditor(self.image)
            editor.crop(left, top, right, bottom)
            self.image = editor.image
            self.display_image()

            self.canvas.delete(self.rect)
            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

    def resize_image(self):
        if self.image:
            def on_resize_input(value):
                try:
                    width, height = map(int, value.split())
                    self.image_stack.append(self.image.copy())
                    editor = ImageEditor(self.image)
                    editor.resize(width, height)
                    self.image = editor.image
                    self.display_image()
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter two integers separated by space.")

            InputDialog(self.root, "Resize Image", "Enter width and height separated by space:", "400 400",
                        on_resize_input)

    def rotate_image(self):
        if self.image:
            def on_rotate_input(value):
                try:
                    degrees = int(value)
                    self.image_stack.append(self.image.copy())
                    editor = ImageEditor(self.image)
                    editor.rotate(degrees)
                    self.image = editor.image
                    self.display_image()
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid integer.")

            InputDialog(self.root, "Rotate Image", "Enter rotation degrees:", "90", on_rotate_input)

    def undo(self, event=None):
        if len(self.image_stack) > 1:
            self.redo_stack.append(self.image_stack.pop())
            self.image = self.image_stack[-1].copy()
            self.display_image()

    def redo(self, event=None):
        if self.redo_stack:
            self.image_stack.append(self.redo_stack.pop())
            self.image = self.image_stack[-1].copy()
            self.display_image()


class InputDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt, default_value, callback):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()

        self.callback = callback

        self.label = tk.Label(self, text=prompt)
        self.label.pack(pady=10)

        self.entry = tk.Entry(self)
        self.entry.insert(0, default_value)
        self.entry.pack(pady=5)

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.bind("<Return>", lambda event: self.on_ok())
        self.bind("<Escape>", lambda event: self.on_cancel())

    def on_ok(self):
        value = self.entry.get()
        self.callback(value)
        self.destroy()

    def on_cancel(self):
        self.destroy()


class FreeformCropDialog(tk.Toplevel):
    def __init__(self, parent, title, callback):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()

        self.callback = callback

        self.label = tk.Label(self, text="Enter crop coordinates as x1, y1, x2, y2:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.bind("<Return>", lambda event: self.on_ok())
        self.bind("<Escape>", lambda event: self.on_cancel())

    def on_ok(self):
        value = self.entry.get()
        try:
            x1, y1, x2, y2 = map(int, value.split())
            self.callback(x1, y1, x2, y2)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter four integers separated by spaces.")
        self.destroy()

    def on_cancel(self):
        self.destroy()
