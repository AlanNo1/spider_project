import pytesseract
from urllib import request
from PIL import Image
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata"'

while True:
    url = "https://passport.lagou.com/vcode/create?from=register&refresh=1513081451891"
    request.urlretrieve(url, 'captcha.png')
    image = Image.open('captcha.png')
    text = pytesseract.image_to_string(image, lang='eng', config=tessdata_dir_config)
    print(text)
    time.sleep(2)
