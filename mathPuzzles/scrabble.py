import itertools
import plotly.express as px
import pandas as pd

letterQuantity = {
    'a': 9,
    'b': 2,
    'c': 2,
    'd': 4,
    'e': 12,
    'f': 2,
    'g': 3,
    'h': 2,
    'i': 9,
    'j': 1,
    'k': 1,
    'l': 4,
    'm': 2,
    'n': 6,
    'o': 8,
    'p': 2,
    'q': 1,
    'r': 6,
    's': 4,
    't': 6,
    'u': 4,
    'v': 2,
    'w': 2,
    'x': 1,
    'y': 2,
    'z': 1,
    ' ': 2
}

letterIndex = {
    0: [' '],
    1: ['a', 'e', 'i', 'o', 'u', 'l', 'n', 's', 't', 'r'],
    2: ['d', 'g'],
    3: ['b', 'c', 'm', 'p'],
    4: ['f', 'h', 'v', 'w', 'y'],
    5: ['k'],
    8: ['j', 'x'],
    10: ['q', 'z']
}

# returns a dictionary with a list of totals for 7 letters and the letter value combinations for that total
# ex. {46: (1, 4, 5, 8, 8, 10, 10), (2, 3, 5, 8, 8, 10, 10), (3, 3, 4, 8, 8, 10, 10), (2, 2, 4, 8, 8, 10, 10)}
def valueCombinations():
    # possible values based on the number of available letters
    values = [0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3,
              3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 8, 8, 10, 10]

    results = list(itertools.combinations(values, 7))

    summary = {}

    for result in results:
        total = 0
        for elem in result:
            total += elem
        if total in summary:
            values = summary[total]
        else:
            values = set()
        values.add(result)
        summary[total] = values

    return summary


# get all possible value combinatons for each total from 5 to 49
print('summarizing combinations of values for each total')
valueCombinations = valueCombinations()

# apply letters based on point value for each value combination for a total
print('total | possible words')
x = []
y = []
for total in range(5, 50):
    solutions = set()
    for combination in valueCombinations[total]:
        # get possible letter combinations based on the values
        words = list(itertools.product(letterIndex[combination[0]], letterIndex[combination[1]], letterIndex[combination[2]],
                                       letterIndex[combination[3]], letterIndex[combination[4]], letterIndex[combination[5]], letterIndex[combination[6]]))

        # remove duplicate words
        wordSet = set()
        for word in words:
            word = list(word)
            word.sort()
            wordSet.add(tuple(word))

        # check if letter count in word exceeds number of available letters
        for word in wordSet:
            letterSummary = {}
            for letter in word:
                if letter in letterSummary:
                    letterSummary[letter] += 1
                else:
                    letterSummary[letter] = 1

            add = True
            for letter in letterSummary:
                if letterSummary[letter] > letterQuantity[letter]:
                    add = False
                    break

            if add:
                solutions.add(word)
                
    num = len(solutions)
    print(str(total).rjust(5, ' '), '|', str(num).rjust(14, ' '))
    x.append(total)
    y.append(num)

df = pd.DataFrame({'total': x, 'possible words': y})
fig = px.bar(df, x = "total", y = "possible words")
fig.show()
