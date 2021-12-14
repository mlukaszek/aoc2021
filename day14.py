import sys
from collections import Counter

def grow(template, formula, steps=10):
    characterCounter = Counter(template)
    
    pairs = [ a+b for a,b in zip(template, template[1:])]
    pairCounter = Counter(pairs)

    for step in range(steps):
        stepCounter = Counter()
        for pair, count in pairCounter.items():
            # Count the character being inserted
            middleChar = formula[pair]
            characterCounter[middleChar] += count

            # Determine newly created pairs and count them, too
            leftPair = pair[0] + middleChar
            rightPair = middleChar + pair[1]
            stepCounter[leftPair] += count
            stepCounter[rightPair] += count

        pairCounter = stepCounter
    return characterCounter

def main(args = ()):
    fileName = "day14.txt" if len(args) < 1 else args[0]

    formula = {}
    template = ""
    with open(fileName) as lines:
        for line in lines:
            line = line.strip()
            if line and "->" not in line:
                template = line
            elif "->" in line:
                pair, insert = line.split(" -> ")
                formula[pair] = insert

    for part, steps in enumerate((10, 40)):
        counter = grow(template, formula, steps)
        mc = counter.most_common()
        print(f"Part {part+1}:", mc[0][1] - mc[-1][1])

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))