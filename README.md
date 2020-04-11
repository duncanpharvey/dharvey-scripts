# scripts

## Maths Puzzles

### [Rotating Table](https://www.think-maths.co.uk/table-puzzle)

Exactly one of your seven investors sits in the correct place, and the other six arrange themselves randomly. Find an arrangement the other six investors could make such that there is no rotation that puts at least two of the investors in the correct seat. [solution](https://github.com/duncanpharvey/scripts/blob/master/mathsPuzzles/cards.py)

### [Scrabble](https://www.think-maths.co.uk/scrabble-puzzle)

How many ways, from the 100 standard scrabble tiles, can you choose seven which total 46 points? [solution](https://github.com/duncanpharvey/scripts/tree/master/mathsPuzzles/scrabble)

Each point total of a scrabble hand has a distinct number of ways to achieve that point total.
For example, a point total of 46 can be achieved using letter tiles with the following point values:

* (1, 4, 5, 8, 8, 10, 10)
* (2, 3, 5, 8, 8, 10, 10)
* (3, 3, 4, 8, 8, 10, 10)
* (2, 2, 4, 8, 8, 10, 10)

For each one of these point value combinations, [scrabble.py](https://github.com/duncanpharvey/scripts/tree/master/mathsPuzzles/scrabble/scrabble.py) substitutes the possible letters for each point value and determines the cartesian product. It then removes duplicate combinations of letters since order doesn't matter. Finally, it verifies that the word is a valid scrabble word based on the number of available letters and summarizes the number of results for each point total.

Only a subset of these character combinations can create a real word. [scrabble_realwords.py](https://github.com/duncanpharvey/scripts/tree/master/mathsPuzzles/scrabble/scrabble_realwords.py) finds 7 letter scrabble words (including blanks!) and uses them to summarize how many unique letter combinations can create at least one real word for each point total.

[scrabble_vis_overlaid.py](https://github.com/duncanpharvey/scripts/tree/master/mathsPuzzles/scrabble/scrabble_vis_overlaid.py) and [scrabble_vis_separate.py](https://github.com/duncanpharvey/scripts/tree/master/mathsPuzzles/scrabble/scrabble_vis_separate.py) provide visualizations of the number of unique letter combinations and real words for each point total. The precomputed data comes directly from scrabble.py and scrabble_realwords.py.
