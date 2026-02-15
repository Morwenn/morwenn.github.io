#include <algorithm>
#include <cassert>
#include <chrono>
#include <format>
#include <forward_list>
#include <functional>
#include <iostream>
#include <iterator>
#include <list>
#include <numeric>
#include <random>
#include <ranges>
#include <vector>
#include <cpp-sort/sorters/splay_sorter.h>

int main()
{
    int seed = 123456;
    std::minstd_rand engine(seed);

    for (int i = 0; i < 1000; ++i) {
        std::vector<int> vec(50'000);
        std::iota(vec.begin(), vec.end(), 0);
        std::shuffle(vec.begin(), vec.end(), engine);

        cppsort::splay_sort(vec);
        assert(std::is_sorted(vec.begin(), vec.end()));
    }
}
