import sys
from dataclasses import dataclass
from itertools import accumulate, combinations

@dataclass
class Element:
    depth: int
    value: int

class SnailfishNumber(object):
    def __init__(self, line = ""):
        self.elements = []
        depth = 0
        for c in line:
            try:
                self.elements.append(Element(depth, int(c)))
            except ValueError:
                depth += {",":0, "[":1, "]":-1}[c]

    def _explode(self):
        for i, element in enumerate(self.elements):
            if element.depth > 4:
                if i > 0:
                    self.elements[i - 1].value += element.value
                if i < len(self.elements) - 2:
                    self.elements[i + 2].value += self.elements[i + 1].value
                self.elements[i:i+2] = [ Element(element.depth - 1, 0) ]
                return True

    def _split(self):
        for i, element in enumerate(self.elements):
            if element.value > 9:
                depth = element.depth + 1
                lower = element.value // 2
                self.elements[i:i+1] = [ Element(depth, lower), Element(depth, element.value - lower) ]
                return True
                
    def reduce(self):
        while True:
            if not self._explode() and not self._split():
                break

    def magnitude(self) -> int:
        result = self.elements
        finished = False
        while not finished:
            for i, element in enumerate(result):
                finished = True
                if i+1 < len(result) and element.depth == result[i+1].depth:
                    result[i:i+2] = [ Element(element.depth - 1, 3 * element.value + 2 * result[i+1].value) ]
                    finished = False
                    break
        return result[0].value

    def __add__(self, other):
        result = SnailfishNumber()
        result.elements = [ Element(element.depth + 1, element.value) for element in self.elements + other.elements ]
        result.reduce()
        return result

def main(args = ()):
    fileName = "day18.txt" if len(args) < 1 else args[0]

    numbers = []
    with open(fileName) as lines:
        numbers = [ SnailfishNumber(line.strip()) for line in lines ]

    part1 = accumulate(numbers)
    print("Part 1:", list(part1)[-1].magnitude())

    part2 = 0
    for a,b in combinations(numbers, 2):
        part2 = max(part2, (a + b).magnitude(), (b + a).magnitude())
    print("Part 2:", part2)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))