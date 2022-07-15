import random

mydict = {}
for i in range(1, 10001):
    k = 'k' + str(i)
    value = random.randint(1, 50000)
    mydict[k] = value
print(mydict)
mydict_sorted = sorted(mydict.items(), key=lambda x: x[1])
print(mydict_sorted)
