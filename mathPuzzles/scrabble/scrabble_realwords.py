import nltk
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

letterValue = {
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
    'z': 10,
    ' ': 0
}

x = 0
words = set() # all possible permutations of letters that form real scrabble words
words_sorted = set() # unique combination of letters that forms at least one real scrabble word
for word in nltk.corpus.words.words("en"):
    x += 1
    if x % 10000 == 0:
        print(x)
    # validate word length
    if len(word) != 7:
        continue
    
    # remove proper nouns
    pos = nltk.pos_tag(nltk.tokenize.word_tokenize(word))[0][1]
    if pos in {'NNP', 'NNPS'}:
        continue

    word = word.lower()

    # find all ways to construct word using 0, 1, or 2 blanks
    blankWords = [word]
    for i in range(7):
        oneBlank = word[:i] + ' ' + word[i + 1:]
        blankWords.append(oneBlank)
        for j in range(i + 1, 7):
            blankWords.append(oneBlank[:j] + ' ' + oneBlank[j + 1:])

    # is it a valid scrabble word based on available letters
    for w in blankWords:
        letterSummary = {}
        for letter in w:
            letterSummary[letter] = letterSummary.get(letter, 0) + 1

        add = True
        for letter in letterSummary:
            if letterSummary[letter] > letterQuantity[letter]:
                add = False
                break

        if not add:
            continue

        words.add(w)
        words_sorted.add(''.join(sorted(w)))

print('total words: ', len(words))
print('unique combinations of letters that form at least one real word: ', len(words_sorted))

totalSummary = {}
for w in words_sorted:
    total = 0
    for l in w:
        total += letterValue[l]
    totalSummary[total] = totalSummary.get(total, 0) + 1

x = []
y = []
for i in range(5, 50):
    x.append(i)
    y.append(totalSummary.get(i, 0))

print(x)
print(y)

df = pd.DataFrame({'total': x, 'possible words': y})
fig = px.bar(df, x = "total", y = "possible words")
fig.show()
    
    

    
