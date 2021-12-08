import sys

def count1478(output):
    lengths =  [ len(digit) for digit in output ]
    return len([ matching for matching in lengths if matching in (2,3,4,7) ])

def count_common_segments(a, b):
    return len([ segment for segment in a if segment in b])

def learn_code(segmentsGroups):
    code = {}
    segmentsGroups = [ "".join(sorted(segments)) for segments in segmentsGroups ]

    while len(code.keys()) < 10:
        for segments in segmentsGroups:
            length = len(segments)
            if length == 2:
                code[1] = segments
            elif length == 3:
                code[7] = segments
            elif length == 4:
                code[4] = segments
            elif length == 7:
                code[8] = segments
            elif length == 6: # 0, 6 or 9
                if 1 not in code or 4 not in code: # need those first
                    continue
        
                commonWithOne = count_common_segments(segments, code[1])
                if 2 == commonWithOne: # 0 or 9
                    if 4 == count_common_segments(segments, code[4]):
                        code[9] = segments
                    else:
                        code[0] = segments
                else: # must be 6
                    code[6] = segments
            elif length == 5: # 2, 3 or 5
                if 1 not in code or 4 not in code: # need those first
                    continue

                commonWithFour = count_common_segments(segments, code[4])
                if 3 == commonWithFour: # 3 or 5
                    if 2 == count_common_segments(segments, code[1]):
                        code[3] = segments
                    else:
                        code[5] = segments
                else: # must be 2
                    code[2] = segments
    return code

def decode_output(output, code):
    multiplier = 1
    result = 0
    segmentsToNumber = { value:key for key, value in code.items() }
    for digit in reversed(output):
        segments = "".join(sorted(digit))
        result += multiplier * segmentsToNumber[segments]
        multiplier *= 10
    return result

def main(args = ()):
    fileName = "day8.txt" if len(args) < 1 else args[0]

    part1 = 0
    outputs = []
    with open(fileName) as lines:
        for line in lines:
            before, after = line.strip().split(" | ")
            patterns = before.split(" ")
            output = after.split(" ")
            part1 += count1478(output)

            code = learn_code(patterns + output)
            outputs.append(decode_output(output, code))

    print("Part 1:", part1)
    print("Part 2:", sum(outputs))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))