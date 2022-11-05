import modify
import time
import decoder
import shutil
from automation import ColorRGB
import random
from automation import rand

file_source = './modified-0.png'
location_file = open('game-location.txt', 'r')
file_destination = location_file.read().replace(
    '\n', '') + '/UserData/chara/female/modified-0.png'
location_file.close()

data = decoder.read_data("modified-0.png")


def randomFace():
    modify.faceShape(data, randomize=True, deviation=1.0)
    modify.facialType(data, randomize=True, deviation=1.2)
    modify.eyebrows(data, randomize=True, deviation=1.6)
    modify.eyes(data, randomize=True, deviation=1.0)
    modify.skinColor(data, randomize=True, deviation=1.0)
    modify.makeup(data, randomize=True, deviation=2.5)
    modify.hair(data, randomize=True, deviation=2.0)

    decoder.write_data("modified-0.png", data)
    shutil.copy(file_source, file_destination)
