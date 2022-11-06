import pyautogui
import time
import json
from random import random
from numpy.random import normal

navigation_data = open('navigation.json', 'r')
coords = json.loads(navigation_data.read())

active_menu = 'faceMenu'
active_setting = 0
scroll_state = 'up'


def rand(upper_bound=100, lower_bound=0):
    return int(random() * upper_bound * 100) % (upper_bound - lower_bound + 1) + lower_bound


def normalRandom(mean=50, deviation=15, lower_bound=0, upper_bound=100):
    value = normal(loc=mean, scale=deviation, size=1)[0]
    if (value < lower_bound):
        return lower_bound
    if (value > upper_bound):
        return upper_bound
    return int(value)


def btnPress(button):
    pyautogui.moveTo(button['x'], button['y'], duration=0.1)
    pyautogui.click()


def btnMove(button):
    pyautogui.moveTo(button['x'], button['y'], duration=0.1)


def setColor(color):
    btnPress(coords['colorHue'])
    pyautogui.typewrite(str(color.hue))
    btnPress(coords['colorSat'])
    pyautogui.typewrite(str(color.saturation))
    btnPress(coords['colorBrig'])
    pyautogui.typewrite(str(color.value))
    btnPress(coords['colorAlpha'])
    pyautogui.typewrite(str(color.alpha))


def setActive(menu, setting, scroll_down=False):
    global active_menu
    global active_setting
    if (active_menu != menu):
        btnPress(coords[menu])
        active_menu = menu
    if (active_setting != setting):
        menuScroll('up')
        btnPress(coords['setting'][setting])
        active_setting = setting


def menuScroll(state):
    global scroll_state
    if (scroll_state == state):
        return 0
    scroll_state = state
    pyautogui.moveTo(coords['scrollbarLeft']['x'],
                     coords['scrollbarLeft']['y'], duration=0.1)
    if (state == 'down'):
        amount = -6
    elif(state == 'up'):
        amount = 6
    else:
        return None
    for i in range(6):
        pyautogui.scroll(amount // 6)
    return amount


class Color:

    def __init__(self, hue=0, saturation=0, value=0, alpha=100):
        self.hue = hue
        self.saturation = saturation
        self.value = value
        self.alpha = alpha


class ColorRGB:

    def __init__(self, red=0, green=0, blue=0, alpha=100):
        self.Red = red
        self.Green = green
        self.Blue = blue
        self.alpha = alpha

    def __iter__(self):
        for attr in self.__dict__.values():
            yield attr


class Setting:

    def __init__(self, params):
        self.Params = params
        self.setting_index = 0
        self.menu = 'faceMenu'

    def set(self, params):
        self.Params = params
        setActive(self.menu, self.setting_index)
        for i in range(min(len(params), 11)):
            btnPress(coords['parameter'][i])
            pyautogui.typewrite(str(params[i]))
        if (len(params) > 11):
            btnMove(coords['scrollbarRight'])
            pyautogui.scroll(-1)
            pyautogui.scroll(-1)
            for i in range(len(params) - 11):
                btnPress(coords['parameter'][11 - (len(params) - 11) + i])
                pyautogui.typewrite(str(params[11 + i]))
            btnMove(coords['scrollbarRight'])
            pyautogui.scroll(1)
            pyautogui.scroll(1)

    def setRandom(self):
        for i in range(len(self.Params)):
            self.Params[i] = normalRandom(self.Params[i])
        self.set(self.Params)


class FacialType(Setting):

    def __init__(self, type=5):
        self.Type = type

    def set(self, type):
        if (type < 1 or type > 5):
            return None
        self.Type = type
        setActive('faceMenu', 0)
        if (type < 4):
            btnMove(coords['slot'][0])
            pyautogui.scroll(1)
            pyautogui.scroll(1)
            btnPress(coords['slot'][type - 1])
        else:
            btnMove(coords['slot'][0])
            pyautogui.scroll(-1)
            pyautogui.scroll(-1)
            btnPress(coords['slot'][type - 4])

    def setRandom(self):
        self.Type = int(random() * 1000) % 5 + 1
        self.set(self.Type)


class Overall(Setting):

    def __init__(self, params=[41, 50, 46, 50, 35]):
        self.Params = params
        self.setting_index = 1
        self.menu = 'faceMenu'


class Jaw(Setting):

    def __init__(self, params=[42, 40, 60, 37, 80, 30, 55, 50]):
        self.Params = params
        self.setting_index = 2
        self.menu = 'faceMenu'


class Cheeks(Setting):

    def __init__(self, params=[56, 69, 20, 41, 41, 36]):
        self.Params = params
        self.setting_index = 3
        self.menu = 'faceMenu'


class Eyebrows(Setting):

    def __init__(self, params=[50, 50, 50, 41, 50]):
        self.Params = params
        self.setting_index = 4
        self.menu = 'faceMenu'


class Eye(Setting):

    def __init__(self, params=[50, 45, 50, 43, 41, 50, 46, 44, 44, 50, 50, 50, 50]):
        self.Params = params
        self.setting_index = 5
        self.menu = 'faceMenu'


class Nose(Setting):

    def __init__(self, params=[55, 55, 56, 45, 48, 58, 20, 52, 60, 44, 51, 50, 49, 49, 37]):
        self.Params = params
        self.setting_index = 6
        self.menu = 'faceMenu'


class Mouth(Setting):

    def __init__(self, params=[65, 50, 51, 57, 48, 41, 48]):
        self.Params = params
        self.setting_index = 7
        self.menu = 'faceMenu'


class Ears(Setting):

    def __init__(self, params=[35, 50, 50, 50, 50]):
        self.Params = params
        self.setting_index = 8
        self.menu = 'faceMenu'


class Moles(Setting):

    def __init__(self, type=0, color=Color(0, 0, 0), arrange=1, params=[0, 0, 0, 0]):
        self.Type = type
        self.Color = color
        self.Arrange = arrange
        self.Params = params
        self.setting_index = 9
        self.menu = 'faceMenu'

    def set(self, type, color, arrange, params):
        self.Type = type
        self.Color = color
        self.Arrange = arrange
        self.Params = params
        setActive(self.menu, self.setting_index)
        btnPress(coords['tab'][0])
        btnPress(coords['slot'][type])
        if (type):
            btnPress(coords['tab'][1])
            btnPress(coords['parameter'][1])
            setColor(color)
        if (type < 3):
            btnPress(coords['tab'][2])
            if (arrange > 6):
                btnMove(coords['scrollbarRight'])
                pyautogui.scroll(-1)
                btnPress(coords['slot'][arrange - 4])
                btnMove(coords['scrollbarRight'])
                pyautogui.scroll(1)
            else:
                btnPress(coords['slot'][arrange - 1])
            for i in range(4):
                btnPress(coords['parameter'][i + 7])
                pyautogui.typewrite(str(params[i]))

    def setRandom(self):
        self.Type = int(random() * 100) % 6
        self.Type = 2
        print(f"type: {self.Type}")
        hue = normalRandom(0, 15, 0, 360)
        saturation = normalRandom(50, 15)
        value = normalRandom(20, 20)
        alpha = normalRandom(55, 15)
        self.Color = Color(hue, saturation, value, alpha)
        self.Arrange = int(random() * 100) % 8 + 1
        self.Params[0] = normalRandom(25, 10)
        self.Params[1] = normalRandom(25, 10)
        self.Params[2] = normalRandom(70, 20)
        self.Params[3] = normalRandom(50, 15)
        self.set(self.Type, self.Color, self.Arrange, self.Params)


class Face:

    def __init__(self):
        self.FacialType = FacialType()
        self.Overall = Overall()
        self.Jaw = Jaw()
        self.Cheeks = Cheeks()
        self.Eyebrows = Eyebrows()
        self.Eye = Eye()
        self.Nose = Nose()
        self.Mouth = Mouth()
        self.Ears = Ears()
        self.Moles = Moles()

    def randomize(self):
        self.FacialType.setRandom()
        self.Overall.setRandom()
        self.Jaw.setRandom()
        self.Cheeks.setRandom()
        self.Eyebrows.setRandom()
        self.Eye.setRandom()
        self.Nose.setRandom()
        self.Mouth.setRandom()
        self.Ears.setRandom()
        self.Moles.setRandom()
