#include <algorithm>
#include <format>
#include <iterator>
#include <numeric>
#include <print>
#include <ranges>
#include <unordered_map>
#include <vector>
#include <cpp-sort/probes.h>

int main()
{
    using difference_t = std::vector<int>::difference_type;
    enum OutputType {
        BELOW_SET,
        EQUAL_SET,
    };

    // Script parameters
    auto measure = cppsort::probe::sus;
    char const* measure_name = "SUS";
    constexpr OutputType output_type = EQUAL_SET;
    constexpr difference_t max_input_size = 10;

    // Write CSV header
    std::println(
        "|X| / {}(X),{:n}",
        measure_name,
        std::views::iota(
            difference_t(0),
            measure.max_for_size(max_input_size) + 1
        )
    );

    for (int input_size: std::views::iota(0, max_input_size + 1)) {
        std::vector<int> counts(measure.max_for_size(input_size) + 1, 0);

        std::vector<int> sequence(input_size, 0);
        std::ranges::iota(sequence, 0);
        do {
            auto disorder = measure(sequence);
            counts[disorder] += 1;
        } while (std::ranges::next_permutation(sequence).found);

        if constexpr (output_type == BELOW_SET) {
            std::partial_sum(counts.begin(), counts.end(), counts.begin());
        }

        std::println("{},{:n}", input_size, counts);
    }
}
