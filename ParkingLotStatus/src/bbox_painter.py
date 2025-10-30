#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Standard imports
import json

# Third-party imports
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


# In[2]:


class BBoxPainter:
    """
    This class provides functionality of:
        1. Upload an image
        2. Define bounding boxes for parking zones
        3. Save the points of bounding boxes to a JSON file
    """
    def __init__(self): # constructor
        self.json_filepath = None

        self.tk = tk
        self.filedialog = filedialog
        self.messagebox = messagebox
        self._setup_ui()
        self._init_props()
        self.master.mainloop() # master: the main Tkinter window

    def _setup_ui(self): # set up Tkinter GUI components
        self.master = self.tk.Tk()
        self.master.title("BBox Painter")
        self.master.resizable(False, False)  # Prevent window resizing

        # canvas for image display
        self.canvas = self.tk.Canvas(self.master, bg='white')
        self.canvas.pack(side=self.tk.BOTTOM)

        # button frame
        button_frame = self.tk.Frame(self.master)
        button_frame.pack(side=self.tk.TOP)

        for text, cmd in [
            ("Upload Image", self.upload_img),
            ("Remove Last BBox", self._remove_last_bbox),
            ("Save", self._save_to_json),
        ]:
            self.tk.Button(button_frame, text=text, command=cmd).pack(side=self.tk.LEFT)

    def _init_props(self): # initialize properties
        self.image = self.canvas_image = None
        self.bboxes, self.current_bbox = [], []
        self.imgw, self.imgh = 0, 0
        self.canvas_max_width, self.canvas_max_height = 1020, 500 # Max display dimensions

    def upload_img(self): # upload an image, resize it to fit the canvas, and display it
        img_filepath = self.filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if not img_filepath:
            return

        self.image = Image.open(img_filepath)
        self.imgw, self.imgh = self.image.size

        # calculate scaling factor while maintaining aspect ratio
        aspect_ratio = self.imgw / self.imgh
        canvas_width = min(self.canvas_max_width, self.imgw) if aspect_ratio > 1 else int(self.canvas_max_height * aspect_ratio)
        canvas_height = min(self.canvas_max_height, self.imgh) if aspect_ratio <= 1 else int(canvas_width / aspect_ratio)

        # configure canvas with scaled dimensions
        self.canvas.config(width=canvas_width, height=canvas_height)
        self.canvas_image = ImageTk.PhotoImage(self.image.resize((canvas_width, canvas_height), Image.LANCZOS))
        self.canvas.create_image(0, 0, anchor=self.tk.NW, image=self.canvas_image)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        self.bboxes.clear()
        self.current_bbox.clear()

    def _on_canvas_click(self, event): # handle mouse click event to add points for bbox
        self.current_bbox.append((event.x, event.y))
        self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="red")

        if len(self.current_bbox) == 4:
            self.bboxes.append(self.current_bbox.copy())
            self._draw_bbox(self.current_bbox)
            self.current_bbox.clear()

    def _draw_bbox(self, box): # triggered once upon bbox formation, draw a bbox on the canvas
        for i in range(4):
            x1, y1 = box[i]
            x2, y2 = box[(i + 1) % 4] # connect back to the first point for the last line at i=3
            self.canvas.create_line(x1, y1, x2, y2, fill='red', width=2)

    def _remove_last_bbox(self): # remove the last bbox
        if not self.bboxes:
            self.messagebox.showwarning("Warning", "No bounding boxes to remove.")
            return
        self.bboxes.pop()
        self._redraw_canvas()

    def _redraw_canvas(self): # triggered on _remove_last_bbox; redraw canvas
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=self.tk.NW, image=self.canvas_image)
        for bbox in self.bboxes:
            self._draw_bbox(bbox)

    def _save_to_json(self): # save the bbox data to a JSON file
        if not self.bboxes:
            self.messagebox.showwarning("Warning", "No bounding boxes to save.")
            return

        # scale points back to original image coordinates
        scale_w = self.imgw / self.canvas.winfo_width()
        scale_h = self.imgh / self.canvas.winfo_height()
        data = [{"points": [(int(x*scale_w), int(y*scale_h)) for x, y in bbox]} for bbox in self.bboxes]

        with open('../output/bboxes.json', 'w') as f:
            json.dump(data, f, indent=4)
        self.messagebox.showinfo("Success", "Bounding boxes saved to output/bboxes.json")

        self.saved_filepath = "../output/bboxes.json"  

    def get_json_filepath(self):
        return self.json_filepath

