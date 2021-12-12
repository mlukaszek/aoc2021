import sys
from collections import defaultdict

class Path(object):
    def __init__(self, nodes, canVisitTwice=True) -> None:
        self.nodes = nodes
        self.canVisitTwice = canVisitTwice

def count_paths(connections, part2=False):
    paths = [ Path(["start"]) ]
    total = 0
    
    while paths:
        path = paths.pop()
        lastNode = path.nodes[-1]
        for cave in connections[lastNode]:
            if cave == "end":
                total += 1
            elif part2 and cave == "start":
                continue                
            elif cave not in path.nodes or cave.isupper(): # first visit, or a large cave
                paths.append( Path(path.nodes + [cave], path.canVisitTwice) )
            elif part2 and path.canVisitTwice: # a small cave visited twice in this path, allow no more
                paths.append( Path(path.nodes + [cave], False) )
    return total

def main(args = ()):
    fileName = "day12.txt" if len(args) < 1 else args[0]

    connections = defaultdict(list)
    with open(fileName) as lines:
        for edge in lines:
            edge = edge.strip()
            if edge:
                a, b = edge.split("-")
                connections[a].append(b)
                connections[b].append(a)

    print("Part 1:", count_paths(connections))
    print("Part 2:", count_paths(connections, True))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))