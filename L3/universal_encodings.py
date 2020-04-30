
def elias_gamma(x):
    x_bin = bin(x)[2:]
    n = len(x_bin)
    return (n-1)*'0' + x_bin


def gamma_decode(code):
    i = 0
    result = []
    while i < len(code):
        n = code.index('1', i)
        result.append(int(code[n:n+n-i+1], 2))
        i += n + 1
    return result


def elias_delta(x):
    x_bin = bin(x)[2:]
    n = len(x_bin)
    n_bin = bin(n)[2:]
    k = len(n_bin)
    return (k-1)*'0' + n_bin + x_bin[1:]


def delta_decode(code):
    k = code.index('1')
    n = int(code[k:2*k+1], 2)
    x = '1' + code[2*k+1:2*k+n]
    return int(x, 2), code[2*k+n:]
    

def elias_omega(x):
    result = '0'
    k = x
    while k > 1:
        k_bin = bin(k)[2:]
        result = k_bin + result
        k = len(k_bin) - 1
    return result


def omega_decode(code):
    n = 1
    i = 0
    while code[i] != '0':
        prev_n = n
        n = int(code[i:i+prev_n+1],2)
        i = i + prev_n + 1 
    return n, code[i+1:]


FIB = [1, 2]

def gen_fib(x):
    while FIB[-1] < x:
        FIB.append(FIB[-1] + FIB[-2])
    return FIB


def gen_fib_2(n):
    while len(FIB) < n:
        FIB.append(FIB[-1] + FIB[-2])
    return FIB


def fibonacci_encode(x):
    gen_fib(x+1)
    index = 0
    current = x
    while FIB[index] <= current:
        index += 1
    index -= 1
    result = '1'
    current -= FIB[index]
    while index > 0:
        if current >= FIB[index-1]:
            result = '1' + result
            current -= FIB[index-1]
        else:
            result = '0' + result
        index -= 1
    return result + '1'


def fibonacci_decode(code):
    l = code.index('11')
    FIB = gen_fib_2(l+1)
    result = 0
    for i in range(l+1):
        result += int(code[i])*FIB[i]
    return result, code[l+2:] 

for el in [12, 45, 657, 456]:
    print(elias_gamma(el))

print(gamma_decode('00000000111001000'))