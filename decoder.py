import copy
import random


def foo(c):
    if (c == 0):
        return ' '
    if (c < 32):
        return " " + str(c)
    if (c < 127):
        return chr(c)
    return " " + str(c)


def isletter(c):
    return ((c > 64 and c < 91) or (c > 96 and c < 123))


def process(data):
    result = []
    indx = 0
    while (indx < len(data)):
        if (not isletter(data[indx])):
            result.append(data[indx])
            indx += 1
        else:
            len_ = 1
            word = ""
            while (len_ + indx - 1 < len(data) and isletter(data[indx + len_])):
                len_ += 1
            if (len_ > 3):
                for i in range(len_):
                    word += chr(data[indx + i])
                result.append(word)
            else:
                for i in range(len_):
                    result.append(data[indx + i])
            indx += len_
    return result


_string_ = type('')


def isnumeric(s):
    for char in s:
        if (ord(char) > 57 or ord(char) < 48):
            return False
    return True


def read_(file):
    f_in = open(file, "r")
    data = f_in.read().replace(']', '').replace(
        '[', '').replace("'", '').split(', ')
    f_in.close()
    for i in range(len(data)):
        if (isnumeric(data[i])):
            data[i] = int(data[i])
    return data


def read_data(file):
    f_in = open(file, 'rb')
    data = process(f_in.read())
    f_in.close()
    return data


def write_data(file, data):
    f_out = open(file, "wb")
    to_bytes = []
    for elem in data:
        if (type(elem) == _string_):
            for char in elem:
                to_bytes.append(ord(char))
        else:
            to_bytes.append(elem)
    f_out.write(bytes(to_bytes))
    f_out.close()


values = [0] * 256
values[0] = [0, 0, 0, 0]
values[1] = [59, 128, 128, 129]
step = 128
for i in range(2, 255):
    values[i] = copy.copy(values[i - 1])
    values[i][2] = (values[i][2] + step) % 128 + 128
    values[i][1] += step
    if (values[i][1] == 128):
        step //= 2
    if (values[i][1] == 256):
        step //= 2
        values[i][1] = 0
        values[i][0] += 1
    values[i][3] = values[i][2] + 1
values[255] = [63, 128, 0, 0]


def WeirdChamp(value):
    global values
    return values[value]
