from math import floor

class Node:
    def __init__(self, value):
        self.value = value
        self.count = 1
        self.cumFreq = 0
        
    
class Tree:
    def __init__(self):
        self.nodes = []
        self.sum = 0
    
    def __str__(self):
        return ', '.join([str((el.value, el.count)) for el in self.nodes])

    def parent(self, index):
        return index//2
    
    def right_child(self, index):
        if 2*index + 1 >= len(self.nodes):
            return None
        else:
            return 2*index + 1
    
    def left_child(self, index):
        if 2*index >= len(self.nodes):
            return None
        else:
            return 2*index

    def cumFreqs(self):
        freq_dict = {}
        counter = 0
        for node in self.nodes[::-1]:
            freq_dict[node.value] = [(counter, counter+node.count)]
            counter += node.count
        for key, item in freq_dict.items():
            freq_dict[key].append((round(item[0][0]/counter, 5), round((item[0][1])/counter, 5)))
        return freq_dict
        # return {'A':[(0,1), (0, 0.2)], 'E':[(1,2), (0.2, 0.3)], 'K': [(2,4), (0.3,0.4)], 'M': [(4,5), (0.4,0.5)], 'R':[(5,10), (0.5, 0.6)], 'T':[(2,5), (0.6, 0.8)], 'Y':[(4,5), (0.8, 1.0)]}

    def find_index(self, value):
        for i, el in enumerate(self.nodes):
            if el.value == value:
                return i
        return None

    def find_node(self, value):
        for i, el in enumerate(self.nodes):
            if el.value == value:
                return el
        return None


    def next_character(self, value):
        self.sum += 1
        index = self.find_index(value)
        if index != None:
            self.nodes[index].count += 1
            to_swap = index
            while to_swap-1>=0 and self.nodes[to_swap-1].count < self.nodes[index].count:
                to_swap -= 1
            if index != to_swap:
                self.nodes[index], self.nodes[to_swap] = self.nodes[to_swap], self.nodes[index]
        else:
            self.nodes.append(Node(value))


def encode2(tree, filename_in, filename_out, n):
    low = 0
    high = 10**n-1
    frequences = tree.cumFreqs()
    out = []
    counter = 0
    with open(filename_in, "r") as f:
        c = f.read(1)
        while c:
            c = chr(ord(c))
            c_freq = frequences[c]

            low, high = low + (high - low + 1)*c_freq[1][0], low + (high - low + 1)*c_freq[1][1]-1
            low, high = int(low), int(high)
            print(f'L:{low}, H:{high}')
            low_str = str(low)
            high_str = str(high)
            
            # while low_str[0] == high_str[0]:
            #     out.append(low_str[0])
            #     if low != 0:
            #         low = int(low_str[1:]+'0')
            #     high = int(high_str[1:]+'9')
            #     if counter != 0:
            #         out.append(counter)

            while low//(10**(n-1)) == high//(10**(n-1)):
                out.append(low//(10**(n-1)))
                low = low%(10**(n-1))*10
                high = high%(10**(n-1))*10+9
                if counter != 0:
                    out.append(counter)

            # if low != 0 and int(low_str[0]) == int(high_str[0])-1 and low_str[1] == '9' and high_str[1] == '0':
            #     low = int(low_str[:2]+low_str[3:]+'0')
            #     high = int(high_str[:2]+high_str[3:]+'9')
            #     counter += 1

            if low//(10**(n-1)) == high//(10**(n-1)) - 1 and (low//(10**(n-2)))%10 == 9 and (high//(10**(n-2)))%10 == 0:
                low = low//(10**(n-2))+low%(10**(n-3))*10
                high = high//(10**(n-2))+high%(10**(n-3))*10+9
                counter += 1

            c = f.read(1)
        out.append(int(str(low)))
    with open(filename_out, "w") as f:
        f.write("LOL\n")
        f.write(''.join(list(map(str, out))))

def decode2(freq_dict, file_in, n):
    print(freq_dict)
    low = 0
    high = 10**n - 1
    # suma = 10
    suma = max([freq_dict[key][0][1] for key in freq_dict.keys()])
    out = []
    with open(file_in, "br") as f:
        _ = f.readline()
        code = int(f.read(n))
        # print(code)
        
        next_c = f.read(1)
        while len(out)<suma:
            print(code)
            index = (code - low) / (high - low + 1)
            print(f"For low:{low} and high: {high} found index {index}")
            for key, item in freq_dict.items():
                if item[1][0] <= index and item[1][1] > index:
                    c = key
                    out.append(c)
                    break
            print(c)
            low, high = low + (high - low + 1)*freq_dict[c][1][0], low + (high - low + 1)*freq_dict[c][1][1] - 1
            low, high = int(low), int(high)
            low_str, high_str = str(low), str(high)

            # while low_str[0] == high_str[0]:
            #     print(f"L:{low_str}, H:{high_str}")
            #     low = int(low_str[1:]+'0')
            #     high = int(high_str[1:]+'9')
            #     low_str, high_str = str(low), str(high)
            #     if next_c:
            #         code = int(str(code)[1:]+str(int(next_c)))
            #     next_c = f.read(1)

            while low//(10**(n-1)) == high//(10**(n-1)):
                # print(f"dropped {low//(10**(n-1))}")
                # print(f"L:{low_str}, H:{high_str}")
                print(f"Before drop: {low} - {high}, code: {code}", end="")
                low = low%(10**(n-1))*10
                high = high%(10**(n-1))*10+9
                if next_c:
                    print(next_c)
                    code = int(str(code)[1:]+str(int(next_c)))
                    print(f"After drop: {low} - {high}, code: {code}")
                    next_c = f.read(1)


            # if low_str[0] == high_str[0] and low_str[1] == '9' and high_str[1] == '0':
            #     low = int(low_str[:2]+low_str[3:]+'0')
            #     high = int(high_str[:2]+high_str[3:]+'9')
            #     if next_c:
            #         code =  int(str(code)[1:]+str(int(next_c)))
            #     next_c = f.read(1)
            
            if low // (10**(n-1)) == high // (10**(n-1)) and (low // (10**(n-2))) % 10 == 9 and (high // (10**(n-2))) % 10 == 0:
                print("ifend")
                print(f"L:{low_str}, H:{high_str}")
                low = low // (10**(n-2)) + low % (10**(n-3)) * 10
                high = high // (10**(n-2)) + high % (10**(n-3)) * 10 + 9 
                if next_c:
                    code = int(str(code)[1:]+str(int(next_c)))
                    next_c = f.read(1)
            print("---------------------------------------END OF ITERATION")
    return out



def encode(tree, filename, out, n):
    L = 0
    H2 = 10**n
    H = 10**n-1 
    frequences = tree.cumFreqs()
    res = []
    cntr = 0
    with open(filename, "br") as f:
        c = f.read(1)
        low = 0
        high = 1
        while c:
            c_char = chr(ord(c))
            c_range = high - low

            low, high = low + c_range*frequences[c_char][1][0], low + c_range*frequences[c_char][1][1]
            L = round(low*H2,0)
            H = round(high*(H2)-1, 0)
            if L//(H2/10) == H//(H2/10):
                res.append(round((L//(H2/10))))
                L = round(L%(H2/10)*10)
                low = (L/H2)
                H = round(H%(H2/10)*10 + 9)
                high = (H/H2)

            if low in (0, 0.5) and high in (0, 0.5):
                low *= 2
                high *=2
                res.append(0)
                for _ in range(cntr):
                    res.append(9)
                cntr = 0
            elif low in (0.5, 1) and high in (0.5, 1):
                low = 2*low - 1
                high = 2*high - 1
                res.append(9)
                for _ in range(cntr):
                    res.append(0)
                cntr = 0
            elif low in (0.25, 0.75) and high in (0.25, 0.75):
                low = 2*low - 0.5
                high = 2*high - 0.5
                cntr += 1

            c = f.read(1) 
        res.append(int(L))
        # if low < 0.25:
        #     res.append(0)
        #     for _ in range(cntr):
        #         res.append(9)
        # else:
        #     res.append(9)
        #     for _ in range(cntr):
        #         res.append(0)

    with open(out, "w") as f2:
        f2.write("XD\n")
        f2.write("".join(list(map(str, res))))


def decode(freq_dict, filename, n):
    low = 0
    high = 10**n-1
    suma = max([freq_dict[key][0][1] for key in freq_dict.keys()])
    res = []
    with open(filename, "r") as f:
        _ = f.readline()
        code = int(f.read(n))
        while len(res) < suma:
            index = ((code - low + 1)*suma - 1)/(high - low + 1)
            print(f'index:{index}', end=" ")
            for key, item in freq_dict.items():
                if item[0][0] <= index and item[0][1] > index:
                    letter = key
                    break
            res.append(letter)
            print(letter)
            low, high = low + (high - low + 1)*freq_dict[letter][0][0]/suma, low + (high - low + 1)*freq_dict[letter][0][1]/suma-1
            print(low, high)
            if low//(10**(n-1)) == high//(10**(n-1)):
                low = low%(10**(n-1))*10
                high = high%(10**(n-1))*10+9
                next = (f.read(1))
                if next:
                    code = code%(10**(n-1))*10 + int(next)
                print(low, high, code)
            
        

            print("-=-=-=-=-=-=-=-=-=-=-=-=-=")
    return res


def read_file(filename):
    with open(filename, "br") as f:
        tree = Tree()
        c = f.read(1)
        while c:
            tree.next_character(chr(ord(c)))
            c = f.read(1)
    return tree

tree = read_file("test2.txt")
print(tree)
print(tree.cumFreqs())
encode2(tree, "test2.txt","test3.txt", 6)
print("IIIIIIIIIIIIII")
print(decode2(tree.cumFreqs(), "test3.txt", 6))
# with open("test3.txt", "br") as f:
#     c = f.readline()
#     print(type(c))


# def quantize_values(high_probs, low_probs, high):
    
        
# print(quantize_values([0.1,0.2], 10000))
