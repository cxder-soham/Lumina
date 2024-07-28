import tkinter as tk
from ttkbootstrap import ttk
from tkinter import simpledialog, colorchooser


class ToolBar:
    def __init__(self, root, main_window):
        self.main_window = main_window

        self.brush_size = 5
        self.brush_color = 'black'
        self.eraser_size = 5

        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Brush", command=self.use_brush)
        self.menu.add_command(label="Eraser", command=self.use_eraser)
        self.menu.add_command(label="Set Brush Size",command=self.set_brush_size)
        self.menu.add_command(label="Set Brush Color",command=self.set_brush_color)
        self.menu.add_command(label="Set Eraser Size",command=self.set_eraser_size)

    def use_brush(self):
        self.main_window.current_tool = 'brush'

    def use_eraser(self):
        self.main_window.current_tool = 'eraser'

    def set_brush_size(self):
        size = simpledialog.askinteger(
            "Brush Size", "Enter Brush Size:", initialvalue=self.brush_size, minvalue=1, maxvalue=100)
        if size:
            self.brush_size = size

    def set_brush_color(self):
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color

    def set_eraser_size(self):
        size = simpledialog.askinteger(
            "Eraser Size", "Enter Eraser Size:", initialvalue=self.eraser_size, minvalue=1, maxvalue=100)
        if size:
            self.eraser_size = size