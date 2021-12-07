#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

using Command = pair<string, int>;
using Commands = vector<Command>;

long part1(Commands& commands)
{
    int position = 0;
    int depth = 0;
    for (auto& command : commands) {
        if (command.first == "forward") {
            position = position + command.second;
        } else if (command.first == "down") {
            depth = depth + command.second;
        } else if (command.first == "up") {
            depth = depth - command.second;
        }
    }
    return position * depth;
}

long part2(Commands& commands)
{
    int position = 0;
    int aim = 0;
    long depth = 0;
    for (auto& command : commands) {
        if (command.first == "forward") {
            position = position + command.second;
            depth = depth + (aim * command.second);
        } else if (command.first == "down") {
            aim = aim + command.second;
        } else if (command.first == "up") {
            aim = aim - command.second;
        }
    }
    return position * depth;
}


int main(int argc, char* argv[])
{
    ifstream input;
    input.open(argc < 2 ? "day2.txt" : argv[1], ifstream::in);

    Commands commands;
    string direction;
    int distance;

    while (input.good()) {
        input >> direction >> distance;
        if (!input.good()) break; // account for an incomplete input, e.g. a blank line
        Command command(direction, distance);
        commands.push_back(command);
    }

    cout << "Part 1: " << part1(commands) << "\n";
    cout << "Part 2: " << part2(commands) << "\n";
}