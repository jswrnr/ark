import time
import cv2 as cv
import os
import pyautogui
import pygetwindow
import numpy as np
from numpy.random import default_rng
from pynput import keyboard

class Screen:
    width : int
    heigth : int
    def __init__(self, width, heigth) -> None:
        self.width = width
        self.heigth = heigth

class BotManagement:
    screen : Screen
    runBot : bool
    dir : str
    needleLoc : str
    def __init__(self, screen, runBot, dir, needleLoc) -> None:
        self.screen = screen
        self.runBot = runBot
        self.dir = dir
        self.needleLoc = needleLoc

#returns the value of best match between needle and hay
def find_match(needle): 
    #take screenshot and change into cv2 format
    hay = pyautogui.screenshot( region= (botManagement.screen.width/2 - 150, botManagement.screen.heigth/2 - 100, 200, 200) )
    hay = cv.cvtColor(np.array(hay), cv.COLOR_RGB2BGR)
    #cv.IMREAD_COLOR to load png without alpha
    #needle = cv.imread("needle2.png", cv.IMREAD_COLOR)
    result = cv.matchTemplate(hay, needle, cv.TM_CCOEFF_NORMED)

    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)
    return maxVal

#help function for game interaction
def press_e(rng): 
    pyautogui.keyDown("e")
    time.sleep(rng.uniform(0.05, 1))
    pyautogui.keyUp("e")

#functions for game interaction
def throw_rod(rng):
    press_e(rng)
    print("thrown")
    time.sleep(3)
    

def get_rod(rng):
    time.sleep(rng.normal(0.2, 0.05))
    press_e(rng)
    print("caught")
    time.sleep(rng.uniform(6.5, 9))
    

#functions for event listener
def on_press(key):
    global botManagement
    print(key)
    if key == keyboard.Key.f1:
        print("stopp the bot")
        botManagement.runBot=False

def on_release(key):
    if key == keyboard.Key.f1:
        return False

def main():
    os.chdir(botManagement.dir)
    rng = default_rng()
    thrown = False
    val=0
    needle = cv.imread(botManagement.needleLoc, cv.IMREAD_COLOR)
    x=100
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    time.sleep(3)
    
    while x>0 and botManagement.runBot:
        if (not thrown): 
            throw_rod(rng)
            thrown=True
            x=100

        val=find_match(needle)
        time.sleep(0.8)

        if (val >= 0.8):
            get_rod(rng)
            thrown=False
            val=0

        x -=1
        
botManagement = BotManagement(Screen(2560, 1440), True, "C:/Users/JonathanW/Projects/VScode/Python/Ark/screenshots", "needle2.png")

if __name__ == "__main__" :
    main()