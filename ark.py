import time
import cv2 as cv
import os
import pyautogui
import numpy as np
from numpy.random import default_rng

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
    try: 
        hay = pyautogui.screenshot( region= (botManagement.screen.width/2 - 100, botManagement.screen.heigth/2 - 150, 200, 250) )
    except: 
        print("error while looking for needle")
        botManagement.runBot=False
    hay = cv.cvtColor(np.array(hay), cv.COLOR_RGB2BGR)
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
    time.sleep(rng.uniform(0.1, 0.2))
    press_e(rng)
    print("caught")
    time.sleep(rng.uniform(6.5, 9))
    

#functions for event listener
#not in use
def on_press(key):
    global botManagement
    print(key)
    if key == " ":
        print("stopp the bot")
        botManagement.runBot=False

def on_release(key):
    return False

def main():
    os.chdir(botManagement.dir)
    rng = default_rng()
    thrown = False
    val=0
    needle = cv.imread(botManagement.needleLoc, cv.IMREAD_COLOR)
    x=0
    

    time.sleep(3)
    
    while x>=0 and botManagement.runBot:
        if (not thrown): 
            throw_rod(rng)
            thrown=True
            x=30

        val=find_match(needle)
        time.sleep(0.5)

        if (val >= 0.8):
            get_rod(rng)
            thrown=False
            val=0

        x -=1
        
botManagement = BotManagement(Screen(2560, 1440), True, "./screenshots", "needle2.png")

if __name__ == "__main__" :
    main()