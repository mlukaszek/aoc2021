#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <bitset>
#include <algorithm>
#include <functional>

using namespace std;

constexpr auto BITS = 12;
using Report = bitset<BITS>;
using Reports = vector<Report>;

std::pair<int,int> count_ones_and_zeros(Reports& reports, int bit)
{
    int zeros = 0;
    int ones = 0;

    for (auto& report : reports) {
        if (report.test(bit)) {
            ones++;
        } else {
            zeros++;
        }
    }
    return make_pair(ones, zeros);
}

Report get_gamma(Reports& reports)
{
    Report gamma = 0;

    for (auto bit = 0; bit < BITS; bit++) {
        auto [ ones, zeros ] = count_ones_and_zeros(reports, bit);
        gamma[bit] = (ones > zeros);
    }
    return gamma;
}

long part1(Reports& reports)
{
    Report gamma = get_gamma(reports);
    Report epsilon = ~gamma;
    
    return gamma.to_ulong() * epsilon.to_ulong();
}

long get_rating(Reports& reports, std::function<int(int ones, int zeros)> value_to_keep_provider)
{
    Reports answer = reports;
    for (auto bit = BITS-1; bit >= 0 && answer.size() > 1; bit--) {
        auto [ ones, zeros ] = count_ones_and_zeros(answer, bit);
        if (ones == 0 && answer.size() == reports.size()) continue; // skip leading zeros
        
        int keep = value_to_keep_provider(ones, zeros);
        answer.erase(remove_if(answer.begin(), answer.end(), [&](Report& report) {
            return report.test(bit) != keep;
        }), answer.end());
    }
    return answer[0].to_ulong();
}

long part2(Reports& reports)
{
    long oxygen = get_rating(reports, [](int ones, int zeros) {
        return (ones >= zeros) ? 1 : 0;
    });

    long co2 = get_rating(reports, [](int ones, int zeros) {
        return (zeros <= ones) ? 0 : 1;
    });

    return oxygen * co2;
}

int main(int argc, char* argv[])
{
    ifstream input;
    input.open(argc < 2 ? "day3.txt" : argv[1], ifstream::in);

    Reports reports;

    string line;
    while (input.good()) {
        input >> line;
        if (!input.good()) break; // account for an incomplete input, e.g. a blank line
        reports.push_back(Report(line));
    }

    cout << "Part 1: " << part1(reports) << "\n";
    cout << "Part 2: " << part2(reports) << "\n";
}