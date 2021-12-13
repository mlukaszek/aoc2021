import sys
from collections import defaultdict

def fold(paper, folds):
    for (fx, fy) in folds:
        for (hx, hy) in paper.copy():
            if fy != 0 and hy > fy:
                del paper[(hx, hy)]
                paper[(hx, fy - (hy - fy))] = 1
            elif fx != 0 and hx > fx:
                del paper[(hx, hy)]
                paper[(fx - (hx - fx), hy)] = 1            
    return sum(paper.values())

def printPaper(paper):
    maxX = 1 + max([ hole[0] for hole in paper ])
    maxY = 1 + max([ hole[1] for hole in paper ])
    for j in range(maxY):
        for i in range(maxX):
            print("#" if paper[(i,j)] == 1 else " ", end="")
        print()
    print()

def main(args = ()):
    fileName = "day13.txt" if len(args) < 1 else args[0]

    paper = defaultdict(int)
    folds = []
    with open(fileName) as lines:
        for line in lines:
            line = line.strip()
            if "," in line:
                x, y = [ int(i) for i in line.split(",") ]
                paper[(x,y)] = 1
            elif "x=" in line:
                folds.append((int(line.split("=")[1]), 0))
            elif "y=" in line:
                folds.append((0, int(line.split("=")[1])))

    part1 = fold(paper, [ folds.pop(0) ])
    print("Part 1:", part1)

    # part 2: continue folding
    fold(paper, folds)
    print("Part 2:")
    printPaper(paper)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))