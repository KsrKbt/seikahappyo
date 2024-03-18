import cv2
import tkinter as tk
from PIL import Image, ImageTk

# 顔を検出する関数
def detection_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        return True
    else:
        return False

# メインのGUIウィンドウを作成する関数
def create_window():
    root = tk.Tk()
    root.title("Room Map")

    # 画像を表示するラベル
    label = tk.Label(root)
    label.pack()

    # OpenCVのカメラキャプチャを開始
    cap = cv2.VideoCapture(0)

    def update():
        ret, frame = cap.read()
        if ret:
            # 顔の検出
            has_face = detection_face(frame)

            # OpenCVの画像をPIL形式に変換
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)

            # 画像をTkinterのラベルに表示するための処理
            img_tk = ImageTk.PhotoImage(image=img)
            label.img_tk = img_tk
            label.config(image=img_tk)

            # 再帰的に更新
            root.after(10, update)

    update()

    root.mainloop()

if __name__ == "__main__":
    create_window()
