import shutil
file_source = 'C:/Users/ivank/Desktop/RG_test/modified-0.png'
file_destination = 'C:/Stuff/Room-Girl_/UserData/chara/female/modified-0.png'

_string_ = type('')


def isnumeric(s):
    for char in s:
        if (ord(char) > 57 or ord(char) < 48):
            return False
    return True


def read_data(file):
    f_in = open(file, "r")
    data = f_in.read().replace(']', '').replace(
        '[', '').replace("'", '').split(', ')
    f_in.close()
    for i in range(len(data)):
        if (isnumeric(data[i])):
            data[i] = int(data[i])
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


data = read_data("out-1.txt")
write_data("modified-0.png", data)

shutil.copy(file_source, file_destination)

print("writing done")
