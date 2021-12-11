import sys
from collections import defaultdict
from functools import reduce
from operator import add

def adjacent(i,j):
    return ((i+1,j), (i-1,j), (i,j+1), (i,j-1), (i+1,j+1), (i-1,j-1), (i+1,j-1), (i-1,j+1))

def in_range(i, j, size):
    return 0 <= min(i, j) and max(i, j) < size

def find_high_energy(levels):
    return set([ location for location in levels if levels[location] > 9 ])

def flash(levels, size):
    for i in range(size):
        for j in range(size):
            levels[(i,j)] += 1
    
    flashing = find_high_energy(levels)
    flashed = set()
    while len(flashing - flashed):
        for location in (flashing - flashed):
            flashed.add(location)
            i, j = location
            for adj in adjacent(i,j):
                ai, aj = adj
                if in_range(ai, aj, size):
                    levels[adj] += 1
        flashing = find_high_energy(levels)

    for location in flashed:
        levels[location] = 0
    return len(flashed)

def flashesAfter(levels, size, steps):
    return reduce(add, [ flash(levels, size) for _ in range(steps) ])

def main(args = ()):
    fileName = "day11.txt" if len(args) < 1 else args[0]

    levels = defaultdict(int)
    with open(fileName) as lines:
        for j, row in enumerate(lines):
            for i, energy in enumerate(row.strip()):
                levels[(i,j)] = int(energy)
    size = max(i+1, j+1)

    steps = 100
    print("Part 1:", flashesAfter(levels, size, steps))
    
    while not all([ levels[location] == 0 for location in levels ]):
        flash(levels, size)
        steps +=1 
    print("Part 2:", steps)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))