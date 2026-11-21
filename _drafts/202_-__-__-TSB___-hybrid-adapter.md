---
layout: post
title: "Mutiplication as a tie-breaker in overload resolution"
date: 202?-??-??
categories: c++
---

More than a decade ago, I got [nerd sniped][xkcd-nerd-sniping] by [Orson Peters][orson-peters] while he was still working on [pattern-defeating quicksort][pdqsort],
and started to learn a bit more about sorting algorithms.
It quickly turned into the most boring project idea anyone could ever come with after such a revelation: creating a library of sorting algorithms.

Instead of making a simple collection thereof, I was interested in finding ways to compose them, and create higher-level algorithms from simpler pieces.
In some aspects it was a success: the library contains sorting adapters (more about that later), [measures of disorder][measures-of-disorder] (TODO: talk about it a lot in this blog), custom comparators, and [metrics][cpp-sort-metrics] used to evaluate different aspects of an algorithm (number of comparisons, etc.).
It comes with some benchmarks, as well as a fairly comprehensive test suite that proved useful on several occasions to identify issues in sorting algorithms from different projects.

The original goal of being able to compose algorithms however was far from a resounding success:
despite various attempts and approaches over time, the related tools in the library manage to be overcomplicated while hard to use, without offering much real power to users.
Several of them 

TODO: mention that the experiment isn't a resounding success, with it becoming a bloated template mess that doesn't actually scale

TODO: today we're gonna focus on one of those template monsters

## Sorters

Influenced by the C++17 [standard library searchers][std-search],
a small collection of function objects that neatly separate the algorithm-specific parameters from the generic ones,
I decided that my library would revolve around the concept of *sorters*, which work roughly as follows:
- A sorter is a function object that encapsulates a sorting algorithm.
- Algorithm-specific parameters can be passed to the constructor of a sorter to parametrize it.
- All sorters follow the *unified sorting interface*, which is fancy wording that says that `operator()` accepts a collection to sort,
  and possibly a comparison function and/or a projection function.

The actual implementation is an absolute mess that tries to do way too much,
so for the rest of this article we wil assume that the *unified sorting interface* is just an `operator()` accepting an iterator/sentinel pair that represent the colleciton to sort.

The following example shows how a simple [counting sort][counting-sort] limited to a given range of values could be implemented:

```cpp
struct counting_sorter
{
private:
    std::int32_t min_, max_;

public:
    counting_sorter(std::int32_t min, std::int32_t max):
        min_(min), max_(max)
    {}
    
    template<
        std::forward_iterator Iterator,
        std::sentinel_for<Iterator> Sentinel
    >
    void operator()(Iterator first, Sentinel last) const
    {
        // Precondition: all the values to sort are in the range [min, max]
        if (first == last) return;

        std::vector<std::int64_t> counts(max_ - min_ + 1, 0);
        for (auto it = first; it != last; ++it) {
            ++counts[*it - min_];
        }

        for (auto count: counts) {
            first = std::fill_n(first, count, min_++);
        }
    }
};
```

A generic counting sort implementation would have to start by traversing the collection once to find the min/max values.
Passing the information to the constructor allows to skip the initial traversal entirely, relying on domain knowledge to save computing time.

We can think of this constructor/`operator()` separation as the philosophical equivalent of a [partial application][partial-application] of the algorithm-specific parameters,
which gives us a sorter with an interface similar to that of [`std::sort`][std-sort],
making it easy to use any sorter as a drop-in replacement for the standard library's routine.

```cpp
int main()
{
    std::vector<int> vec = { 5, 2, 3, 9, 8, 7, 7, 1, 5, 2, 3 }:
    auto sort = counting_sorter(1, 9);
    sort(vec.begin(), vec.end());
    
    // Displays [1, 2, 2, 3, 3, 5, 5, 7, 7, 8, 9]
    std::print("{}", vec);
}
```

## `hybrid_adapter`

Sorters were only the first concept introduced in **cpp-sort** to parametrize algorithm, TODO: sorters parametrization is intrusive
TODO: adapters are the non-intrusive way for transversal concepts, diss Boost.Sort that needs indirect everything

TODO: introduce the idea of adapters

TODO: introduce the idea, take several sorters, make a sorter that can take them all

TODO: introduce whatever code is needed to base it on declaration order alone

TODO: graph with "stack" of priority as is, show what call matches what

## Making iterator categories take priority

TODO: problem, we want to select priority based on iterator category first, then declaration order (illustration, switch heap and merge sorts)

TODO: change priority stack illustration 

TODO: mention that a common trick is multiply(first)+second

TODO: new table with holes

## Granular overload resolution

TODO: mention `choice`, link to Flaming Dangerzone article

TODO: `Sorter::iterator_category` mapping

TODO: bind it all together

## Bonus: reducing instantiations

TODO: whatever's needed for the current computation used for `choice`

## Conclusion

TODO: not a great component, but funny and a good demonstration

TODO: might talk about other aspects of hybrid_adapter in subsequent articles

## Notes

  [^1]: TODO


  [adapters]: TODO:<codeberg>
  [counting-sort]: https://en.wikipedia.org/wiki/Counting_sort
  [cpp-sort]: TODO:<codeberg>
  [cpp-sort-metrics]: TODO:<codeberg>
  [measures-of-disorder]: :<codeberg>
  [orson-peters]: https://orlp.net/
  [overload-ranking]: https://web.archive.org/web/20150726012823/http://flamingdangerzone.com/cxx11/overload-ranking/
  [partial-application]: https://en.wikipedia.org/wiki/Partial_application
  [pdqsort]: https://github.com/orlp/pdqsort
  [sorters]: TODO:<codeberg>
  [std-search]: https://en.cppreference.com/w/cpp/algorithm/search.html
  [std-sort]: https://cppreference.com/w/cpp/algorithm/sort.html
  [xkcd-nerd-sniping]: https://xkcd.com/356/
