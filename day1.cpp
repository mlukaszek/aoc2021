#include <iostream>
#include <fstream>
#include <vector>
#include <numeric>

using namespace std;
using Vector = vector<int>;

int part1(Vector& numbers)
{
    int previous = 0;
    unsigned larger = 0;
    for (auto number : numbers) {
        if (previous && number > previous) {
            larger++;
        }
        previous = number;
    }
    return larger;
}

int part2(Vector& numbers)
{
    Vector sums;
    Vector::const_iterator begin, end;
    constexpr auto windowSize = 3;
    for (begin = numbers.begin(), end = begin + windowSize; end != numbers.end(); begin++, end++) {
        sums.push_back(accumulate(begin, end, 0));
    }
    return part1(sums);
}

int main(int argc, char* argv[])
{
    ifstream input;
    input.open(argc < 2 ? "day1.txt" : argv[1], ifstream::in);

    Vector numbers;
    int number;
    while (input.good()) {
        input >> number;
        numbers.push_back(number);
    }

    cout << "Part 1: " << part1(numbers) << "\n";
    cout << "Part 2: " << part2(numbers) << "\n";
}