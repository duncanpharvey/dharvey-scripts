import itertools

letters = ['a'] * 1 + \
       ['b'] * 2 + \
       ['c'] * 2 + \
       ['d'] * 1 + \
       ['e'] * 1 + \
       ['f'] * 2 + \
       ['g'] * 1 + \
       ['h'] * 2 + \
       ['i'] * 1 + \
       ['j'] * 1 + \
       ['k'] * 1 + \
       ['l'] * 1 + \
       ['m'] * 2 + \
       ['n'] * 1 + \
       ['o'] * 1 + \
       ['p'] * 2 + \
       ['q'] * 1 + \
       ['r'] * 1 + \
       ['s'] * 1 + \
       ['t'] * 1 + \
       ['u'] * 1 + \
       ['v'] * 2 + \
       ['w'] * 2 + \
       ['x'] * 1 + \
       ['y'] * 2 + \
       ['z'] * 1

test = list(itertools.combinations(letters, 7))


def arrayTotal(arr):
       value = {
              'a': 1,
              'b': 3,
              'c': 3,
              'd': 2,
              'e': 1,
              'f': 4,
              'g': 2,
              'h': 4,
              'i': 1,
              'j': 8,
              'k': 5,
              'l': 1,
              'm': 3,
              'n': 1,
              'o': 1,
              'p': 3,
              'q': 10,
              'r': 1,
              's': 1,
              't': 1,
              'u': 1,
              'v': 4,
              'w': 4,
              'x': 8,
              'y': 4,
              'z': 10
       }
       total = 0
       for elem in arr:
              total += value[elem]
       return total

solutions = set()

for elem in test:
       if arrayTotal(elem) == 46:
              solutions.add(elem)

print(len(solutions))
print(solutions)
