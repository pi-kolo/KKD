import universal_encodings
import argparse
from math import log2

def encode(file):
    dict_size = 256
    dictionary = {chr(i):i for i in range(dict_size)}

    w = ''
    result = []
    with open(file, "rb") as f:
        for c in f.read():
            wc = w + chr(c)
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                dictionary[wc] = dict_size
                dict_size += 1
                w = chr(c)
        if w:
            result.append(dictionary[w])
        return result 


def decode(code):
    dict_size = 256
    dictionary = {i:chr(i) for i in range(dict_size)}
    result = ''
    w = chr(code[0])
    code = code[1:]
    result += w
    for k in code:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        result += entry

        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry

    return result


def string_to_bits(text, file_out):
    with open(file_out, "wb") as f:
        padding = 8 - len(text)%8
        text = text + '0'*padding
        f.write(bytes([padding]))
        byte_arr = bytes([int(text[i:i+8],2) for i in range(0, len(text), 8)])
        f.write(byte_arr)


def file_to_bitstring(file):
    with open(file, "rb") as f:
        n = int.from_bytes((f.read(1)), byteorder='big')
        result = ''.join([bin(c)[2:].zfill(8) for c in f.read()])
        result = result[:len(result)-n]
    return result


def universal_coding(code, encoding):
    result = ''
    for el in code:
        result += encoding(el)
    return result


def universal_decoding(bit_string, encoding):
    result = []
    code = bit_string
    while len(code) > 0:
        n, code = encoding(code)
        result.append(n)
    return result


def encode_all(in_file, out_file, encoding):
    code_array = encode(in_file)
    bit_string = universal_coding(code_array, encoding)
    string_to_bits(bit_string, out_file) 


def decode_all(in_file, out_file, encoding):
    bit_string1 = file_to_bitstring(in_file)
    code_array = universal_decoding(bit_string1, encoding)
    bit_string2 = decode(code_array)
    byte_arr = bytes([ord(el) for el in bit_string2])
    with open(out_file, "wb") as f:
        f.write(byte_arr)


def stats(in_file, out_file):
    with open(in_file, "br") as f1, open(out_file, "br") as f2:
        f1_bytes = f1.read()
        f2_bytes = f2.read()
        
        symbols_quantity1 = {}   # częstości wystąpienia danego symbolu
        symbols_quantity1 = {i:0 for i in range(256)}
        
        for byte in f1_bytes:
            symbols_quantity1[byte] += 1
        entropy1 = 0
        for symbol in range(256):
            if symbols_quantity1[symbol] != 0:
                probability = symbols_quantity1[symbol]/len(f1_bytes)
                entropy1 -= probability*log2(probability)

        
        symbols_quantity2 = {}   # częstości wystąpienia danego symbolu
        symbols_quantity2 = {i:0 for i in range(256)}
        
        for byte in f2_bytes:
            symbols_quantity2[byte] += 1
        entropy2 = 0
        for symbol in range(256):
            if symbols_quantity2[symbol] != 0:
                probability = symbols_quantity2[symbol]/len(f2_bytes)
                entropy2 -= probability*log2(probability)
        print(f"Długość kodowanego: {len(f1_bytes)}")
        print(f"Długość zakodowanego: {len(f2_bytes)}")
        print(f"Stopień kompresji: {len(f1_bytes)/len(f2_bytes)}")
        print(f"Entropia kodowanego: {entropy1}")
        print(f"Entropia zakodowanego: {entropy2}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("-d", "--delta", action="store_true", help="Elias delta encoding")
    group1.add_argument("-g", "--gamma", action="store_true", help="Elias gamma encoding")
    group1.add_argument("-f", "--fibonacci", action="store_true", help="Fibonacci encoding")
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument("-D", "--decode", action="store_true")
    group2.add_argument("-E", "--encode", action="store_true")
    parser.add_argument("in_file", help="Input file")
    parser.add_argument("out_file", help="Output file")
    args = parser.parse_args()

    if args.encode:
        if args.delta:
            encode_all(args.in_file, args.out_file, universal_encodings.elias_delta)
        elif args.gamma:
            encode_all(args.in_file, args.out_file, universal_encodings.elias_gamma)
        elif args.fibonacci:
            encode_all(args.in_file, args.out_file, universal_encodings.fibonacci_encode)
        else:
            encode_all(args.in_file, args.out_file, universal_encodings.elias_omega)
        stats(args.in_file, args.out_file)
    else:
        if args.delta:
            decode_all(args.in_file, args.out_file, universal_encodings.delta_decode)
        elif args.gamma:
            decode_all(args.in_file, args.out_file, universal_encodings.gamma_decode)
        elif args.fibonacci:
            decode_all(args.in_file, args.out_file, universal_encodings.fibonacci_decode)
        else:
            decode_all(args.in_file, args.out_file, universal_encodings.omega_decode)
