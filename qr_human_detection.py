import cv2
import numpy as np

def read_qrcode(frame, qrd):
    # QRコードデコード
        retval, decoded_info, points, straight_qrcode = qrd.detectAndDecodeMulti(frame)

        if retval:
            points = points.astype(np.int32)

            for dec_inf, point in zip(decoded_info, points):
                if dec_inf == '':
                    continue

                # QRコード座標取得
                # x = point[0][0]
                # y = point[0][1]

                # QRコードデータ
                print('dec:', dec_inf)
            return dec_inf
                # frame = cv2.putText(frame, dec_inf, (x, y - 6), font, .3, (0, 0, 255), 1, cv2.LINE_AA)

                # バウンディングボックス
                # frame = cv2.polylines(frame, [point], True, (0, 255, 0), 1, cv2.LINE_AA)

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
        return
    


if __name__ == '__main__':
    font = cv2.FONT_HERSHEY_SIMPLEX
    # VideoCaptureインスタンス生成
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # QRCodeDetectorインスタンス生成
    qrd = cv2.QRCodeDetector()

    # 学習済みモデルの読み込み
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            tmp = read_qrcode(frame, qrd)
            tmp2 = detction_face(frame, cascade)
            # read_qrcodeがroom1の場合
                # detection_faceがtrueなら
                # アプリケーションに反映
            # read_qrcodeが更新されて新しくなった場合
                # 一個前の部屋には誰もいないとして判断
                # 更新された後人が検知されたらアプリケーションに反映
                 
            # 画像表示
            cv2.imshow('cv2', frame)

            # quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # キャプチャリソースリリース
    cap.release()