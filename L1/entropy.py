from math import log2
import sys

def entropy(file_name):
    with open(file_name, "rb") as f:

        bytes_file = f.read()
        length = len(bytes_file)

        symbols_quantity = {}   # częstości wystąpienia danego symbolu
        consecutive_symbols_quantity = {} # częstości wystąpienia symbolu po danym : x[a][b] - liczba wystąpień symbolu 'a' jako następnego po 'b'

        symbols_quantity = {i:0 for i in range(256)}
        consecutive_symbols_quantity = {i:{j:0 for j in range(256)} for i in range(256)}

        for byte in bytes_file:
            symbols_quantity[byte] += 1

        consecutive_symbols_quantity[bytes_file[0]][0]+=1

        for i in range(1,length):
            consecutive_symbols_quantity[bytes_file[i]][bytes_file[i-1]]+=1

        entropy = 0
        for symbol in range(256):
            if symbols_quantity[symbol] != 0:
                probability = symbols_quantity[symbol]/length
                entropy -= probability*log2(probability)

        conditional_entropy=0

        for x in range(256):
            prob_x = symbols_quantity[x]/length
            prob_y = 0
            for y in range(256):
                if symbols_quantity[x] != 0 and consecutive_symbols_quantity[y][x] !=0 :
                    temp = consecutive_symbols_quantity[y][x] / symbols_quantity[x]
                    prob_y -= temp*log2(temp)
            conditional_entropy += prob_x*prob_y

    print("Entropia: ", entropy)
    print("Entropia warunkowa:", conditional_entropy)


if __name__ == "__main__":
    entropy(sys.argv[1])
