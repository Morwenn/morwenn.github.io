#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <unordered_map>
#include <vector>
#include <cpp-sort/probes/amp.h>

int main()
{
    int input_size = 10;
    //for (int input_size: {4, 5, 6, 7, 8, 9, 10, 11}) {
        std::vector<int> counts(cppsort::probe::amp.max_for_size(input_size) + 2, 0);

        std::vector<int> sequence(input_size, 0);
        std::iota(sequence.begin(), sequence.end(), 0);

        do {
            auto amp = cppsort::probe::amp(sequence);
            counts[amp] += 1;
        } while (std::ranges::next_permutation(sequence).found);

        std::vector<int> below_n;
        std::partial_sum(counts.begin(), counts.end(), std::back_inserter(below_n));

        std::cout << "below\tnumber\n";
        int index = 0;
        for (int value: counts) {
            std::cout << index << '\t' << value << '\n';
            ++index;
        }
        //std::cout << input_size << '\t' << counts[2] << '\n';
    //}
}
