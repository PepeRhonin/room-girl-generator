import shutil
file_source = 'C:/Stuff/Room-Girl_/UserData/chara/female/modified-0.png'
file_destination = 'C:/Users/ivank/Desktop/RG_test/modified-0.png'

# shutil.copy(file_source, file_destination)


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


f_in = open('test-0.png', 'rb')
data_1 = f_in.read()
f_in.close()

f_out = open('out-0.txt', 'w')
f_out.write(str(process(data_1)))
f_out.close()

f_in = open('test-1.png', 'rb')
data_1 = f_in.read()
f_in.close()

f_out = open('out-1.txt', 'w')
f_out.write(str(process(data_1)))
f_out.close()

print('reading done')
