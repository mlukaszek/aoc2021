import sys
from collections import defaultdict
from tqdm import trange

DARK = 0
LIGHT = 1
BORDER = 2

def lookup(i, j, bits, algorithm):
    num = bits[(i-1,j-1)] << 8 \
        | bits[(i,j-1)] << 7 \
        | bits[(i+1,j-1)] << 6 \
        | bits[(i-1,j)] << 5 \
        | bits[(i,j)] << 4 \
        | bits[(i+1,j)] << 3 \
        | bits[(i-1,j+1)] << 2 \
        | bits[(i,j+1)] << 1 \
        | bits[(i+1,j+1)]
    return 1 if algorithm[num] == "#" else 0, num

def bounds(image):
    minX = min( i for i, _ in image )
    minY = min( j for _, j in image )
    maxX = max( i for i, _ in image )
    maxY = max( j for _, j in image )
    return minX, minY, maxX, maxY

def enhance(image, algorithm, step):
    minX, minY, maxX, maxY = bounds(image) # this should be more clever, it slows things down. oh well
    result = defaultdict(lambda: LIGHT if algorithm[0 if step % 2 == 0 else 0x1FF] == "#" else DARK)
    for j in range(minY - BORDER, maxY+1 + BORDER):
        for i in range(minX - BORDER, maxX+1 + BORDER):
            result[(i,j)], _ = lookup(i, j, image, algorithm)
    return result

def main(args = ()):
    fileName = "day20.txt" if len(args) < 1 else args[0]

    algoritm = ""
    image = defaultdict(lambda: DARK)
    with open(fileName) as lines:
        algoritm = lines.readline().strip()
        assert "" == lines.readline().strip()
        for j, line in enumerate(lines):
            for i, pixel in enumerate(line):
                if "#" == pixel:
                    image[(i, j)] = LIGHT

    for step in trange(50):
        image = enhance(image, algoritm, step)

    print(f"\nPixels lit after enhancing {step+1} times:")
    print(len([ pixel for pixel in image.values() if pixel ]))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))