import sys
import logging
from math import prod

LITERAL = 4

class Packet(object):
    def __init__(self, version, type, bits) -> None:
        self.version = version
        self.type = type
        self.bits = bits

    def value(self):
        raise NotImplementedError

class Literal(Packet):
    def __init__(self, version, bits) -> None:
        super().__init__(version, LITERAL, bits)
        self._value = self._parse()
        logging.debug(f"Literal value {self._value}")

    def _parse(self):
        v = 0
        while True:
            more = self.bits.read()
            group = self.bits.read(4)
            v <<= 4
            v |= group
            if not more:
                return v
    
    def value(self):
        return self._value

class Operator(Packet):
    def __init__(self, version, type, bits) -> None:
        super().__init__(version, type, bits)

        self.operands = []
        if self.bits.read():
            length = self.bits.read(11)
            logging.debug(f"Operator with {length} following sub-packets:")
            for _ in range(length):
                self.operands.append(parse(self.bits))
        else:
            length = self.bits.read(15)
            logging.debug(f"Operator with {length} bits in following sub-packets:")
            end = self.bits.tell() + length
            while self.bits.tell() < end:
                self.operands.append(parse(self.bits))

    def value(self):
        logging.debug("Operation: " + ("+", "*", "min", "max", None, ">", "<", "==")[self.type])
        logging.debug(f"Operands: {self.operands}")

        result = int((
            sum,
            prod,
            min, 
            max,
            None,
            lambda args: args[0] > args[1],
            lambda args: args[0] < args[1],
            lambda args: args[0] == args[1]
        )[self.type](self.operands))

        logging.debug(f"Returning {result}")
        return result

class BitStream(object):
    def __init__(self, data) -> None:        
        self.bits = "".join([ f"{int(c, 16):04b}" for c in data.strip() ])
        self.playhead = 0
        self.versionCounter = 0

    # Read bits like from tape, moving the playhead.
    def read(self, numBits=1):
        value = self.bits[self.playhead:self.playhead + numBits]
        self.playhead += numBits
        return int(value, 2)

    def tell(self):
        return self.playhead

def parse(bits):
    V, T = bits.read(3), bits.read(3)
    bits.versionCounter += V
    logging.debug(f"@ {bits.tell()}, V {V} T {T}: ")

    packet = Literal(V,bits) if T == LITERAL else Operator(V,T,bits)
    return int(packet.value())

def main(args = ()):
    fileName = "day16.txt" if len(args) < 1 else args[0]

    bits = None
    with open(fileName) as lines:
        bits = BitStream(lines.readline())

    result = parse(bits)
    print("Sum of versions:", bits.versionCounter)
    print("Final result:", result)

if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    sys.exit(main(sys.argv[1:]))