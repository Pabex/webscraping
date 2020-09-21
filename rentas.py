import webbrowser
import pyautogui
import time
import pyscreenshot as ImageGrab
import random
import os


cuits = ["33537186009", "30583137943"]

x_txt, y_txt = 1768, 183

x1_check, x2_check = 1730, 1750
y1_check, y2_check = 232, 254

x1_txt, x2_txt = 1713, 2020
y1_txt, y2_txt = 164, 197

x1_btn, x2_btn = 1716, 1800
y1_btn, y2_btn = 296, 326


def get_point_inner_check():
    x = random.randint(x1_check, x2_check)
    y = random.randint(y1_check, y2_check)
    return x, y


def get_point_inner_txt():
    x = random.randint(x1_txt, x2_txt)
    y = random.randint(y1_txt, y2_txt)
    return x, y


def get_point_inner_button():
    x = random.randint(x1_btn, x2_btn)
    y = random.randint(y1_btn, y2_btn)
    return x, y


def make_screenshot(name):
    img = ImageGrab.grab(bbox=(1368, 38, 2725, 766))
    img.save("./rentas/%s.png" % name)


def cuit(cuit):
    os.system("brave https://www.rentascordoba.gob.ar/mirentas/rentas.html?page=situacionfiscal &")
    time.sleep(5)
    #x, y = get_point_inner_txt()
    #pyautogui.moveTo(x, y, duration=3, tween=pyautogui.easeInElastic)
    #time.sleep(0.8)
    #pyautogui.click()
    #time.sleep(1)
    pyautogui.write(cuit, interval=0.15)
    time.sleep(1)
    x, y = get_point_inner_check()
    pyautogui.click(x, y, clicks=1, duration=3, tween=pyautogui.easeInOutCirc)
    time.sleep(3.5)
    x, y = get_point_inner_button()
    pyautogui.click(x, y, clicks=1, duration=0.1, tween=pyautogui.easeInOutCirc)
    time.sleep(3)
    make_screenshot(cuit)


for c in cuits:
    cuit(c)
    time.sleep(1)
