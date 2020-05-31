# Na wstępie nie pozdrawiam.
import sys

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

# (min,255)
def quants(bits, min):
    delta = 255 - min
    n = 2**bits
    values = []
    for i in range(n):
        values.append(int(min + delta/n * (i+1)))
    quant_dict = {}
    k = 0
    for i in range(min, 256):
        if k+1 < n and abs(values[k+1] - i) <= abs(values[k] - i):
            k += 1
        quant_dict[i] = k

    return values, quant_dict



def differences_sequence(sequence):
    a = sequence[0]
    result = [a]
    for p in sequence[1:]:
        a = p - a
        result.append(a)
        a = p
    return result

def reconstruct_from_differences(diffs):
    a = diffs[0]
    result = [a]
    for q in diffs[1:]:
        a = a + q
        result.append(a)

    return result


def differential_encoding(bitmap, bits):
    pixels = []
    for _, row in enumerate(bitmap):
        for _, pixel in enumerate(row):
            pixels.extend([pixel.r, pixel.g, pixel.b])
    subs = differences_sequence(pixels)
    return subs
    # n-bits quantized values
    # v, quant_dict = quants(bits, -255)

    # quantize values 
    # coded = [quant_dict[el] for el in subs]
    # print(coded[:100])
    # print([v[el] for el in coded][:100])
    # print(coded)
    # return coded
    # return ''.join([num_to_bits(el, bits) for el in coded])


def differential_decoding(file):
    # quant_vals, _ = quants(bits, -255)
    bitstring, header = read_encoded(file)
    # differences = [quant_vals[int(bitstring[i:i+bits], 2)] for i in range(0, len(bitstring), bits)]
    differences = [int(bitstring[i:i+8], 2) for i in range(0, len(bitstring), 8)]
    rgbs = reconstruct_from_differences(differences) 
    return rgbs, header


def simple_quantizer_encoding(bitmap, bits):
    pixels = []
    for _, row in enumerate(bitmap):
        for _, pixel in enumerate(row):
            pixels.extend([pixel.r, pixel.g, pixel.b])
    
    quant_vals, quant_dict = quants(bits, 0)

    coded = [quant_dict[el] for el in pixels]

    return ''.join([num_to_bits(el, bits) for el in coded])


def simple_quantizer_decoding(file, bits):
    quant_vals, quant_dict = quants(bits, 0)
    bitstring, header = read_encoded(file)
    rgbs = [quant_vals[int(bitstring[i:i+bits], 2)] for i in range(0, len(bitstring), bits)]
 
    return rgbs, header


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


def nonuniform_quantizer(pixels, bits, min, max):
    n = 2**bits
    d = {i:0 for i in range(min, max+1)}
    for p in pixels:
        d[p] += 1
    intervals = {(i, i+1):d[i]+d[i+1] for i in d if i%2 == 0} 

    while len(intervals) > n:
        min_interval = sorted(intervals, key=intervals.get)[0]
        dict_list = list(intervals)
        k = dict_list.index(min_interval)

        if k == 0:
            to_join = dict_list[1]
        elif k == len(dict_list) - 1:
            to_join = dict_list[-2]
        else:
            if intervals[dict_list[k-1]] < intervals[dict_list[k+1]]:
                to_join = dict_list[k-1]
            else:
                to_join = dict_list[k+1]
        if to_join[0] > min_interval[0]:
            new_interval = (min_interval[0], to_join[1])
        else:
            new_interval = (to_join[0], min_interval[1])
        new_interval_value = intervals[min_interval] + intervals[to_join]
        intervals[new_interval] = new_interval_value
        del intervals[min_interval]
        del intervals[to_join]
        intervals = dict(sorted(intervals.items()))

    values = [(el[0]+el[1])//2 for el in intervals]
    quant_dict = {}
    j = 0
    for i in range(min, max+1):
        if j+1 < n and abs(values[j+1] - i) <= abs(values[j] - i):
            j += 1
        quant_dict[i] = j
        
    return values, quant_dict, intervals
        

def num_to_bits(x, n):
    return bin(x)[2:].zfill(n)

def smaller_header(h):
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
    return h

def main():

    if sys.argv[1] == '-e':
        if len(sys.argv) < 5:
            print("python coders.py -e k in_file out_file1 out_file2")
            return
        else:
            bm, h = read_tga(sys.argv[3])
            h2 = smaller_header(h.copy())

            x1 = transform(bm, highpass_filter)
            x2 = transform(bm, lowpass_filter)

            bitstring1 = simple_quantizer_encoding(x1, int(sys.argv[2]))
            bitstring_to_file(bitstring1, h2, sys.argv[4])

    elif sys.argv[1] == '-d':
        if len(sys.argv) < 5:
            print("nie tak")
            return
        else:
            if sys.argv[3] == '-L':
                rgbs, header = differential_decoding(sys.argv[4])
                with open(sys.argv[5], "wb") as f:
                    f.write(bytes(header) + bytes(rgbs))
            elif sys.argv[3] == '-H':
                rgbs, header = simple_quantizer_decoding(sys.argv[4], int(sys.argv[2]))
                with open(sys.argv[5], "wb") as f:
                    f.write(bytes(header) + bytes(rgbs))

    
if __name__ == "__main__":
    main()


