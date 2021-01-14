from glob import glob
import time
import cv2
from mouse import click
import mss
import numpy
from global_hotkeys import *
from matplotlib import pyplot as plt
import keyboard
import random
import mouse
import pytesseract

from win32gui import GetWindowText, GetForegroundWindow

class Button:
    title = ''
    pp = ''
    effect = ''
    type = ''
    x = 0
    y = 0
    w = 0
    h = 0
    fullText = ''

    def __init__(self,x,y,w,h,title,pp,effect,type,fullText):
      self.x = x
      self.y = y
      self.w = w
      self.h = h
      self.title = title
      self.effect = effect
      self.pp = pp
      self.type = type
      self.fullText = fullText

    def click(self):
        mouse.move(self.x + 15, self.y + 15)
        mouse.click()

def getScreenshot():
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        img = cv2.cvtColor(numpy.array(sct.grab(monitor)), cv2.COLOR_BGR2GRAY)
        cv2.imwrite('C:\\pokemon\\res.png', img)
        return img

def matchImgArea(img, templatePath, x,y,w,h, threshold):
    crop = img[y:y+h, x:x+w]
    res = cv2.matchTemplate(crop, cv2.cvtColor(cv2.imread(templatePath), cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
    return numpy.any(res >= threshold),crop

def isBattle(img):
    res = matchImgArea(img, "C:\\pokemon\\img\\templateBK.png", 1332, 522, 298, 94, 0.8)
    return res[0]

def transform():
    img_rgb = cv2.imread("C:\\pokemon\\ss.png")
    cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('C:\\pokemon\\ss.png', img_rgb)

def isClientOpen(img):
    res = matchImgArea(img, "C:\\pokemon\\img\\clientBase.png", 0, 0, 100, 30, 0.8)
    return res[0]

def getButton(img,x,y,w,h):
    btn = img[y:y+h, x:x+w]

    px = 0
    py = 0
    pw = 147
    ph = 22
    title = ocrImage(btn[py:py+ph, px:px+pw])

    px = 6
    py = 24
    pw = 104
    ph = 16
    eff = ocrImage(btn[py:py+ph, px:px+pw])

    px = 119
    py = 23
    pw = 82
    ph = 20
    pp = ocrImage(btn[py:py+ph, px:px+pw])

    px = 148
    py = 6
    pw = 51
    ph = 16
    type = ocrImage(btn[py:py+ph, px:px+pw])

    fullText = ocrImage(btn)

    return Button(x,y,w,h,title,pp,eff,type,fullText)



def ocrImage(img):
    text = pytesseract.image_to_string(img)
    return text

def getButtons(img):

    oBtn1 = getButton(img, 297,680,202,46)
    oBtn2 = getButton(img, 297,734,202,46)
    oBtn3 = getButton(img, 508,680,202,46)
    oBtn4 = getButton(img, 508,734,202,46)

    return oBtn1,oBtn2,oBtn3,oBtn4


def doWork(img):
    if isBattle(img):
        buttons = getButtons(img)
        if ("fight" in buttons[0].fullText.lower()):
            buttons[0].click()
        else:
            for btn in buttons:
                if ('surf' in btn.title.lower()):
                    print("Using Surf.")
                    btn.click()
                pass
    else:
        global steps
        steps += 1
        print("Not in battle, wandering around")
        if (steps % 2 == 0):
            keyboard.send('a', True, False)
            time.sleep(0.8)
            keyboard.release('a')
        else:
            keyboard.send('d', True, False)
            time.sleep(0.8)
            keyboard.release('d')

def turnOff():
    global is_alive
    is_alive = False

#Program start
is_alive = True
bindings = [
    [["control", "shift", "7"], None, turnOff],
    [["control", "shift", "8"], None, transform],
]

# Register all of our keybindings
register_hotkeys(bindings)

# Finally, start listening for keypresses
start_checking_hotkeys()
steps = 0
while True:
    time.sleep(0.01)
    img = getScreenshot()
    if (isClientOpen(img)):
        doWork(img)
    else:
        print("Client not focused or closed.")