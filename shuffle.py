import time
import generate
import pyautogui
import msvcrt as msv
import keyboard
from modify import loadCard

print("Switch to the game window and press Q to generate a new character.\nPress E to stop this script.")

while True:
    if keyboard.is_pressed("q"):
        generate.randomFace()
        time.sleep(0.2)
        loadCard()
        time.sleep(1)
    elif keyboard.is_pressed("e"):
        print("Finished.")
        break
