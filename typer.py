import pyscreenshot
import pytesseract
import time
import numpy as np
from pyautogui import press
from PIL import Image

DEBUG = False
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\carso\AppData\Local\Tesseract-OCR\tesseract.exe"

class Typer:
    def __init__(self, box=(548,806,591,906)):
        self.box = box
        self.text = None

    def screenshot(self):
        im = pyscreenshot.grab(bbox=self.box)
        im.save('screenshot.png')
        if DEBUG:
            im.show()
    
    def recognize_text(self):
        text = pytesseract.image_to_string(Image.open('screenshot.png'))
        if text is not "":
            print(text)
            print(text[0])
            self.text = text[0]
        else:
            self.text = " "
            print(" ")

    def send_keystroke(self):
        press(self.text)

def master():
    type_bot = Typer()

    while (True):
        type_bot.screenshot()
        type_bot.recognize_text()
        type_bot.send_keystroke()
        #wait_time = np.random.normal(loc=0.1,scale=0.01)
        #time.sleep(abs(wait_time))

if __name__ == '__main__':
    master()