import tkinter as tk
from PIL import Image, ImageTk
import random
import sys
import os

MAP_WIDTH = 768
MAP_HEIGHT = 372
ORIGINAL_AREA_CENTERS = [
    (342, 105),
    (342, 135),
    (342, 165),
    (342, 195),
    (342, 225),
    (342, 255)
]
MARK_FILES = ["yellow.png", "green.png", "red.png", "white.png"]
MARGIN_RATIO_X = 0.06
MARGIN_RATIO_Y = 0.08
DEFAULT_BG = "#F0F0F0"

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

class ResizableLotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WRO2025 RoboMission Junior Randomization")
        self.root.configure(bg=DEFAULT_BG)

        # ここでimgフォルダ配下として指定
        self.map_img_pil = Image.open(resource_path("img/Junior_map.png"))
        self.mark_imgs_pil = [Image.open(resource_path(f"img/{fname}")) for fname in MARK_FILES]

        self.frame = tk.Frame(root, bg=DEFAULT_BG)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label_title = tk.Label(
            self.frame,
            text="WRO2025 RoboMission Junior Randomization",
            bg=DEFAULT_BG,
            font=("Arial", 1),
            justify="center"
        )
        self.label_title.pack(pady=10)

        self.canvas = tk.Canvas(self.frame, bg=DEFAULT_BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.button_draw = tk.Button(
            self.frame,
            text="Click!",
            command=self.display_random_images,
            bg=DEFAULT_BG,
            font=("Arial", 1)
        )
        self.button_draw.pack(pady=(20, 40))

        self.bg_img = None
        self.mark_img_refs = []
        self.chosen_indices = None
        self.chosen_marks = None

        self._resize_after_id = None
        self._initialized = False

        self.frame.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Configure>", self.on_resize)

        self.root.after(500, self._initial_draw)

    def _initial_draw(self):
        self._initialized = True
        self.redraw_canvas()

    def get_map_bbox(self, w, h):
        margin_x = int(w * MARGIN_RATIO_X)
        margin_y = int(h * MARGIN_RATIO_Y)
        avail_w = max(w - 2*margin_x, 1)
        avail_h = max(h - 2*margin_y, 1)
        scale = min(avail_w / MAP_WIDTH, avail_h / MAP_HEIGHT)
        draw_w = int(MAP_WIDTH * scale)
        draw_h = int(MAP_HEIGHT * scale)
        left = (w - draw_w) // 2
        top = (h - draw_h) // 2
        return left, top, left + draw_w, top + draw_h, scale

    def get_scaled_positions(self, left, top, scale):
        return [(int(left + x*scale), int(top + y*scale)) for x, y in ORIGINAL_AREA_CENTERS]

    def calc_font_sizes(self, w, h):
        base = min(w, h)
        title_size = max(int(base * 0.05), 14)
        button_size = max(int(base * 0.035), 11)
        button_pad_y_top = int(h * 0.02)
        button_pad_y_bottom = int(h * 0.06)
        return title_size, button_size, button_pad_y_top, button_pad_y_bottom

    def redraw_canvas(self, event=None):
        w = self.frame.winfo_width()
        h = self.frame.winfo_height()
        if w < 100 or h < 100:
            self.root.after(50, self.redraw_canvas)
            return

        title_size, button_size, pad_y_top, pad_y_bottom = self.calc_font_sizes(w, h)
        self.label_title.config(
            font=("Arial", title_size),
            fg="black"
        )
        self.button_draw.config(
            font=("Arial", button_size),
            fg="black",
            bg=DEFAULT_BG,
            padx=button_size,
            pady=button_size // 2
        )
        self.button_draw.pack_configure(pady=(pad_y_top, pad_y_bottom))

        self.canvas.config(width=w, height=int(h * 0.7))
        c_w = self.canvas.winfo_width()
        c_h = self.canvas.winfo_height()
        left, top, right, bottom, scale = self.get_map_bbox(c_w, c_h)
        self.canvas.delete("all")
        map_img = self.map_img_pil.resize((right-left, bottom-top), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(map_img)
        self.canvas.create_image(left, top, anchor=tk.NW, image=self.bg_img)

        self.mark_img_refs = []
        mark_size = max(int(32 * scale), 10)
        if self.chosen_indices and self.chosen_marks:
            positions = self.get_scaled_positions(left, top, scale)
            for idx, mark_idx in zip(self.chosen_indices, self.chosen_marks):
                resized_img = ImageTk.PhotoImage(self.mark_imgs_pil[mark_idx].resize((mark_size, mark_size), Image.Resampling.LANCZOS))
                self.canvas.create_image(*positions[idx], image=resized_img)
                self.mark_img_refs.append(resized_img)

    def display_random_images(self):
        c_w = self.canvas.winfo_width()
        c_h = self.canvas.winfo_height()
        left, top, right, bottom, scale = self.get_map_bbox(c_w, c_h)
        selected = random.sample(range(len(ORIGINAL_AREA_CENTERS)), 4)
        marks = list(range(4))
        random.shuffle(marks)
        self.chosen_indices = selected
        self.chosen_marks = marks
        self.redraw_canvas()

    def on_resize(self, event):
        if not self._initialized:
            return
        if self._resize_after_id:
            self.root.after_cancel(self._resize_after_id)
        self._resize_after_id = self.root.after(200, self._resize_end)

    def _resize_end(self):
        self._resize_after_id = None
        self.redraw_canvas()

if __name__ == "__main__":
    root = tk.Tk()

    screen_w = int(root.winfo_screenwidth()*0.8)
    screen_h = int(root.winfo_screenheight()*0.8)
    root.geometry(f"{screen_w}x{screen_h}+0+0")
    root.resizable(True, True)

    app = ResizableLotteryApp(root)
    root.mainloop()
