import cv2
import numpy as np
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import threading
from threading import Lock
import queue
import random

room_name = ""
dfResult = False
# 顔検知回数
count = 0
# QRコード読み取り
def read_qrcode(frame, qrd):
    # QRコードデコード
        retval, decoded_info, points, straight_qrcode = qrd.detectAndDecodeMulti(frame)

        if retval:
            points = points.astype(np.int32)
            for dec_inf, point in zip(decoded_info, points):
                if dec_inf == '':
                    return dec_inf
                else:
                    return dec_inf
                # QRコード座標取得
                # x = point[0][0]
                # y = point[0][1]

                # QRコードデータ
                #print('dec:', dec_inf)
                # frame = cv2.putText(frame, dec_inf, (x, y - 6), font, .3, (0, 0, 255), 1, cv2.LINE_AA)

                # バウンディングボックス
                # frame = cv2.polylines(frame, [point], True, (0, 255, 0), 1, cv2.LINE_AA)

# 顔検知
def detction_face(frame, cascade):
    # 画像データをグレースケール化（白黒）
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 顔を検出する
    lists = cascade.detectMultiScale(frame_gray, minSize=(50, 50))
    # 顔が検出された場合の処理
    if len(lists) > 0:
        for (x, y, w, h) in lists:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), thickness=2)
        return True
    # 顔が検出されなかった場合の処理
    else:
        return False

# カメラ映像表示
def cam_view():
    global room_name, dfResult, count
    lock = Lock()
    # VideoCaptureインスタンス生成
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # QRCodeDetectorインスタンス生成
    qrd = cv2.QRCodeDetector()

    # 学習済みモデルの読み込み
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            with lock:
                # QRコードが表す文字列
                room_name = read_qrcode(frame, qrd)
                # 顔が検出されたか否か
                dfResult = detction_face(frame, cascade)
                if dfResult:
                    count = count + 1

            # OpenCVの画像をPIL形式に変換
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            # 画像表示
            cv2.imshow('cv2', frame)

            # quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # キャプチャリソースリリース
    cap.release()



# 部屋マップ表示
def create_window():
    # グローバル変数のロック用
    lock = Lock()
    prevRoomName = ''
    # 部屋の在室確認を何回したか
    flag = 0
    # 在室と判断したときに加算
    flag2 = 0
    # 不在と判断したときに加算
    flag3 = 0
    # 在室状況更新
    def update_room(prevRoomName, flag, flag2, flag3):
        global room_name, dfResult, count
        # 在室確認する部屋が更新された場合
        if room_name is not None:
            prevRoomName = room_name
            print(prevRoomName)
            flag = 0
            flag2 = 0
            flag3 = 0
        # 顔検知が誤ったものでないかの指標となる閾値
        # 一秒間に何回顔検知されたか
        threshold = 5
        # countが閾値よりも大きい場合（誤検知ではなさそうな場合）
        if threshold < count:
            if flag != 8:
                # 在室確認が取れた
                flag2 += 1
                flag += 1
        # 誤検知、もしくは検知できなかった場合
        else:
            if flag != 8:
                # 不在と判断した場合
                flag3 += 1
                flag += 1

        if flag == 8:
            if flag2 > flag3:
                if prevRoomName == "room1":
                    canvas.itemconfig(circle, fill="green")
                elif prevRoomName == "room2":
                    canvas.itemconfig(circle2, fill="green")
                elif prevRoomName == "room3":
                    canvas.itemconfig(circle3, fill="green")
            else:
                if prevRoomName == "room1":
                    canvas.itemconfig(circle, fill="red")
                elif prevRoomName == "room2":
                    canvas.itemconfig(circle2, fill="red")
                elif prevRoomName == "room3":
                    canvas.itemconfig(circle3, fill="red")

        with lock:
            room_name = ""
            count = 0
        root.after(1000, lambda: update_room(prevRoomName, flag, flag2, flag3))
    # 画面作成
    root = tk.Tk()
    root.geometry("700x554")
    root.title("room_map")
    # キャンバス作成
    canvas = tk.Canvas(root, bg="#deb887", height=554, width=700)
    # キャンバス表示
    canvas.place(x=0, y=0)
 
    # イメージ作成
    img = tk.PhotoImage(file="room.png", width=700, height=554)
    # キャンバスにイメージを表示
    canvas.create_image(0, 0, image=img, anchor=tk.NW)
    # テキスト表示処理
    custom_font = font.Font(family="Helvetica", size=20)  # Helveticaフォント、サイズ20
    text_label = tk.Label(root, text="赤は不在、緑は在室", bg="#deb887", font=custom_font)  # テキストと背景色を指定
    text_label.place(x=10, y=10)  # テキストの位置を指定

    # 在室マークの初期化
    # 円の初期位置と色
    circle_x = 150
    circle_y = 140
    circle_radius = 20
    circle_color = "red"

    # 初期の円を描画
    circle = canvas.create_oval(circle_x - circle_radius, circle_y - circle_radius, circle_x + circle_radius, circle_y + circle_radius, fill=circle_color)
    circle2 = canvas.create_oval(360 - circle_radius, circle_y - circle_radius, 360 + circle_radius, circle_y + circle_radius, fill=circle_color)
    circle3 = canvas.create_oval(560 - circle_radius, circle_y - circle_radius, 560 + circle_radius, circle_y + circle_radius, fill=circle_color)
    update_room(prevRoomName, flag, flag2, flag3)
    root.mainloop()

    




def main():
    cam_thread = threading.Thread(target=cam_view)
    room_thread = threading.Thread(target=create_window)
    cam_thread.start()
    room_thread.start()
    

if __name__ == '__main__':
    main()