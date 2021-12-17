import sys
from re import findall
from dataclasses import dataclass

@dataclass
class Point:
    x: int = 0
    y: int = 0

def shoot(target, vx, vy):
    probe = Point()
    highest = -(sys.maxsize - 1)

    hit = False
    while probe.x <= target.br.x and probe.y >= target.br.y:
        probe.x += vx
        probe.y += vy
        vx = max(0, vx-1)
        vy -= 1
        highest = max(highest, probe.y)
        if hit := (probe in target):
            break
    return hit, highest

def highest_position_of_good_shots(target):
    # Just brute force the combinations, don't have time to do the math...
    for vx in range(1, target.br.x + 1):
        for vy in range(target.br.y, -target.br.y + 1):
            good, highest = shoot(target, vx, vy)
            if good:
                yield highest

class Rect(object):
    def __init__(self, ranges) -> None:
        self.tl = Point()
        self.br = Point()
        self.tl.x, self.br.x, self.br.y, self.tl.y = ( int(i) for i in findall(r"-?\d+", ranges) )

    def __contains__(self, point):
        return self.tl.x <= point.x <= self.br.x and self.br.y <= point.y <= self.tl.y

def main(args = ()):
    fileName = "day17.txt" if len(args) < 1 else args[0]

    with open(fileName) as lines:
        target = Rect(lines.readline().strip())

    heights = list(highest_position_of_good_shots(target))

    print(f"Best shot has y =", max(heights))
    print(len(heights), "combinations hit the target")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))