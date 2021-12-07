import sys
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Line:
    start: Point
    end: Point

def mark(segment, diagram):
    dx =  segment.end.x - segment.start.x 
    dy =  segment.end.y - segment.start.y
    if dx: dx = dx / abs(dx)
    if dy: dy = dy / abs(dy)

    x, y = segment.start.x, segment.start.y
    diagram[(x,y)] += 1

    while x != segment.end.x or y != segment.end.y:
        x += dx
        y += dy
        diagram[(x,y)] += 1

def mark_segments(segments, diagram, diagonals):
    for segment in segments:
        if diagonals or segment.start.x == segment.end.x or segment.start.y == segment.end.y:
            mark(segment, diagram)

def count_overlaps(diagram):
    return len([ visits for visits in diagram.values() if visits > 1 ])

def main(args = ()):
    fileName = "day5.txt" if len(args) < 1 else args[0]
    segments = []

    with open(fileName) as coords:
        for line in coords:
            line = line.strip()
            if not line: continue
            x1, y1, x2, y2 = [ int(n) for n in ",".join(line.split(" -> ")).split(",") ]
            segments.append(Line(Point(x1,y1), Point(x2,y2)))

    part1 = defaultdict(int)
    mark_segments(segments, part1, diagonals=False)
    print("Part 1:", count_overlaps(part1))

    part2 = defaultdict(int)
    mark_segments(segments, part2, diagonals=True)
    print("Part 2:", count_overlaps(part2))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))