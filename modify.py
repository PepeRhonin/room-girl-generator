import decoder
import random
import shutil
import json
from automation import ColorRGB, normalRandom, rand
import pyautogui
import time
import copy

default_values = json.loads(open("default.values", 'r').read())
_values = json.loads(open("cheat.sheet", 'r').read())

load_button = None


def loadCard():
    global load_button
    if (load_button == None):
        load_button = pyautogui.locateOnScreen('src/load_btn.png')
    if (load_button == None):
        print('Please switch to the game window and open the "Load" menu.')
        return False
    X, Y, width, height = load_button
    pyautogui.moveTo(X + width // 2, Y + height // 2, duration=0.1)
    pyautogui.click()
    return True


def randomRGB(mean_red=127, mean_green=127, mean_blue=127, mean_alpha=100, deviation=25, opaque=False):
    deviation255 = int(deviation * 50 / 127)
    red = normalRandom(mean_red, deviation255, 0, 255)
    green = normalRandom(mean_green, deviation255, 0, 255)
    blue = normalRandom(mean_blue, deviation255, 0, 255)
    alpha = 100 if opaque else normalRandom(mean_alpha, deviation)
    return ColorRGB(red, green, blue, alpha)


def HSVtoRGB(H, S, V, alpha=100):
    S /= 100
    V /= 100
    C = V * S
    X = C * (1 - abs((H / 60) % 2 - 1))
    m = V - C
    if (H < 60):
        R_, G_, B_ = (C, X, 0)
    elif (H < 120):
        R_, G_, B_ = (X, C, 0)
    elif (H < 180):
        R_, G_, B_ = (0, C, X)
    elif (H < 240):
        R_, G_, B_ = (0, X, C)
    elif (H < 300):
        R_, G_, B_ = (X, 0, C)
    else:
        R_, G_, B_ = (C, 0, X)
    R, G, B = (int((R_ + m) * 255), int((G_ + m) * 255), int((B_ + m) * 255))
    return ColorRGB(R, G, B, alpha)


class ColorHSV():

    def __init__(self, hue=0, saturation=0, value=0, alpha=100):
        self.hue = hue
        self.saturation = saturation
        self.value = value
        self.alpha = alpha

    def toRGB(self):
        return HSVtoRGB(self.hue, self.saturation, self.value, self.alpha)

    def __iter__(self):
        for attr in self.__dict__.values():
            yield attr


def writeNumericValue(data, index, value):
    keys = _values[str(value)].split(', ')
    for i in range(4):
        data[index + i + 1] = int(keys[i])


def writeNumericValue256(data, index, value):
    keys = decoder.WeirdChamp(value)
    for i in range(4):
        data[index + i + 1] = keys[i]


def writeColorValue(data, index, value, alpha=True):
    writeNumericValue256(data, index, value.Red)
    writeNumericValue256(data, index + 5, value.Green)
    writeNumericValue256(data, index + 10, value.Blue)
    if (alpha):
        writeNumericValue(data, index + 15, value.alpha)


def faceShape(data, values=copy.deepcopy(default_values['shapeValueFace']), randomize=False, deviation=1.0):
    if (randomize):
        for i in range(len(values)):
            values[i] = normalRandom(
                default_values['shapeValueFace'][i], 15 * deviation)
    i = 0
    while (data[i] != 'shapeValueFace'):
        i += 1
    count = 0
    while (data[i] != 'headId'):
        if (data[i] == 202 and (data[i + 5] == 202 or data[i + 5] == 166)):
            writeNumericValue(data, i, values[count])
            count += 1
        i += 1
    return values


def facialType(data, type=4, skin_id=0, detail_id=0, detail_power=54, randomize=False, deviation=1.0):
    if (randomize):
        type = rand(4)
        skin_id = rand(9)
        detail_id = rand(18)
        detail_power = normalRandom(54, 25 * deviation)
    i = 0
    while (data[i] != 'headId'):
        i += 1
    data[i + 1] = type
    if (type == 0):
        data[i + 4] = skin_id
    if (type == 1):
        data[i + 4] = 9 + skin_id
    if (type == 2):
        data[i + 4] = 20 + skin_id
    if (type == 3):
        data[i + 4] = 30 + skin_id
    if (type == 4):
        data[i + 4] = 49 + skin_id
    data[i + 7] = detail_id
    writeNumericValue(data, i + 10, detail_power)
    return [type, skin_id, detail_id, detail_power]


def eyebrows(data, type=18, color=ColorHSV(), position=[50, 41, 50, 50, 50], randomize=False, deviation=1.0, hair_color=None):
    if (randomize):
        default_position = [50, 41, 50, 50, 50]
        type = rand(26)
        if (hair_color == None):
            hue, saturation, value, alpha = 20, 15, 0, 100
        else:
            hue, saturation, value, alpha = hair_color
        factor = deviation / (1 + deviation)
        hue = normalRandom(hue * factor + 20 * (1 - factor),
                           5 * deviation * deviation, 0, 360)
        saturation = normalRandom(
            saturation * factor + 15 * (1 - factor), 7 * deviation * deviation)
        value = normalRandom(value * factor, 35 * deviation)
        alpha = normalRandom(100, 15 * deviation)
        color = ColorHSV(hue, saturation, value, alpha)
        for i in range(5):
            position[i] = normalRandom(default_position[i], 7 * deviation)
    i = 0
    while (data[i] != 'eyebrowId'):
        i += 1
    data[i + 1] = type
    writeColorValue(data, i + 5, color.toRGB())
    while (data[i] != 'eyebrowLayout'):
        i += 1
        if (i == len(data) - 1):
            return None
    i += 2
    for j in range(4):
        writeNumericValue(data, i, position[j])
        i += 5
    writeNumericValue(data, i + 2, position[4])
    return [type, color] + position


def eyes(data, white_color1=ColorHSV(201, 2, 85), iris_id1=0, iris_color1=ColorHSV(14, 33, 29), iris_width1=70, iris_height1=70, iris_emission1=0, pupil_id1=0, pupil_color1=ColorHSV(), pupil_width1=83, pupil_height1=83, white_color2=ColorHSV(201, 2, 85), iris_id2=0, iris_color2=ColorHSV(14, 33, 29), iris_width2=70, iris_height2=70, iris_emission2=0, pupil_id2=0, pupil_color2=ColorHSV(), pupil_width2=83, pupil_height2=83, eye_same=True, eye_roll=50, hl_id=44, hl_color=ColorHSV(0, 0, 100), hl_width=50, hl_height=50, hl_X=50, hl_Y=50, hl_angle=50, shadow_scale=40, eyelashes_id=6, eyelashes_color=ColorHSV(0, 0, 0, 87), randomize=False, deviation=1.0, eyebrow_color=None):
    if (randomize):
        hue = normalRandom(201, 10 * deviation * deviation, 0, 360)
        saturation = normalRandom(2, 7 * deviation * deviation)
        value = normalRandom(85, 5 * deviation * deviation)
        white_color1 = ColorHSV(hue, saturation, value)
        hue = normalRandom(201, 10 * deviation * deviation, 0, 360)
        saturation = normalRandom(2, 7 * deviation * deviation)
        value = normalRandom(85, 5 * deviation * deviation)
        white_color2 = ColorHSV(hue, saturation, value)
        iris_id1 = rand(29)
        iris_id2 = rand(29)
        hue = normalRandom(14, 150 * deviation, 0, 360)
        saturation = normalRandom(33, 10 * deviation * deviation)
        value = normalRandom(29, 18 * deviation * deviation)
        iris_color1 = ColorHSV(hue, saturation, value)
        hue = normalRandom(14, 150 * deviation, 0, 360)
        saturation = normalRandom(33, 10 * deviation * deviation)
        value = normalRandom(29, 18 * deviation * deviation)
        iris_color2 = ColorHSV(hue, saturation, value)
        iris_width1 = normalRandom(70, 12 * deviation)
        iris_width2 = normalRandom(70, 12 * deviation)
        iris_height1 = normalRandom(iris_width1, 5 * deviation)
        iris_height2 = normalRandom(iris_width2, 5 * deviation)
        iris_emission1 = normalRandom(0, 7 * deviation * deviation)
        iris_emission2 = normalRandom(0, 7 * deviation * deviation)
        pupil_id1 = max(0, rand(7, -21))
        pupil_id2 = max(0, rand(7, -21))
        hue = normalRandom(180, 180, 0, 360)
        saturation = normalRandom(0, 10 * deviation * deviation)
        value = normalRandom(0, 8 * deviation * deviation)
        pupil_color1 = ColorHSV(hue, saturation, value)
        hue = normalRandom(180, 180, 0, 360)
        saturation = normalRandom(0, 10 * deviation * deviation)
        value = normalRandom(0, 8 * deviation * deviation)
        pupil_color2 = ColorHSV(hue, saturation, value)
        pupil_width1 = normalRandom(83, 15 * deviation)
        pupil_width2 = normalRandom(83, 15 * deviation)
        pupil_height1 = normalRandom(pupil_width1, 7 * deviation)
        pupil_height2 = normalRandom(pupil_height2, 7 * deviation)
        eye_same = (rand(5) > 0)
        eye_roll = normalRandom(47, 5 * deviation)
        hl_id = rand(44)
        hue = normalRandom(180, 180, 0, 360)
        saturation = normalRandom(0, 10 * deviation * deviation)
        value = normalRandom(100, 8 * deviation * deviation)
        hl_color = ColorHSV(hue, saturation, value)
        hl_width = normalRandom(50, 15 * deviation)
        hl_height = normalRandom(50, 15 * deviation)
        hl_X = normalRandom(50, 15 * deviation)
        hl_Y = normalRandom(50, 15 * deviation)
        hl_angle = normalRandom(50, 25 * deviation)
        shadow_scale = normalRandom(40, 20 * deviation)
        eyelashes_id = rand(8)
        if (eyebrow_color == None):
            hue, saturation, value, alpha = 0, 0, 0, 87
        else:
            hue, saturation, value, alpha = eyebrow_color
        hue = normalRandom(hue, 5 * deviation * deviation, 0, 360)
        saturation = normalRandom(saturation, 7 * deviation * deviation)
        value = normalRandom(value * 0.75, 35 * deviation)
        alpha = normalRandom(87, 30 * deviation)
        eyelashes_color = ColorHSV(hue, saturation, value, alpha)
    i = 0
    while (data[i] != 'whiteColor'):
        i += 1
    writeColorValue(data, i + 2, white_color1.toRGB())
    i += 23
    data[i + 1] = iris_id1
    i += 3
    writeColorValue(data, i + 2, iris_color1.toRGB())
    i += 23
    writeNumericValue(data, i + 1, iris_width1)
    i += 7
    writeNumericValue(data, i + 1, iris_height1)
    i += 7
    writeNumericValue(data, i + 1, iris_emission1)
    i += 7
    data[i + 1] = pupil_id1
    i += 3
    writeColorValue(data, i + 2, pupil_color1.toRGB())
    i += 23
    writeNumericValue(data, i + 1, pupil_width1)
    i += 7
    writeNumericValue(data, i + 1, pupil_height1)
    i += 8
    writeColorValue(data, i + 2, white_color1.toRGB())
    i += 23
    data[i + 1] = iris_id1 if eye_same else iris_id2
    i += 3
    writeColorValue(data, i + 2, iris_color1.toRGB()
                    if eye_same else iris_color2.toRGB())
    i += 23
    writeNumericValue(data, i + 1, iris_width1)
    i += 7
    writeNumericValue(data, i + 1, iris_height1)
    i += 7
    writeNumericValue(
        data, i + 1, iris_emission1 if eye_same else iris_emission2)
    i += 7
    data[i + 1] = pupil_id1 if eye_same else pupil_id2
    i += 3
    writeColorValue(data, i + 2, pupil_color1.toRGB()
                    if eye_same else pupil_color2.toRGB())
    i += 23
    writeNumericValue(data, i + 1, pupil_width1)
    i += 7
    writeNumericValue(data, i + 1, pupil_height1)
    i += 7
    data[i + 1] = 195 if eye_same else 194
    i += 3
    writeNumericValue(data, i + 1, eye_roll)
    i += 7
    data[i + 1] = hl_id
    i += 3
    writeColorValue(data, i + 2, hl_color.toRGB())
    i += 23
    writeNumericValue(data, i + 2, hl_width)
    writeNumericValue(data, i + 7, hl_height)
    writeNumericValue(data, i + 12, hl_X)
    writeNumericValue(data, i + 17, hl_Y)
    i += 23
    writeNumericValue(data, i + 1, hl_angle)
    i += 7
    writeNumericValue(data, i + 1, shadow_scale)
    i += 7
    data[i + 1] = eyelashes_id
    i += 3
    writeColorValue(data, i + 2, eyelashes_color.toRGB())
    return [white_color1, iris_id1, iris_color1, iris_width1, iris_height1, iris_emission1, pupil_id1, pupil_color1, pupil_width1, pupil_height1, white_color2, iris_id2, iris_color2, iris_width2, iris_height2, iris_emission2, pupil_id2, pupil_color2, pupil_width2, pupil_height2, eye_same, eye_roll, hl_id, hl_color, hl_width, hl_height, hl_X, hl_Y, hl_angle, shadow_scale, eyelashes_id, eyelashes_color]


def skinColor(data, skin_color=HSVtoRGB(24, 18, 78), skin_glossiness=68, skin_metalness=15, blush_id=5, blush_color=ColorRGB(167, 127, 114, 39), blush_glossiness=57, mole_id=0, mole_color=ColorRGB(0, 0, 0, 74), mole_width=70, mole_height=70, mole_X=50, mole_Y=49, randomize=False, deviation=1.0):
    if (randomize):
        base_hue = normalRandom(24, 5 * deviation * deviation, 0, 360)
        base_saturation = normalRandom(20, 7 * deviation * deviation)
        base_value = normalRandom(55, 35 * deviation)
        skin_color = HSVtoRGB(base_hue, base_saturation, base_value)
        skin_glossiness = normalRandom(68, 10 * deviation)
        skin_metalness = normalRandom(15, 7 * deviation)
        blush_id = rand(19)
        for i in range(4):
            if (blush_id in [10, 11, 12, 13, 14, 18, 19]):
                blush_id = rand(19)
        hue = normalRandom(14, 7 * deviation * deviation, 0, 360)
        saturation = normalRandom(31, 20 * deviation * deviation)
        value = normalRandom((base_value - 65) * 0.6 + 65, 10 * deviation)
        alpha = normalRandom(39, 35 * deviation)
        blush_color = HSVtoRGB(hue, saturation, value)
        blush_glossiness = normalRandom(skin_glossiness - 10, 10 * deviation)
        mole_id = max(0, rand(5, -2))
        if (mole_id > 2):
            hue = normalRandom(22, 5 * deviation * deviation, 0, 360)
            saturation = normalRandom(43, 12 * deviation * deviation)
            value = normalRandom(38, 23 * deviation)
            alpha = normalRandom(74, 20 * deviation)
            mole_color = HSVtoRGB(hue, saturation, value, alpha)
            mole_width = 70
            mole_height = 70
            mole_X = 50
            moly_Y = 49
        else:
            hue = normalRandom(18, 5 * deviation * deviation, 0, 360)
            saturation = normalRandom(15, 12 * deviation * deviation)
            value = normalRandom(0, 23 * deviation)
            alpha = normalRandom(74, 20 * deviation)
            mole_color = HSVtoRGB(hue, saturation, value, alpha)
            mole_width = normalRandom(30, 30)
            mole_height = normalRandom(mole_width, 20)
            mole_X = rand(80, 20)
            mole_Y = rand(65, 0)
    i = 0
    while (data[i] != 'moleId'):
        i += 1
    data[i + 1] = mole_id
    i += 3
    writeColorValue(data, i + 2, mole_color)
    i += 23
    writeNumericValue(data, i + 2, mole_width)
    writeNumericValue(data, i + 7, mole_height)
    writeNumericValue(data, i + 12, mole_X)
    writeNumericValue(data, i + 17, mole_Y)
    while (data[i] != 'cheekId'):
        i += 1
    data[i + 1] = blush_id
    i += 3
    writeColorValue(data, i + 2, blush_color)
    i += 23
    writeNumericValue(data, i + 1, blush_glossiness)
    while (data[i] != 'skinColor'):
        i += 1
    writeColorValue(data, i + 2, skin_color)
    i += 23
    writeNumericValue(data, i + 1, skin_glossiness)
    i += 7
    writeNumericValue(data, i + 1, skin_metalness)
    return [skin_color, skin_glossiness, skin_metalness, blush_id, blush_color, blush_glossiness, mole_id, mole_color, mole_width, mole_height, mole_X, mole_Y]


def makeup(data, eyeshadow_id=17, eyeshadow_color=ColorRGB(81, 45, 45, 27), eyeshadow_glossiness=0, lip_id=6, lip_color=ColorRGB(137, 41, 41, 74), lip_glossiness=80, randomize=False, deviation=1.0):
    if (randomize):
        eyeshadow_id = rand(43)
        eyeshadow_color = randomRGB(81, 45, 45, 70, 25 * deviation)
        eyeshadow_glossiness = normalRandom(0, 45 * deviation)
        lip_id = rand(18)
        for i in range(2):
            if lip_id > 15:
                lip_id = rand(18)
        lip_color = randomRGB(137, 41, 41, 74, 50 * deviation)
        lip_glossiness = normalRandom(80, 25 * deviation)
    i = 0
    while (data[i] != 'eyeshadowId'):
        i += 1
    data[i + 1] = eyeshadow_id
    i += 3
    writeColorValue(data, i + 2, eyeshadow_color)
    i += 23
    writeNumericValue(data, i + 1, eyeshadow_glossiness)
    while (data[i] != 'lipId'):
        i += 1
    data[i + 1] = lip_id
    i += 3
    writeColorValue(data, i + 2, lip_color)
    i += 23
    writeNumericValue(data, i + 1, lip_glossiness)
    return [eyeshadow_id, eyeshadow_color, eyeshadow_glossiness, lip_id, lip_color, lip_glossiness]


def hair(data, back_hair=0, bangs=0, base_color=ColorHSV(11, 24, 29), top_color=ColorHSV(26, 30, 13), under_color=ColorHSV(26, 16, 55), specular_color=ColorHSV(26, 30, 45), metalness=40, smoothness=20, randomize=False, deviation=1.0):
    if (randomize):
        back_hair = rand(61)
        bangs = rand(44)
        base_hue = normalRandom(20, 18 * deviation * deviation, 0, 360)
        base_saturation = normalRandom(30, 15 * deviation)
        base_value = normalRandom(43, 35 * deviation)
        base_color = ColorHSV(base_hue, base_saturation, base_value)
        hue = normalRandom(base_hue, 7 * deviation * deviation, 0, 360)
        saturation = normalRandom(base_saturation, 20 * deviation * deviation)
        value = normalRandom(base_value + 20, 10 * deviation)
        top_color = ColorHSV(hue, saturation, value)
        hue = normalRandom(base_hue, 7 * deviation * deviation, 0, 360)
        saturation = normalRandom(base_saturation, 20 * deviation * deviation)
        value = normalRandom(base_value, 10 * deviation)
        under_color = ColorHSV(hue, saturation, value)
        hue = normalRandom(base_hue, 7 * deviation * deviation, 0, 360)
        saturation = normalRandom(base_saturation, 20 * deviation * deviation)
        value = normalRandom(base_value + 30, 10 * deviation)
        specular_color = ColorHSV(hue, saturation, value)
        smoothness = normalRandom(20, 30 * deviation)
        metalness = normalRandom(40, 30 * deviation)
    i = 0
    while data[i] != 'sameSetting':
        i += 1
    while data[i] != 'baseColor':
        i += 1
    data[i - 2] = back_hair
    while data[i] != 'meshLayout':
        i += 1
    while data[i] != 'baseColor':
        i += 1
    data[i - 2] = bangs
    i = 0
    for j in range(12):
        while data[i] != 'topColor':
            i += 1
        while data[i] != 'baseColor':
            i -= 1
        writeColorValue(data, i + 2, base_color.toRGB())
        i += 23
        writeColorValue(data, i + 2, top_color.toRGB())
        i += 23
        writeColorValue(data, i + 2, under_color.toRGB())
        i += 23
        writeColorValue(data, i + 2, specular_color.toRGB())
        i += 23
        writeNumericValue(data, i + 1, metalness)
        i += 7
        writeNumericValue(data, i + 1, smoothness)
    return [back_hair, bangs, base_color, top_color, under_color, specular_color, metalness, smoothness]
