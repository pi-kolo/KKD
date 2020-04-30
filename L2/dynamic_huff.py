import sys, getopt
from math import log2

class Node():
    def __init__(self, parent=None, left=None, right=None, weight=0, symbol=''):
        self.parent = parent
        self.left = left
        self.right = right
        self.weight = weight
        self.symbol = symbol

class HuffmanTree():

    def __init__(self):
        self.NYT = Node(symbol="NYT")
        self.root = self.NYT
        self.nodes = []
        self.seen = [None] * 256
    
    def encode(self, text):
        result = ''
        for c in text:
            if self.seen[ord(c)]:
                result += self.get_code(c, self.root)
            else:
                result += self.get_code('NYT', self.root)
                result += bin(ord(c))[2:].zfill(8)
            self.insert(c)

        padding = 8-len(result)%8
        result = str(padding) + result + '0'*padding
        return result
    
    def decode(self, in_file, out_file):
        with open(in_file, "r", encoding='utf-8') as f1:
            with open(out_file, "w") as f2:
                n = int(f1.read(1))
                text = ''.join([bin(ord(c))[2:].zfill(8) for c in f1.read()])
                text = text[:len(text)-n]
                # print(text)
                symbol = self.get_symbol(text[:8])
                f2.write(symbol)
                self.insert(symbol)
                node = self.root

                i = 8
                while i < len(text):
                    if text[i] == '0':
                        node = node.left
                    else:
                        node = node.right
                    symbol = node.symbol
                    if symbol:
                        if symbol == 'NYT':
                            symbol = self.get_symbol(text[i+1:i+9])
                            i += 8
                        f2.write(symbol)
                        self.insert(symbol)
                        node = self.root
                    i += 1
                
    def get_symbol(self, bin_str):
        return chr(int(bin_str, 2))

    def get_code(self, c, node, code=''):
        if node.left is None and node.right is None:
            return code if node.symbol == c else ''
        else:
            temp = ''
            if node.left is not None:
                temp = self.get_code(c, node.left, code+'0')
            if not temp and node.right is not None:
                temp = self.get_code(c, node.right, code+'1')
            return temp

    def largest_node(self, weight):
        for n in self.nodes:
            if n.weight == weight:
                return n    

    def insert(self, c):
        node = self.seen[ord(c)]
        if node is None:
            new = Node(symbol=c, weight=1)
            internal = Node(symbol='', weight=1, parent=self.NYT.parent, left=self.NYT, right=new)
            new.parent = internal
            self.NYT.parent = internal

            if internal.parent is not None:
                internal.parent.left = internal
            else:
                self.root = internal
            
            self.nodes.append(internal)
            self.nodes.append(new)

            self.seen[ord(c)] = new
            node = internal.parent
        
        while node is not None:
            largest = self.largest_node(node.weight)
            if node is not largest and node is not largest.parent and largest is not node.parent:
                self.swap(node, largest)
            node.weight = node.weight + 1
            node = node.parent

    def swap(self, n1, n2):
        i1, i2 = self.nodes.index(n1), self.nodes.index(n2)
        self.nodes[i1], self.nodes[i2] = self.nodes[i2], self.nodes[i1]

        tmp_parent = n1.parent
        n1.parent = n2.parent
        n2.parent = tmp_parent

        if n1.parent.left is n2:
            n1.parent.left = n1
        else:
            n1.parent.right = n1

        if n2.parent.left is n1:
            n2.parent.left = n2
        else:
            n2.parent.right = n2


def entropy_and_others(file_in, file_out):
    with open(file_in, "rb") as f1:

        bytes_file = f1.read()
        length = len(bytes_file)
        symbols_quantity = {}   # częstości wystąpienia danego symbolu
        symbols_quantity = {i:0 for i in range(256)}
        for byte in bytes_file:
            symbols_quantity[byte] += 1

        entropy = 0
        for symbol in range(256):
            if symbols_quantity[symbol] != 0:
                probability = symbols_quantity[symbol]/length
                entropy -= probability*log2(probability)
    with open(file_out, "rb") as f2:
        encoded = f2.read()
        compression_lvl = len(bytes_file)/(len(encoded))
        avg_length = len(encoded)*8/len(bytes_file)
        
    print("Entropia: ", entropy)
    print("Stopień kompresji: ", compression_lvl)
    print("Średnia długość kodu ", avg_length)


def string_to_bits(text, file_out):
    with open(file_out, "w", encoding='utf-8') as f:
        f.write(text[0])
        text = text[1:]
        while len(text) > 0:
            f.write(chr(int(text[:8], 2)))
            text = text[8:]


def main():

    if len(sys.argv) < 4:
        print("python _program_ -d/-e <infile> <outfile>")
        return
    else: 
        if sys.argv[1] == '-e':
            with open(sys.argv[2], "r") as f:
                text = f.read()
                string_to_bits(HuffmanTree().encode(text), sys.argv[3])
            entropy_and_others(sys.argv[2], sys.argv[3])
            
        if sys.argv[1] == '-d':
            HuffmanTree().decode(sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()