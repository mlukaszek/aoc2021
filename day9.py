import sys
from collections import defaultdict
from functools import reduce
from operator import mul

def adjacent(i, j):
    return ((i,j+1), (i,j-1), (i+1,j), (i-1,j))

def get_low_points(heightmap):
    lowpoints = []
    for location, value in heightmap.items():
        i, j = location
        if all([ value < heightmap[adj] for adj in adjacent(i,j) if adj in heightmap ]):
            lowpoints.append(location)
    return lowpoints

def get_risk(heightmap):
    return sum([ 1 + heightmap[lowpoint] for lowpoint in get_low_points(heightmap) ])

def get_basins(heightmap):
    lowpoints = get_low_points(heightmap)

    basins = []
    for lowpoint in lowpoints:
        locations = set([lowpoint])
        neighbours = set()
        size = 0
        while size != len(locations): # look for neighbours until we stop finding new ones
            size = len(locations)
            for i, j in locations:
                neighbours.update([ neighbour for neighbour in adjacent(i,j) if heightmap[neighbour] < 9 ])
            locations.update(neighbours)
        basins.append({ "lowpoint":lowpoint, "size":len(locations) })
    return basins

def main(args = ()):
    fileName = "day9.txt" if len(args) < 1 else args[0]

    heightmap = defaultdict(lambda:9)
    with open(fileName) as lines:
        for j, row in enumerate(lines):
            for i, height in enumerate(row.strip()):
                heightmap[(i,j)] = int(height)

    print("Part 1:", get_risk(heightmap))

    largest_basins = [ basin["size"] for basin in sorted(get_basins(heightmap), key=lambda basin: basin["size"], reverse=True)[:3] ]
    part2 = reduce(mul, largest_basins)
    print("Part 2:", part2)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))