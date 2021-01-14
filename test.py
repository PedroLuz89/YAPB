import time
import cv2
import mss
import numpy
from global_hotkeys import *

is_alive = True

def exit_application():
    global is_alive
    stop_checking_hotkeys()
    is_alive = False

def print_world():
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        last_time = time.time()
        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        cv2.imwrite("C:\\pokemon\\testimg.png", img)
        time.sleep(10)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        print("fps: {}".format(1 / (time.time() - last_time)))

def get_squares():
    from matplotlib import pyplot as plt

    img_rgb = cv2.imread("C:\\pokemon\\testimg.png")
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("C:\\pokemon\\img\\p3.png")
    img_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[1], template.shape[0]
    res = cv2.matchTemplate(img_rgb,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.4
    loc = numpy.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        # cv2.rectangle(img_rgb, pt, (pt[0] + (w*2), pt[1] + h), (0,0,255), 2)
        # cv2.rectangle(img_rgb, pt, (pt[0] + (w//2), pt[1] + (h*2)), (0,0,255), 2)
        # cv2.rectangle(img_rgb, pt, (pt[0] + (w//2), pt[1] + (h*2)), (0,0,255), 2)
    cv2.imwrite('C:\\pokemon\\res.png',img_rgb)
        
bindings = [
    [["control", "shift", "7"], None, print_world],
    [["control", "shift", "9"], None, get_squares],
]

# Register all of our keybindings
register_hotkeys(bindings)

# Finally, start listening for keypresses
start_checking_hotkeys()

while is_alive:
    time.sleep(0.1)