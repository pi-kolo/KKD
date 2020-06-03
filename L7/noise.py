import random
import sys


def read_file(filename):
    with open(filename, "br") as f:
        result = ''.join([bin(c)[2:].zfill(8) for c in f.read()])
    return result


def noise(bitstring, p):
    out = list(bitstring)
    for i, bit in enumerate(out):
        if random.random() < p:
            if bit == '0':
                out[i] = '1'
            else:
                out[i] = '0'
    return ''.join(out)


def bitstring_to_file(bitstring, filename):
    with open(filename, "wb") as f:
        byte_arr = bytes([int(bitstring[i:i+8], 2) for i in range(0, len(bitstring), 8)])
        f.write(byte_arr)


def main():
    if len(sys.argv) < 4:
        print("Correct usage: python noise.py <probability> <file_in> <file_out>")
        return
    bits = read_file(sys.argv[2])
    noised = noise(bits, float(sys.argv[1]))
    bitstring_to_file(noised, sys.argv[3])


if __name__ == "__main__":
    main()