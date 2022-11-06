import modify
import time
import decoder
import shutil
from automation import ColorRGB
import random
from automation import rand

file_source = 'src/modified-0.png'
location_file = open('game-location.txt', 'r')
file_destination = location_file.read().replace(
    '\n', '') + '/UserData/chara/female/modified-0.png'
location_file.close()

data = decoder.read_data("src/modified-0.png")


def randomFace():
    face_shape_data = modify.faceShape(data, randomize=True, deviation=1.0)
    facial_type_data = modify.facialType(data, randomize=True, deviation=1.0)
    hair_data = modify.hair(data, randomize=True, deviation=1.0)
    eyebrows_data = modify.eyebrows(
        data, randomize=True, deviation=1.0, hair_color=hair_data[2])
    eyes_data = modify.eyes(data, randomize=True,
                            deviation=1.0, eyebrow_color=eyebrows_data[1])
    skinColor_data = modify.skinColor(data, randomize=True, deviation=1.0)
    makeup_data = modify.makeup(data, randomize=True, deviation=1.0)

    decoder.write_data("src/modified-0.png", data)
    shutil.copy(file_source, file_destination)
