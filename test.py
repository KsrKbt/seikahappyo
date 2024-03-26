import tkinter as tk
import random

def change_shape_color():
    # ランダムな色を生成
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    # 図形の色を変更
    canvas.itemconfig(rectangle, fill=color)
    canvas.itemconfig(circle, fill=color)

# Tkinterウィンドウを作成
root = tk.Tk()
root.title("Shape Color Changer")

# キャンバスを作成
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# 図形を描画
rectangle = canvas.create_rectangle(50, 50, 150, 150, fill="blue")
circle = canvas.create_oval(200, 50, 250, 150, fill="red")

# ボタンを作成して関数を呼び出す
change_color_button = tk.Button(root, text="Change Color", command=change_shape_color)
change_color_button.pack()

root.mainloop()
