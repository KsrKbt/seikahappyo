import pyqrcode

FILE_PNG_A = 'qrcode_A.png'
FILE_PNG_B = 'qrcode_B.png'
FILE_PNG_C = 'qrcode_C.png'

# QRコード作成
# code = pyqrcode.create('https://qiita.com/PoodleMaster', error='L', version=3, mode='binary')
#code.png(FILE_PNG_A, scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])

# QRコード作成
#code = pyqrcode.create('https://github.com/PoodleMaster', error='L', version=3, mode='binary')
#code.png(FILE_PNG_B, scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])

# QRコードに埋め込む文字列
encoded_text = "room1"
# QRコードを生成
code = pyqrcode.create(encoded_text)
code.png(FILE_PNG_A, scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])

# QRコードに埋め込む文字列
encoded_text = "room2"
# QRコードを生成
code = pyqrcode.create(encoded_text)
code.png(FILE_PNG_B, scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])

# QRコードに埋め込む文字列
encoded_text = "room3"
# QRコードを生成
code = pyqrcode.create(encoded_text)
code.png(FILE_PNG_C, scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])