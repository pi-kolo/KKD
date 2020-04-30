from itertools import permutations
perms = permutations([1,2,3,4,5])

def count_sth(perm):
    i = 0
    count = 1
    highest = perm[0]
    while i < len(perm)-1:
        if perm[i] < perm[i+1] and perm[i+1]>highest:
            highest = perm[i+1]
            count += 1
        i += 1
    return count

# perm_dict = {i:[] for i in range(1,6)}
# for perm in perms:
#     perm_dict[count_sth(perm)].append(perm)

# for i in range(1,6):
#     print(i, len(perm_dict[i]), perm_dict[i])
# print(count_sth([1,3,2,5,4]))


# xd = filter(lambda strin: strin[2]==5 and count_sth(list(reversed(strin)))==3, perm_dict[3])
# print(list(perms))
for x in perms:
    for y in perms:
        for z in perms:
            if x[4] == 5 and y[0] == x[1] and z[0] == x[2] and z[3] == 5: #and count_sth(x) == 3 and count_sth(y) == 4 and count_sth(z) == 4:
                print(x,y,z)
# first = filter(lambda x, y, z: x[4] == 5 and y[0] == x[1] and z[0] == x[2] and z[3] == 5 and count_sth(x) == 3 and count_sth(y) == 4 and count_sth(z) == 5, perms)

# print(list(first))