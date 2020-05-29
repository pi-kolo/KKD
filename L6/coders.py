# Na wstępie nie pozdrawiam.

def read_tga(filename):
    with open(filename, "br") as f:
        header = list(map(int, f.read(18)))
        width = header[13]*256+header[12]
        height = header[15]*256+header[14]
        image_array = [[Pixel(0, 0, 0) for _ in range(width)]
                       for _ in range(height)]
        for row in range(height):
            for col in range(width):
                image_array[row][col] = Pixel(*(list(map(int, f.read(3)))))
        return image_array, header


class Pixel:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str((self.r, self.g, self.b))

# gets list of each color coords as list
def get_r(bitmap):
    return [[pixl.r for pixl in row] for row in bitmap]

def get_g(bitmap):
    return [[pixl.g for pixl in row] for row in bitmap]

def get_b(bitmap):
    return [[pixl.b for pixl in row] for row in bitmap]


# calculates highpass color based on the neighbourhood (matrix [-1 -1 -1; -1 9 -1; -1 -1 -1])
def highpass_filter(bm, i, j):
    x = 9 * bm[i][j] - (bm[i-1][j] + bm[i+1][j] + bm[i][j-1] + bm[i][j+1] 
                        + bm[i-1][j-1] + bm[i-1][j+1] + bm[i+1][j-1] + bm[i+1][j+1])
    if x < 0:
        return 0
    elif x > 255:
        return 255
    else:
        return x

# calculates lowpass color based on the neighbourhood (matrix [1 1 1; 1 1 1; 1 1 1])
def lowpass_filter(bm, i, j):
    x = (bm[i][j] + (bm[i-1][j] + bm[i+1][j] + bm[i][j-1] + bm[i][j+1] +
                     bm[i-1][j-1] + bm[i-1][j+1] + bm[i+1][j-1] + bm[i+1][j+1]))//9
    if x < 0:
        return 0
    elif x > 255:
        return 255
    else:
        return x


def transform(bm, filter):
    rs, gs, bs = get_r(bm), get_g(bm), get_b(bm)
    
    output = [[None for pixl in row[1:-1]] for row in bm[1:-1]]

    for i, row in enumerate(bm[1:-1], 1):
        for j, _ in enumerate(row[1:-1], 1):
            output[i-1][j-1] = Pixel(
                filter(rs, i, j),
                filter(gs, i, j),
                filter(bs, i, j)
            )
    
    return output


def bitmap_to_bytes(bitmap):
    payload = []
    for i, row in enumerate(bitmap):
        for j, e in enumerate(row):
            payload.extend([e.r, e.g, e.b])
    return bytes(payload)

# (-255,255)
def quants1(bits):
    min = -255
    delta = 512
    n = 2**bits
    values = []
    for i in range(n):
        values.append(int(min + delta/n * (i+0.5)))
    quant_dict = {}
    k = 0
    for i in range(-255, 256):
        if k+1 < n and abs(values[k+1] - i) < abs(values[k] - i):
            k += 1
        quant_dict[i] = k

    return values, quant_dict

# (0, 255)
def quants2(bits):
    min = 0
    delta = 256
    n = 2**bits
    values = []
    for i in range(n):
        values.append(int(min + delta/n * (i+0.5)))
    quant_dict = {}
    k = 0
    for i in range(0, 256):
        if k+1 < n and abs(values[k+1] - i) < abs(values[k] - i):
            k += 1
        quant_dict[i] = k

    return values, quant_dict


def differential_encoding(bitmap, bits):
    pixels = []
    for _, row in enumerate(bitmap):
        for _, pixel in enumerate(row):
            pixels.extend([pixel.r, pixel.g, pixel.b]) 

    # differences sequence
    subs = [pixels[0]]
    for i, el in enumerate(pixels[:-1]):
        subs.append(pixels[i+1]-pixels[i])

    # n-bits quantized values
    quant_vals, quant_dict = quants1(bits)

    # quantize values 
    coded = [quant_dict[el] for el in subs]
    
    return ''.join([num_to_bits(el, bits) for el in coded])


def simple_quantizer_encoding(bitmap, bits):
    pixels = []
    for _, row in enumerate(bitmap):
        for _, pixel in enumerate(row):
            pixels.extend([pixel.r, pixel.g, pixel.b])
    
    quant_vals, quant_dict = quants2(bits)

    coded = [quant_dict[el] for el in pixels]

    return ''.join([num_to_bits(el, bits) for el in coded])

def simple_quantizer_decoding(file, bits):
    quant_vals, quant_dict = quants2(bits)
    bitstring, header = read_encoded(file)
    rgbs = [quant_vals[int(bitstring[i:i+bits], 2)] for i in range(0, len(bitstring), bits)]
    pixels = [Pixel(rgbs[i], rgbs[i+1], rgbs[i+2]) for i in range(0, len(rgbs), 3)]
    width = header[13]*256+header[12]
    height = header[15]*256+header[14]

    
    # image_array = [[None for _ in range(width)]
    #                    for _ in range(height)]
    # for row in range(height):
    #     for col in range(width):
    #         image_array[row][col] = pixels[row*width + col]

    return rgbs, header

def differential_decoding(file, bits):
    quant_vals, quant_dict = quants1(bits)
    bitstring, header = read_encoded(file)
    differences = [quant_vals[int(bitstring[i:i+bits], 2)] for i in range(0, len(bitstring), bits)]
    print(differences[:100])
    rgbs = [differences[0]]
    for i in range(1, len(differences)):    # NIE DZIAŁA AAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        rgbs.append(rgbs[-1] + differences[i])  # LECI W INFFFFFFFFFFINITY
    # for i, el in enumerate(differences[1:]):
    #     rgbs.append(rgbs[-1] + differences[i+1])
    # print(rgbs[:100])
    pixels = [Pixel(rgbs[i], rgbs[i+1], rgbs[i+2]) for i in range(0, len(rgbs), 3)]
    width = header[13]*256+header[12]
    height = header[15]*256+header[14]
    image_array = [[None for _ in range(width)]
                       for _ in range(height)]
    for row in range(height):
        for col in range(width):
            image_array[row][col] = pixels[row*width + col]

    return image_array

# read encoded file (that has header and encoded bitmap somehow)
def read_encoded(file_in):
    with open(file_in, "br") as f:
        header = list(map(int, f.read(18)))
        n = int.from_bytes((f.read(1)), byteorder='big')
        result = ''.join([bin(c)[2:].zfill(8) for c in f.read()])
        result = result[:len(result)-n]
    return result, header

# save bitstring as a file
def bitstring_to_file(bitstring, header, file_out):
    padding = 8 - len(bitstring)%8
    bitstring = bitstring + padding*'0'
    bytes_list = bytes([padding]) + bytes([int(bitstring[i:i+8],2) for i in range(0, len(bitstring), 8)])
    with open(file_out, "bw") as f:
        f.write(bytes(header) + bytes_list)


def num_to_bits(x, n):
    return bin(x)[2:].zfill(n)


def main():
    bm, h = read_tga("example0.tga")

    if h[12] == 0:
        h[12] = 254
        h[13] -= 1
    else:
        h[12] -= 2
    if h[14] == 0:
        h[14] = 254
        h[15] -= 1
    else:
        h[14] -= 2  
    
    x = transform(bm, highpass_filter)

    # coded = differential_encoding(x, 5)
    # bitstring_to_file(coded, h, "example.out")
    # # coded2, h2 = read_encoded("example.out")

    # bm2 = differential_decoding("example.out", 5)

    coded = simple_quantizer_encoding(x, 5)
    bitstring_to_file(coded, h, "example.out")
    # coded2, h2 = read_encoded("example.out")
    bm2, h2 = simple_quantizer_decoding("example.out", 5)
    # bitstring_to_file(bm2, h2, "examplee.tga")
    # print(bm2)
    with open("exampleee.tga", "wb") as f:
        f.write(bytes(h2) + bytes(bm2))

main()