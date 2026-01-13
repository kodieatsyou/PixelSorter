import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from enum import Enum
import numpy as np


class Mode(Enum):
    VERTICAL = 1
    HORIZONTAL = 2


class App:
    def __init__(self, master):
        self.master = master

        self.original_image = None
        self.sorted_image = None
        self.original_image_raw = None
        self.sorted_image_raw = None

        self.light_threshold = 50
        self.dark_threshold = 30

        # ---- Main layout frames ----
        left_frame = tk.Frame(master, width=300, height=850, bg="white")
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ns")
        left_frame.grid_propagate(False)

        right_frame = tk.Frame(master, width=1050, height=1050, bg="white")
        right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        right_frame.grid_propagate(False)

        # Allow the right side to expand
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # ---- Original image preview\ ----
        frame_original_image_border = tk.Frame(
            left_frame,
            width=280,
            height=280,
            bg="white",
            highlightbackground="black",
            highlightthickness=2,
        )
        frame_original_image_border.grid(row=0, column=0, padx=10, pady=5, sticky="n")
        frame_original_image_border.grid_propagate(False)
        frame_original_image_border.grid_columnconfigure(0, weight=1)

        frame_original_image_header = tk.Frame(frame_original_image_border, width=250, height=40, bg="white")
        frame_original_image_header.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        frame_original_image_header.grid_propagate(False)
        frame_original_image_header.grid_columnconfigure(0, weight=1)

        original_image_header = tk.Label(frame_original_image_header, text="Original Image", bg="white", fg="black")
        original_image_header.grid(row=0, column=0, padx=10, pady=5)

        frame_original_image = tk.Frame(frame_original_image_border, width=200, height=200, bg="white")
        frame_original_image.grid(row=1, column=0, padx=10, pady=5)
        frame_original_image.grid_propagate(False)
        frame_original_image.grid_columnconfigure(0, weight=1)
        frame_original_image.grid_rowconfigure(0, weight=1)

        self.original_image_holder = tk.Label(frame_original_image, image=None, bg="black", fg="black")
        self.original_image_holder.grid(row=0, column=0)

        # ---- Sorted image preview ----
        frame_sorted_image = tk.Frame(right_frame, bg="white")
        frame_sorted_image.grid(row=0, column=0, sticky="nsew")
        frame_sorted_image.grid_rowconfigure(0, weight=1)
        frame_sorted_image.grid_columnconfigure(0, weight=1)

        self.sorted_image_holder = tk.Label(frame_sorted_image, image=None, bg="black", fg="black")
        self.sorted_image_holder.grid(row=0, column=0, sticky="nsew")

        # ---- Tools ----
        tool_bar = tk.Frame(left_frame, width=280, height=550, bg="white", highlightbackground="black", highlightthickness=2)
        tool_bar.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        tool_bar.grid_propagate(False)
        tool_bar.grid_columnconfigure(0, weight=1)

        tk.Label(tool_bar, text="Tools", bg="white", fg="black").grid(row=0, column=0, padx=5, pady=3)

        tk.Button(tool_bar, text="Select Image", command=self.get_image).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(tool_bar, text="Vertical Sort", command=self.vertical_sort).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(tool_bar, text="Horizontal Sort", command=self.horizontal_sort).grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(tool_bar, text="Export Sorted Image", command=self.export_image).grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        tk.Label(tool_bar, text="Lightness threshold:", bg="white", fg="black").grid(
            row=5, column=0, padx=5, pady=(20, 3), sticky="w"
        )
        self.lightness_text = tk.Text(tool_bar, background="white", fg="black", width=20, height=1)
        self.lightness_text.grid(row=6, column=0, padx=5, pady=3, sticky="w")
        self.lightness_text.insert(tk.END, str(self.light_threshold))

        tk.Label(tool_bar, text="Darkness threshold:", bg="white", fg="black").grid(
            row=7, column=0, padx=5, pady=(10, 3), sticky="w"
        )
        self.darkness_text = tk.Text(tool_bar, background="white", fg="black", width=20, height=1)
        self.darkness_text.grid(row=8, column=0, padx=5, pady=3, sticky="w")
        self.darkness_text.insert(tk.END, str(self.dark_threshold))

    def get_image(self):
        filename = filedialog.askopenfilename(
            initialdir="/Project/pixelsorter/input",
            title="Select An Image",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")),
        )
        if not filename:
            return

        self.original_image_raw = Image.open(filename)
        self.original_image = ImageTk.PhotoImage(self.original_image_raw.resize((200, 200)))
        self.sorted_image = ImageTk.PhotoImage(self.original_image_raw)

        self.original_image_holder.configure(image=self.original_image)
        self.sorted_image_holder.configure(image=self.sorted_image)
        self.master.update()

    def export_image(self):
        if self.sorted_image is None:
            return
        imgpil = ImageTk.getimage(self.sorted_image)
        imgpil.save("./output/export.png", "PNG")

    def vertical_sort(self):
        if self.original_image_raw is None:
            return

        self.light_threshold = int(self.lightness_text.get("1.0", "end-1c"))
        self.dark_threshold = int(self.darkness_text.get("1.0", "end-1c"))
        data = np.array(self.original_image_raw)

        image_height = data.shape[0]
        image_width = data.shape[1]
        mask = self.get_mask(data, self.light_threshold, self.dark_threshold)
        intervals = self.get_intervals(mask, image_width, image_height, Mode.VERTICAL)

        for interval in intervals:
            interval_details = interval[:3]
            interval_pixels = self.quicksort(interval[3:], data)
            self.map_interval_to_data((interval_details + interval_pixels), data)

        self.sorted_image_raw = Image.fromarray(data)
        self.sorted_image = ImageTk.PhotoImage(self.sorted_image_raw)
        self.sorted_image_holder.configure(image=self.sorted_image)
        self.master.update()

    def horizontal_sort(self):
        if self.original_image_raw is None:
            return

        self.light_threshold = int(self.lightness_text.get("1.0", "end-1c"))
        self.dark_threshold = int(self.darkness_text.get("1.0", "end-1c"))
        data = np.array(self.original_image_raw)

        image_height = data.shape[0]
        image_width = data.shape[1]
        mask = self.get_mask(data, self.light_threshold, self.dark_threshold)
        intervals = self.get_intervals(mask, image_width, image_height, Mode.HORIZONTAL)

        for interval in intervals:
            interval_details = interval[:3]
            interval_pixels = self.quicksort(interval[3:], data)
            self.map_interval_to_data((interval_details + interval_pixels), data)

        self.sorted_image_raw = Image.fromarray(data)
        self.sorted_image = ImageTk.PhotoImage(self.sorted_image_raw)
        self.sorted_image_holder.configure(image=self.sorted_image)
        self.master.update()

    def map_interval_to_data(self, interval, data):
        if interval[0] == Mode.VERTICAL:
            start_y = interval[2]
            x = interval[1]
            for i in range(3, len(interval)):
                y = (start_y + i) - 3
                if x >= data.shape[1]:
                    continue
                if y >= data.shape[0]:
                    continue
                data[y, x] = data[interval[i][1]][interval[i][0]]

        if interval[0] == Mode.HORIZONTAL:
            start_x = interval[1]
            y = interval[2]
            for i in range(3, len(interval)):
                x = (start_x + i) - 3
                if x >= data.shape[1]:
                    continue
                if y >= data.shape[0]:
                    continue
                data[y, x] = data[interval[i][1]][interval[i][0]]

    def get_pixel_lightness(self, pixel):
        return (0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2])

    def get_mask(self, data, light_threshold, dark_threshold):
        mask = np.copy(data)
        for row in mask:
            for pixel in row:
                lightness = self.get_pixel_lightness(pixel)
                if lightness < dark_threshold or lightness > light_threshold:
                    pixel[0] = 0
                    pixel[1] = 0
                    pixel[2] = 0
                else:
                    pixel[0] = 255
                    pixel[1] = 255
                    pixel[2] = 255
        return mask

    def get_intervals(self, mask, width, height, mode):
        intervals = []
        interval = []
        in_interval = False

        if mode == Mode.VERTICAL:
            for x in range(width):
                for y in range(height):
                    if mask[y, x][0] == 255:
                        if not in_interval:
                            interval = [Mode.VERTICAL, x, y]
                            interval.append([x, y])
                            in_interval = True
                        else:
                            interval.append([x, y])
                    else:
                        if in_interval:
                            if len(interval) > 4:
                                intervals.append(interval)
                            in_interval = False
                if in_interval:
                    if len(interval) > 4:
                        intervals.append(interval)
                    in_interval = False
                    interval = []
            return intervals

        if mode == Mode.HORIZONTAL:
            for y in range(height):
                for x in range(width):
                    if mask[y, x][0] == 255:
                        if not in_interval:
                            interval = [Mode.HORIZONTAL, x, y]
                            interval.append([x, y])
                            in_interval = True
                        else:
                            interval.append([x, y])
                    else:
                        if in_interval:
                            if len(interval) > 4:
                                intervals.append(interval)
                            in_interval = False
                if in_interval:
                    if len(interval) > 4:
                        intervals.append(interval)
                    in_interval = False
                    interval = []
            return intervals

    def quicksort(self, interval, data):
        if len(interval) <= 1:
            return interval
        pivot = interval[-1]
        interval = interval[: len(interval) - 1]
        pivot_lightness = self.get_pixel_lightness(data[pivot[1]][pivot[0]])
        smaller = [x for x in interval if self.get_pixel_lightness(data[x[1]][x[0]]) < pivot_lightness]
        larger = [x for x in interval if self.get_pixel_lightness(data[x[1]][x[0]]) >= pivot_lightness]
        return self.quicksort(smaller, data) + [pivot] + self.quicksort(larger, data)


root = tk.Tk()
root.title("Image Pixel Sorter")
root.config(bg="skyblue")

root.resizable(True, True)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)

app = App(root)
root.mainloop()
