import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import random

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 抽選用の画像サイズ
IMAGE_SIZE = (20, 20)

# 中央の6つのエリアの座標（相対座標: 画像の左上を(0, 0)とする）
relative_areas = [
    (330, 95),
    (330, 125),
    (330, 155),
    (330, 185),
    (330, 215),
    (330, 245)
]

def display_random_images():
    """ランダムに4つのエリアに抽選用画像を配置"""
    # 既存の抽選画像を削除
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and widget != label_map and widget != label_title:
            widget.destroy()

    # Junior_map のサイズ取得
    map_width = label_map.winfo_width()
    map_height = label_map.winfo_height()

    # Junior_map の座標
    map_x = label_map.winfo_x()
    map_y = label_map.winfo_y()

    # 画像サイズに基づき座標をスケーリング
    scaled_areas = [
        (map_x + int(x / 768 * map_width), map_y + int(y / 372 * map_height))
        for x, y in relative_areas
    ]

    # ランダムにエリアと画像を選択して配置
    selected_areas = random.sample(scaled_areas, 4)
    images = [yellow_img, green_img, red_img, white_img]
    random.shuffle(images)

    for area, img in zip(selected_areas, images):
        x, y = area
        label = tk.Label(root, image=img, bg="white")
        label.image = img  # 参照を保持
        label.place(x=x, y=y)

# ウィンドウの作成
root = tk.Tk()
root.title("WRO2025 RoboMission Junior 抽選")
root.geometry("1024x600")
root.state("zoomed")

# 上部のタイトルラベル
label_title = tk.Label(root, text="WRO2025 RoboMission Junior 抽選", font=("Meiryo", 24))
label_title.pack(pady=30)

# Junior_mapの表示
map_image = Image.open(resource_path("Junior_map.png")).resize((768, 372), Image.Resampling.LANCZOS)
map_photo = ImageTk.PhotoImage(map_image)

label_map = tk.Label(root, image=map_photo)
label_map.pack(pady=0)

# 抽選用の画像の読み込み
yellow_img = ImageTk.PhotoImage(Image.open(resource_path("yellow.png")).resize(IMAGE_SIZE))
green_img = ImageTk.PhotoImage(Image.open(resource_path("green.png")).resize(IMAGE_SIZE))
red_img = ImageTk.PhotoImage(Image.open(resource_path("red.png")).resize(IMAGE_SIZE))
white_img = ImageTk.PhotoImage(Image.open(resource_path("white.png")).resize(IMAGE_SIZE))

# 抽選ボタン
button_draw = tk.Button(root, text=" 抽選！ ", font=("Meiryo", 24), command=display_random_images)
button_draw.pack(pady=20)

# メインループ
root.mainloop()
