from math import log2
import sys
# header struct:
#   -0-7 bytes - __unimportant__
#   ...
#   12-13 bytes - width in pixels
#   14-15 bytes - height in pixels
#   16 byte - pixel depth (24)
#   17 - ...


def read_tga(filename):
    with open(filename, "br") as f:
        header = list(map(int, f.read(18)))
        width = header[13]*256+header[12]
        height = header[15]*256+header[14]
        image_array = [[(0,0,0) for _ in range(width+2)] for _ in range(height+2)]
        for row in range(height):
            for col in range(width):
                image_array[row+1][col+1] = tuple(map(int, f.read(3)))
        return image_array

class Pixel:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


def predictW(bit_map):
    prediction = [[(0,0,0) for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for y, row in enumerate(bit_map[1:-1]):
        for x, cell in enumerate(row[1:-1]):
            r = cell[0] - bit_map[y][x-1][0]
            g = cell[1] - bit_map[y][x-1][1]
            b = cell[2] - bit_map[y][x-1][2]
            prediction[y][x] = (r%256, g%256, b%256)
    return prediction


def predictN(bit_map):
    prediction = [[(0, 0, 0) for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for row_index, row in enumerate(bit_map[1:-1]):
        for col_index, cell in enumerate(row[1:-1]):
            r = cell[0] - bit_map[row_index-1][col_index][0]
            g = cell[1] - bit_map[row_index-1][col_index][1]
            b = cell[2] - bit_map[row_index-1][col_index][2]
            prediction[row_index][col_index] = (r%256, g%256, b%256)
    return prediction


def predictNW(bit_map):
    prediction = [[(0, 0, 0) for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for row_index, row in enumerate(bit_map[1:-1]):
        for col_index, cell in enumerate(row[1:-1]):
            r = cell[0] - bit_map[row_index-1][col_index-1][0]
            g = cell[1] - bit_map[row_index-1][col_index-1][1]
            b = cell[2] - bit_map[row_index-1][col_index-1][2]
            prediction[row_index][col_index] = (r%256, g%256, b%256)
    return prediction

# N + W - NW
def predictNW1(bit_map):
    prediction = [[(0, 0, 0) for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for row_index, row in enumerate(bit_map[1:-1]):
        for col_index, cell in enumerate(row[1:-1]):
            N = bit_map[row_index-1][col_index]
            W = bit_map[row_index][col_index-1]
            NW = bit_map[row_index-1][col_index-1]
            r = cell[0] - (N[0] + W[0] - NW[0])
            g = cell[1] - (N[1] + W[1] - NW[1])
            b = cell[2] - (N[2] + W[2] - NW[2])
            prediction[row_index][col_index] = (r%256, g%256, b%256)
    return prediction

# N + (W - NW)/2
def predictNW2(bit_map):
    prediction = [[(0, 0, 0) for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for row_index, row in enumerate(bit_map[1:-1]):
        for col_index, cell in enumerate(row[1:-1]):
            N = bit_map[row_index-1][col_index]
            W = bit_map[row_index][col_index-1]
            NW = bit_map[row_index-1][col_index-1]
            r = cell[0] - (N[0] + (W[0] - NW[0])//2)
            g = cell[1] - (N[1] + (W[1] - NW[1])//2)
            b = cell[2] - (N[2] + (W[2] - NW[2])//2)
            prediction[row_index][col_index] = (r%256, g%256, b%256)
    
    return prediction

# W + (N - NW)/2
def predictNW3(bit_map):
    prediction = [[(0, 0, 0) for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for row_index, row in enumerate(bit_map[1:-1]):
        for col_index, cell in enumerate(row[1:-1]):
            N = bit_map[row_index-1][col_index]
            W = bit_map[row_index][col_index-1]
            NW = bit_map[row_index-1][col_index-1]

            r = cell[0] - (W[0] + (N[0] - NW[0])//2)
            g = cell[1] - (W[1] + (N[1] - NW[1])//2)
            b = cell[2] - (W[2] + (N[2] - NW[2])//2)
            prediction[row_index][col_index] = (r%256, g%256, b%256)
    
    return prediction

# (N+W)/2
def predictNW4(bit_map):
    prediction = [[(0, 0, 0) for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for row_index, row in enumerate(bit_map[1:-1]):
        for col_index, cell in enumerate(row[1:-1]):
            N = bit_map[row_index-1][col_index]
            W = bit_map[row_index][col_index-1]

            r = cell[0] - (N[0] + W[0])//2 
            g = cell[1] - (N[1] + W[1])//2
            b = cell[2] - (N[2] + W[2])//2 
            prediction[row_index][col_index] = (r%256, g%256, b%256)
    
    return prediction


def predict_new(bit_map):
    prediction = [[(0, 0, 0) for _ in range(len(bit_map[0])-2)] for _ in range(len(bit_map)-2)]
    for row_index, row in enumerate(bit_map[1:-1]):
        for col_index, cell in enumerate(row[1:-1]):
            N = bit_map[row_index-1][col_index]
            W = bit_map[row_index][col_index-1]
            NW = bit_map[row_index-1][col_index-1]
            if NW[0] >= max(N[0], W[0]):
                r = max(N[0], W[0])
            elif NW[0] <= min(N[0], W[0]):
                r = min(N[0], W[0])
            else:
                r = W[0] + N[0] - NW[0]

            if NW[1] >= max(N[1], W[1]):
                g = max(N[1], W[1])
            elif NW[1] <= min(N[1], W[1]):
                g = min(N[1], W[1])
            else:
                b = W[1] + N[1] - NW[1]
            
            if NW[2] >= max(N[2], W[2]):
                b = max(N[2], W[2])
            elif NW[2] <= min(N[2], W[2]):
                b = min(N[2], W[2])
            else:
                b = W[2] + N[2] - NW[2]
            prediction[row_index][col_index] = ((cell[0] - r)%256, (cell[1] - g)%256, (cell[2] - b)%256)
    return prediction

types_desc = {
    predictW: "X̂ = W",
    predictN: "X̂ = N",
    predictNW: "X̂ = NW",
    predictNW1: "X̂ = N + W - NW",
    predictNW2: "X̂ = N + (W - NW)/2",
    predictNW3: "X̂ = W + (N - NW)/2",
    predictNW4: "X̂ = (N + W)/2",
    predict_new: "new standard"
}


def entropy(data_set):
    quantity = {i:0 for i in range(256)}
    for el in data_set:
        quantity[el] += 1       
    entropy = 0
    for el in range(256):
        if quantity[el] != 0:
            probability = quantity[el]/len(data_set)
            entropy -= probability*log2(probability)
    return entropy

def bit_map_to_tuple_list(list_list):
    new_list = []
    for el in list_list:
        for ee in el:
            new_list.append(ee)
    return new_list

def bit_map_to_list(list_list):
    new_list = []
    for el in list_list:
        for ee in el:
            for eee in ee:
                new_list.append(eee)
    return new_list

def get_colour(bitmap_list, n):
    return list(map(lambda x: x[n], bitmap_list))

def main():
    filename = sys.argv[1]
    x = read_tga(filename)

    e_min = (8, None)
    er_min = (8, None)
    eg_min = (8, None)
    eb_min = (8, None)

    x2 = [[x[i][j] for i in range(1,len(x)-1)] for j in range(1,len(x[0])-1)]
    print(f"Input file:\n    entropy={entropy(bit_map_to_list(x2))}")
    print(f"    red_entropy={entropy(get_colour(bit_map_to_tuple_list(x2),0))}")
    print(f"    green_entropy={entropy(get_colour(bit_map_to_tuple_list(x2),1))}")
    print(f"    blue_entropy={entropy(get_colour(bit_map_to_tuple_list(x2),2))}")

    for typee, desc in types_desc.items():
        y = typee(x)
        
        e1 = entropy(bit_map_to_list(y))
        er = entropy(get_colour(bit_map_to_tuple_list(y),0))
        eg = entropy(get_colour(bit_map_to_tuple_list(y),1))
        eb = entropy(get_colour(bit_map_to_tuple_list(y),2))

        if e1 < e_min[0]:
            e_min = (e1, desc)
        if er < er_min[0]:
            er_min = (er, desc)
        if eg < eg_min[0]:
            eg_min = (eg, desc)
        if eb < eb_min[0]:
            eb_min = (eb, desc)

        print(f"For prediction: {desc}")
        print(f"    entropy={e1}")
        print(f"    red_entropy={er}")
        print(f"    green_entropy={eg}")
        print(f"    blue_entropy={eb}")
        print()
    # print()
    print(f"Best results:")
    print(f"    Total: {e_min[0]} for {e_min[1]}")
    print(f"    Red: {er_min[0]} for {er_min[1]}")
    print(f"    Green: {eg_min[0]} for {eg_min[1]}")
    print(f"    Blue: {eb_min[0]} for {eb_min[1]}")

        

if __name__ == "__main__":
    main()