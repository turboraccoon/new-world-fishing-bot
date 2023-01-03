import mss
import pyautogui
from PIL import Image
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import gc
import time
import random

mouse = MouseController()
keyboard = KeyboardController()


def main():
    # Load needle images.
    fishIcon = Image.open('imgs/fishIcon.png')
    holdCast = Image.open('imgs/holdCast.png')
    fishReeling = Image.open('imgs/fishReeling.png')
    fishReelingOrange = Image.open('imgs/fishReelingOrange.png')

    fishIcon.load()
    holdCast.load()
    fishReeling.load()
    fishReelingOrange.load()

    # Max cast is 2 seconds.
    castingBaseTime = 2
    castingTimeRandom = .05

    # Find all windows with the title "New World".
    newWorldWindows = pyautogui.getWindowsWithTitle('New World')

    # Find the window titled exactly "New World".
    for window in newWorldWindows:
        if window.title == 'New World':
            newWorldWindow = window
            break

    # Activate the game window.
    newWorldWindow.activate()

    # Move your mouse to the center of the game window.
    pyautogui.moveTo(
        newWorldWindow.left + (newWorldWindow.width / 2),
        newWorldWindow.top + (newWorldWindow.height / 2)
    )

    # Selecting the middle 3rd of the New World window.
    mssRegion = {
        'mon': 1,
        'top': newWorldWindow.top,
        'left': newWorldWindow.left + round(newWorldWindow.width / 3),
        'width': round(newWorldWindow.width / 3),
        'height': newWorldWindow.height
    }

    # Create an instance of the screenshotter.
    sct = mss.mss()

    def grabScreenshot():
        if random.random() > .6:
            gc.collect()

        screenshot = sct.grab(mssRegion)

        return Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')

    # You have one second to prepare.
    time.sleep(1)

    while True:
        print('Holding "free book" button')
        keyboard.press(Key.alt)

        print('Casting line...')
        mouse.press(Button.left)
        time.sleep(castingBaseTime + (castingTimeRandom * random.random()))
        mouse.release(Button.left)

        time.sleep(1)

        # Looking for the fish icon
        while True:
            sctImg = grabScreenshot()

            if pyautogui.locate(fishIcon, sctImg, grayscale=True, confidence=.7):
                break

            time.sleep(.1)

        # Hooking the fish
        print('Fish hooked')
        mouse.click(Button.left)

        pressed = False

        # Keeps reeling into "HOLD Cast" text shows on screen.
        while pyautogui.locate(holdCast, sctImg, grayscale=True, confidence=.6, limit=1) is None:
            sctImg = grabScreenshot()

            # Locating the needle image in the color mode seems to be more reliable and removes "jerky" reeling.
            if not pressed and pyautogui.locate(fishReeling, sctImg, grayscale=False, confidence=.75, limit=1):
                print('Reeling...')
                mouse.press(Button.left)
                pressed = True
                time.sleep(.2)

            elif pressed and pyautogui.locate(fishReelingOrange, sctImg, grayscale=False, confidence=.75, limit=1):
                print('Slacking...')
                mouse.release(Button.left)
                pressed = False
                time.sleep(.2)

            else:
                time.sleep(.1)

        mouse.release(Button.left)
        print('Caught fish')

        # Release the "Free Look" button.
        print('Release "free look" button')
        keyboard.release(Key.alt)

        # Move from side to side to reset AFK cooldown.
        if random.random() > .5:
            keyboard.press('a')
            time.sleep(.2)
            keyboard.release('a')
            time.sleep(.2)
            keyboard.press('d')
            time.sleep(.2)
            keyboard.release('d')
            time.sleep(.2)

        else:
            time.sleep(.2)

        gc.collect()


# Runs the main function.
if __name__ == '__main__':
    main()
