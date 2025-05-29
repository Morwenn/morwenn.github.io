---
layout: post
title: "Cartesian tree sort"
date: 2021-03-21
categories: sorting, c++
---

*Cartesian tree sort* is an unstable comparison sort first proposed by C. Levcopoulos and O. Petersson in *Heapsort - Adapted for Presorted Files*. It is from a time when research on adaptive sorting was prolific and the very concept of adaptive sorting was being formalized (TODO: manilla).

This sorting algorithm sorts in linear time when it encounters specific patterns with a high presortedness, and gracefully degrades to O(n log n) as the presortedness in the collection to sort decreases. A simple implementation allocates a Cartesian tree and a priority queue, making it run in O(n) space.

## Description of the algorithm

### Cartesian tree

Quoting Wikipedia:

> A Cartesian tree is a binary tree derived from a sequence of elements: it can be uniquely defined from the properties that it is heap-ordered and that a symmetric (in-order) traversal of the tree returns the original sequence.

TODO: latex graph

What makes Cartesian trees interesting in the realm of sorting is that they can be constructed in linear time and that they have the heap property.

### Cartesian tree sort

Cartesian tree sort can be tersely resumed in a few steps:
* Create a Cartesian tree from the collection to sort.
* Initialize a priority queue with the root of the Cartesian tree.
* While the priority is not empty:
  * Remove the top of the priority queue and add it back to the original collection.
  * Add the children of the removed elements to the priority queue.

TODO: show example of almost-sorted Cartesian tree

## Implementing the algorithm in C++

Since Cartesian tree sort is a comparison sort, we can use a similar interface to that of `std::ranges::sort`, fully conceptified with support for iterator, sentinels and ranges:

{% highlight cpp %}
template<
    std::random_access_iterator Iterator,
    std::sentinel_for<Iterator> Sentinel,
    typename Compare = std::ranges::less,
    typename Projection = std::identity
>
    requires std::sortable<Iterator, Compare, Projection>
auto cartesian_tree_sort(Iterator first, Sentinel last, Compare comp={}, Projection proj={})
    -> Iterator;

template<
    std::ranges::random_access_range Range,
    typename Compare = std::ranges::less,
    typename Projection = std::identity
>
    requires std::sortable<std::ranges::iterator_t<Range>, Compare, Projection>
auto cartesian_tree_sort(Range&& range, Compare comp={}, Projection proj={})
    -> std::ranges::borrowed_iterator_t<Range>
{
    return cartesian_tree_sort(
        std::ranges::begin(range), std::ranges::end(range),
        std::move(comp), std::move(proj)
    );
}
{% endhighlight %}

Technically we could require forward iterator instead of random-access ones since the elements will be moved from the collection to the Cartesian tree and back to it with a linear access pattern. We will analyze this possibility later in the article.

### Representing the Cartesian tree

{% highlight cpp %}
#include <algorithm>

template<typename T>
struct tree_node
{
    T value;
};
{% endhighlight %}

### Building the Cartesian tree

TODO: mention Wikipedia algo

> One method is to simply process the sequence values in left-to-right order, maintaining the Cartesian tree of the nodes processed so far, in a structure that allows both upwards and downwards traversal of the tree. To process each new value *x*, start at the node representing the value prior to *x* in the sequence and follow the path from this node to the root of the tree until finding a value *y* smaller than *x*. The node *x* becomes the right child of *y*, and the previous right child of *y* becomes the new left child of *x*. 

### Sorting with a priority queue

## Optimizing the algorithm

### Better priority queue

TODO: Arthur O'Dwyer article about `replace_top`

### Dropping some back-pointers

## Going further

TODO: immutable nodes, static buffer instead of vector, other tree construction methods, generalized callables, forward iterators

