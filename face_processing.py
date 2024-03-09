import cv2

# 学習済みモデルの読み込み
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# カメラ映像からVideoCaptureオブジェクトを取得
cap = cv2.VideoCapture(0)
# カメラに問題がないかの確認
if not cap.isOpened():
    print("カメラが正常ではありません")
    exit()
# カメラから連続的にキャプチャ画像を取得
while True:
    # Bool値とキャプチャ画像を変数に格納
    ret, frame = cap.read()
    # キャプチャ画像が正しく読み込めたかの確認
    if not ret:
        print("画像を正しく読み込めませんでした")
        break
    # 画像データをグレースケール化（白黒）
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 顔を検出する
    lists = cascade.detectMultiScale(frame_gray, minSize=(50, 50))
    # forですべての顔を赤い長方形で囲む
    for (x,y,w,h) in lists:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), thickness=2)
    # 顔認識を行っている画像を表示
    cv2.imshow('video image', frame)
    # qが押されたらwhileから抜ける
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
