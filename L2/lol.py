with open('test1.txt', "rb") as f:
    x = f.read()
    for el in x:
        print(bin(el))
    

import time

def timer(f):
    def show_time(*args):
        start = time.time()
        f(*args)
        print(f"Function time: {time.time()-start}")
    return show_time

@timer
def tests():
    text = ''.join(map(str, list(range(13**5))))

    for i in range(10**5):
        a = text[:8]
        # print(a)
        text = text[8:]


@timer
def tests2():
    text = ''.join(map(str, list(range(13**5))))
    i = 0
    while i < 10**5:
        a = text[i:i+8]
        # print(a)
        i += 8        

# tests()
# tests2()

