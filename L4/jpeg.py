# header struct:
#   -0-7 bytes - __unimportant__
#   ...
#   12-13 bytes - width in pixels
#   14-15 bytes - height in pixels
#   16 byte - pixel depth (24)
#   17 - ...


def read_tga(filename):
    with open(filename, "br") as f:
        x = list(map(int, f.read(18)))
        width = x[13]*256+x[12]
        height = x[15]*256+x[14]
        image_array = [[[] for _ in range(width)] for _ in range(height)]
        for row in range(height):
            for col in range(width):
                image_array[row][col] = list(map(int, f.read(3)))
        return image_array


def predictW(bit_map):
    prediction = [[[] for _ in range(len(bit_map[0]))] for _ in range(len(bit_map))]
    for row_index, row in enumerate(bit_map):
        for col_index, cell in enumerate(row):
            if col_index == 0:
                prediction[row_index][col_index] = bit_map[row_index][col_index]
            else:
                r = cell[0] - bit_map[row_index][col_index-1][0]
                g = cell[1] - bit_map[row_index][col_index-1][1]
                b = cell[2] - bit_map[row_index][col_index-1][2]
                prediction[row_index][col_index] = [r,g,b]
    return prediction


def predictN(bit_map):
    prediction = [[[] for _ in range(len(bit_map[0]))] for _ in range(len(bit_map))]
    for row_index, row in enumerate(bit_map):
        for col_index, cell in enumerate(row):
            if row_index == 0:
                prediction[row_index][col_index] = bit_map[row_index][col_index]
            else:
                r = cell[0] - bit_map[row_index-1][col_index][0]
                g = cell[1] - bit_map[row_index-1][col_index][1]
                b = cell[2] - bit_map[row_index-1][col_index][2]
                prediction[row_index][col_index] = [r,g,b]
    return prediction


def predictNW(bit_map):
    prediction = [[[] for _ in range(len(bit_map[0]))] for _ in range(len(bit_map))]
    for row_index, row in enumerate(bit_map):
        for col_index, cell in enumerate(row):
            if row_index == 0 or col_index == 0:
                prediction[row_index][col_index] = bit_map[row_index][col_index]
            else:
                r = cell[0] - bit_map[row_index-1][col_index-1][0]
                g = cell[1] - bit_map[row_index-1][col_index-1][1]
                b = cell[2] - bit_map[row_index-1][col_index-1][2]
                prediction[row_index][col_index] = [r,g,b]
    return prediction

# N + W - NW
def predictNW1(bit_map):
    prediction = [[[] for _ in range(len(bit_map[0]))] for _ in range(len(bit_map))]
    for row_index, row in enumerate(bit_map):
        for col_index, cell in enumerate(row):
            if row_index == 0 and col_index == 0:
                prediction[row_index][col_index] = bit_map[row_index][col_index]
            elif row_index == 0:
                r = (cell[0] - (bit_map[row_index][col_index-1][0])) % 256
                g = (cell[1] - (bit_map[row_index][col_index-1][1])) % 256
                b = (cell[2] - (bit_map[row_index][col_index-1][2])) % 256
                prediction[row_index][col_index] = [r,g,b]
            elif col_index == 0:
                r = cell[0] - (bit_map[row_index-1][col_index][0])
                g = cell[1] - (bit_map[row_index-1][col_index][1])
                b = cell[2] - (bit_map[row_index-1][col_index][2])
                prediction[row_index][col_index] = [r%256,g%256,b%256]
            else:
                r = cell[0] - (bit_map[row_index-1][col_index][0] \
                    + bit_map[row_index][col_index][0] \
                    - bit_map[row_index-1][col_index-1][0])
                g = cell[1] - (bit_map[row_index-1][col_index][1] \
                    + bit_map[row_index][col_index][1] \
                    - bit_map[row_index-1][col_index-1][1])
                b = cell[2] - (bit_map[row_index-1][col_index][2] \
                    + bit_map[row_index][col_index][2] \
                    - bit_map[row_index-1][col_index-1][2])
                prediction[row_index][col_index] = [r%256,g%256,b%256]
    return prediction


# N + (W - NW)/2
def predictNW2(bit_map):
    prediction = [[[] for _ in range(len(bit_map[0]))] for _ in range(len(bit_map))]
    for row_index, row in enumerate(bit_map):
        for col_index, cell in enumerate(row):
            if row_index == 0 and col_index == 0:
                prediction[row_index][col_index] = bit_map[row_index][col_index]
            elif row_index == 0:
                r = cell[0] - (bit_map[row_index][col_index-1][0]) // 2
                g = cell[1] - (bit_map[row_index][col_index-1][1]) // 2
                b = cell[2] - (bit_map[row_index][col_index-1][2]) // 2
                prediction[row_index][col_index] = [r%256 ,g%256 ,b%256]
            elif col_index == 0:
                r = cell[0] - (bit_map[row_index-1][col_index][0])
                g = cell[1] - (bit_map[row_index-1][col_index][1])
                b = cell[2] - (bit_map[row_index-1][col_index][2])
                prediction[row_index][col_index] = [r%256, g%256, b%256]
            else:
                r = cell[0] - (bit_map[row_index-1][col_index][0] \
                    + (bit_map[row_index][col_index-1][0] \
                    - bit_map[row_index-1][col_index-1][0])//2)
                g = cell[1] - (bit_map[row_index-1][col_index][1] \
                    + (bit_map[row_index][col_index-1][1] \
                    - bit_map[row_index-1][col_index-1][1])//2)
                b = cell[2] - (bit_map[row_index-1][col_index][2] \
                    + (bit_map[row_index][col_index-1][2] \
                    - bit_map[row_index-1][col_index-1][2])//2)
                prediction[row_index][col_index] = [r%256, g%256, b%256]
    return prediction

# W + (N - NW)/2
def predictNW3(bit_map):
    prediction = [[[] for _ in range(len(bit_map[0]))] for _ in range(len(bit_map))]
    for row_index, row in enumerate(bit_map):
        for col_index, cell in enumerate(row):
            if row_index == 0 and col_index == 0:
                prediction[row_index][col_index] = bit_map[row_index][col_index]
            elif row_index == 0:
                r = cell[0] - (bit_map[row_index][col_index-1][0])
                g = cell[1] - (bit_map[row_index][col_index-1][1])
                b = cell[2] - (bit_map[row_index][col_index-1][2])
                prediction[row_index][col_index] = [r%256 ,g%256 ,b%256]
            elif col_index == 0:
                r = cell[0] - (bit_map[row_index-1][col_index][0]) // 2
                g = cell[1] - (bit_map[row_index-1][col_index][1]) // 2
                b = cell[2] - (bit_map[row_index-1][col_index][2]) // 2
                prediction[row_index][col_index] = [r%256, g%256, b%256]
            else:
                r = cell[0] - (bit_map[row_index][col_index-1][0] \
                    + (bit_map[row_index-1][col_index][0] \
                    - bit_map[row_index-1][col_index-1][0])//2)
                g = cell[1] - (bit_map[row_index][col_index-1][1] \
                    + (bit_map[row_index-1][col_index][1] \
                    - bit_map[row_index-1][col_index-1][1])//2)
                b = cell[2] - (bit_map[row_index][col_index-1][2] \
                    + (bit_map[row_index-1][col_index][2] \
                    - bit_map[row_index-1][col_index-1][2])//2)
                prediction[row_index][col_index] = [r%256, g%256, b%256]
    return prediction


# (N+W)/2
def predictNW4(bit_map):
    prediction = [[[] for _ in range(len(bit_map[0]))] for _ in range(len(bit_map))]
    for row_index, row in enumerate(bit_map):
        for col_index, cell in enumerate(row):
            if row_index == 0 and col_index == 0:
                prediction[row_index][col_index] = bit_map[row_index][col_index]
            elif row_index == 0:
                r = cell[0] - (bit_map[row_index][col_index-1][0]) // 2
                g = cell[1] - (bit_map[row_index][col_index-1][1]) // 2
                b = cell[2] - (bit_map[row_index][col_index-1][2]) // 2
                prediction[row_index][col_index] = [r%256 ,g%256 ,b%256]
            elif col_index == 0:
                r = cell[0] - (bit_map[row_index-1][col_index][0]) // 2
                g = cell[1] - (bit_map[row_index-1][col_index][1]) // 2
                b = cell[2] - (bit_map[row_index-1][col_index][2]) // 2
                prediction[row_index][col_index] = [r%256, g%256, b%256]
            else:
                r = cell[0] - (bit_map[row_index][col_index-1][0] \
                    + bit_map[row_index-1][col_index][0]) // 2
                g = cell[1] - (bit_map[row_index][col_index-1][1] \
                    + bit_map[row_index-1][col_index][1]) // 2
                b = cell[2] - (bit_map[row_index][col_index-1][2] \
                    + bit_map[row_index-1][col_index][2]) // 2
                prediction[row_index][col_index] = [r%256, g%256, b%256]
    return prediction

def predict_new(bit_map):
    prediction = [[[] for _ in range(len(bit_map[0]))] for _ in range(len(bit_map))]
    for row_index, row in enumerate(bit_map):
        for col_index, cell in enumerate(row):
            


x = read_tga("example0.tga")
print(predictW(x)[:1])
print(predictNW1(x)[:1])