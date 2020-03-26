import itertools
from collections import deque

def matches(l):
    count = 0
    for i in range(len(l)):
        count += 1 if i + 1== l[i] else 0
    return count

items = [1, 2, 3, 4, 5, 6, 7]
length = len(items)

allPermutations = itertools.permutations(items)
count = 0
oneMatches = []

for elem in allPermutations:
    p = list(elem)
    if matches(p) == 1:
        oneMatches.append(p)


for elem in oneMatches:
    p = deque(elem)
    funded = False
    for i in range(length - 1):
        p.rotate()
        if matches(p) >= 2:
            funded = True
            break
    if not funded:
        print(p)
        count += 1

print(count)

    