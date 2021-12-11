import sys

matching = {"(": ")", "[": "]", "{": "}", "<": ">"}
mismatchPenalties = {")": 3, "]": 57, "}": 1197, ">": 25137}

def parse(line):
    opened = []
    for bracket in line.strip():
        if bracket in "([{<":
            opened.append(bracket)
        elif bracket in ")]}>":
            expected = matching[opened[-1]]
            if bracket != expected:
                raise RuntimeError(mismatchPenalties[bracket])
            opened.pop()
    if len(opened):
        score = 0
        autocomplete = [ matching[bracket] for bracket in reversed(opened) ]
        for bracket in autocomplete:
            score *= 5
            score += " )]}>".find(bracket)
        return score

def main(args = ()):
    fileName = "day10.txt" if len(args) < 1 else args[0]

    errorScore = 0
    autocompleteScores = []

    with open(fileName) as lines:
        for line in lines:
            try:
                autocompleteScores.append(parse(line))
            except RuntimeError as e:
                errorScore += e.args[0]

    print("Part 1:", errorScore)
    print("Part 2:", sorted(autocompleteScores)[int(len(autocompleteScores)/2)])

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))