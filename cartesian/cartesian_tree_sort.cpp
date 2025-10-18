/*
 * Copyright (c) 2021 Morwenn
 * SPDX-License-Identifier: BSL-1.0
 */
#include <functional>
#include <iterator>
#include <queue>
#include <ranges>
#include <utility>
#include <vector>

template<typename T>
struct tree_node
{
    constexpr tree_node(T&& value, tree_node* parent, tree_node* left_child)
        noexcept(std::is_nothrow_move_constructible<T>::value):
        value(std::move(value)),
        parent(parent),
        left_child(left_child)
    {}

    // Tree nodes are move-only
    tree_node(const tree_node&) = delete;
    tree_node(tree_node&&) = default;
    tree_node& operator=(const tree_node&) = delete;
    tree_node& operator=(tree_node&&) = default;

    // Stored value
    T value;

    // Parent node
    tree_node* parent = nullptr;
    // Children nodes
    tree_node* left_child = nullptr;
    tree_node* right_child = nullptr;
};

template<
    std::random_access_iterator Iterator,
    std::sentinel_for<Iterator> Sentinel,
    typename Compare = std::ranges::less,
    typename Projection = std::identity
>
    requires std::sortable<Iterator, Compare, Projection>
auto cartesian_tree_sort(Iterator first, Sentinel last, Compare comp={}, Projection proj={})
    -> Iterator
{
    using node_type = tree_node<std::iter_value_t<Iterator>>;

    auto size = last - first;
    if (size < 2) {
        return first + size;
    }

    ////////////////////////////////////////////////////////////
    // Make a Cartesian tree

    // Create a vector with just the right size to ensure that it
    // won't get resized and that iterators won't be invalidated
    std::vector<node_type> cartesian_tree;
    cartesian_tree.reserve(size);

    // Create the first node
    cartesian_tree.emplace_back(std::ranges::iter_move(first), nullptr, nullptr);

    // Root of the Cartesian tree
    node_type* root = &cartesian_tree.back();

    for (auto it = std::next(first); it != last; ++it) {
        // Find where to insert the current node
        auto&& proj_value = proj(*it);
        node_type* new_node_parent = &cartesian_tree.back();
        while (comp(proj_value, proj(new_node_parent->value))) {
            if (new_node_parent == root) {
                new_node_parent = nullptr;
                break;
            }
            new_node_parent = new_node_parent->parent;
        }

        // Insert the node
        if (new_node_parent == nullptr) {
            cartesian_tree.emplace_back(std::ranges::iter_move(it), nullptr, root);
            root = &cartesian_tree.back();
        } else {
            cartesian_tree.emplace_back(std::ranges::iter_move(it), new_node_parent, new_node_parent->right_child);
            new_node_parent->right_child = &cartesian_tree.back();
        }
    }

    ////////////////////////////////////////////////////////////
    // Sort the Cartesian tree with a priority queue

    auto pq_comp = [&comp, &proj](auto* lhs, auto* rhs) {
        return comp(proj(rhs->value), proj(lhs->value));
    };
    std::priority_queue<node_type*, std::vector<node_type*>, decltype(pq_comp)> pq(pq_comp);
    pq.push(root);

    while (not pq.empty()) {
        // Retrieve biggest element
        node_type* node = pq.top();
        pq.pop();

        // Add the element back to the original collection
        *first = std::move(node->value);
        ++first;

        // Add the node's children to the priority queue
        if (node->left_child != nullptr) {
            pq.push(node->left_child);
        }
        if (node->right_child != nullptr) {
            pq.push(node->right_child);
        }
    }

    return first;
}

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


#include <algorithm>
#include <cassert>
#include <numeric>
#include <experimental/algorithm>

int main()
{
    std::vector<int> vec(500);
    std::iota(vec.begin(), vec.end(), 0);
    std::experimental::shuffle(vec.begin(), vec.end());

    cartesian_tree_sort(vec);
    assert(std::ranges::is_sorted(vec));
}
