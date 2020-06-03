import numpy as np 
import sys


H_matrix = np.matrix([[0, 1, 1, 1, 1, 0, 0, 0],
                        [1, 0, 1, 1, 0, 1, 0, 0],
                        [1, 1, 0, 1, 0, 0, 1, 0],
                        [1, 1, 1, 0, 0, 0, 0, 1]])


def decode(coded):
    coded = np.matrix(list(map(int, coded))).T
    error = H_matrix * coded % 2
    ones = len([el for el in error if el == 1])
    if ones == 3:
        i = np.where(error == 0)[0]
        coded[i] = 1 - coded[i]
    elif ones in (2, 4):
        return ''.join(map(str, coded.T.tolist()[0][:4])), False 
    return ''.join(map(str, coded.T.tolist()[0][:4])), True


def decode_file(file_in, file_out):
    bs = read_file(file_in)
    decoded = [decode(bs[i:i+8]) for i in range(0, len(bs), 8)]
    two_errors = len([el for el in decoded if el[1] == False])
    decoded = ''.join(map(lambda x: x[0], decoded))
    bitstring_to_file(decoded, file_out)
    print(f"Two errors occured {two_errors} times")


def read_file(filename):
    with open(filename, "br") as f:
        result = ''.join([bin(c)[2:].zfill(8) for c in f.read()])
    return result


def bitstring_to_file(bitstring, filename):
    with open(filename, "wb") as f:
        byte_arr = bytes([int(bitstring[i:i+8], 2) for i in range(0, len(bitstring), 8)])
        f.write(byte_arr)


def main():
    if len(sys.argv) < 3:
        print("Proper usage: python decoder.py <file_in> <file_out>")
        return
    else:
        decode_file(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()