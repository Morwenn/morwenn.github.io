---
layout: post
title: "Destructive in-order tree traversal with at most 2N node visitations"
date: 2025-05-08
categories: algorithms
---

A few years ago, I decided to implement [splaysort][splaysort] in my sorting algorithms library, [cpp-sort][cpp-sort].
The algorithm turned out to be deceiptively simple from a high-level point of view:

1. Insert all elements to sort into a [splay tree][splay-tree] (a kind of [self-balancing binary search tree][self-balancing-tree]).
2. Perform [in-order traversal][inorder-traversal] on the tree to move elements back to the original collection in sorted order.

It is basically just a [tree sort][tree-sort], which benefits from the ability of splay trees to gracefully adapt to the existing order in a sequence.

TODO: illustration with a splay tree

This article is not really about splaysort, not even about tree sorts: it is about in-order traversal.

## In-order traversal in its simplest form

Visiting a binary search tree in-order is most easily explained through the recursive definition of the algorithm to visit a node:

1. Recursively visit the node's left child if any
2. Visit the current node (in our case, move the value back to the original collection)
3. Recursively visit the node's right child if any

It is perhaps even clearer when compared to pre-order and post-order traversals:

<table>
<tr>
<td> pre-order </td> <td> in-order </td> <td> post-order </td>
</tr>
<tr>
<td> 200 </td>
<td>
    
```
func pre-order(node):
    visit(node)
    pre-order(left-child)
    pre-order(right-child)
}
```

</td>
<td>
    
```
func in-order(node):
    in-order(left-child)
    visit(node)
    in-order(right-child)
}
```

</td>
<td>
    
```
func post-order(node):
    post-order(left-child)
    post-order(right-child)
    visit(node)
}
```

</td>
</tr>
</table>

If we start such traversal with the root node, we can move all values back to the original collection in sorted order,
thanks to the fundamental property of binary search tree: left children have a smaller value than the current node, right children have a greater value.

TODO: illustration of the visitation

## C++ recursive implementation

We're gonna use the following `node` type to implement in-order traversal in C++:

```cpp
template<std::movable T>
struct node
{
    T value;
    node* parent;
    node* left;
    node* right;
};
```

The recursive traversal function moving values out of our tree and into an output iterator looks like this:

```cpp
template<std::movable T, std::output_iterator Iterator>
void move_to(node<T>* node, Iterator& out)
{
    if (node == nullptr) return;
    move_to(node->left, out);
    *out++ = std::move(node->value);
    move_to(node->right, out);
}
```

So far we got a beautifully simple algorithm, call it on the root and it moves your whole tree away, which is exacty what we want.

## C++ iterative implementation

Technically the recursive version of in-order traversal is enough for our use case: we are using a splay tree, which is self-balancing, so its depth should never exceed $O(log n)$.
Non-balancing trees can become degenerate, forcing one to dive down through $O(n)$ layers, potentially blowing the stack, though that simply can't happen to us.
I could have stopped there, but I wanted to implement an iterative tree traversal, and it turns out that there are [lots of different ways][inorder-impl-wikipedia] to do that.
Many of those either use a stack of nodes to mimick recursion, or use more involved alternatives such as Morris [threaded binary tree][threaded-tree] in-order traversal.

As much as possible I didn't want to allocate additional memory, and threading a binary seemed complicated at the time.
Fortunately I had a considerable advantage up my sleeve: parent pointers! Splaying operations often involve following parent nodes, which make such a traversal much easier.
Though I was still a lazy bum, and instead of trying to come up with a smart solution, I did what most millenials do when faced with such an exciting challenge:
[copy-pasting some code from StackOverflow][inorder-impl-stackoverflow].

```cpp
void in_order_traversal_iterative_with_parent(node* root) {
node* current = root;
node* previous = NULL;

while (current) {
    if (previous == current->parent) { // Traversing down the tree.
        previous = current;
        if (current->left) {
            current = current->left;
        } else {
            cout << ' ' << current->data;
            if (current->right)
                current = current->right;
            else
                current = current->parent;
        }
    } else if (previous == current->left) { // Traversing up the tree from the left.
        previous = current;
        cout << ' ' << current->data;
        if (current->right)
            current = current->right;
        else
            current = current->parent;
    } else if (previous == current->right) { // Traversing up the tree from the right.
        previous = current;
        current = current->parent;
    }
}

cout << endl;
}
```

That piece of C++ code is the work of StackOverflow user @OmarOthman, based on a previous answer by @svick.
The algorithm revolves around the fact that knowing where we come from is enough to know where we need to go next:
1. If we come from the parent node, it is our first node visit, we go left if possible.
2. If we come from the left child node, our next target is the right node.
3. If we come from the right node, all we can do is bubble up to the parent node.

In all of those steps, if our next target is null, we behave *as if* we were in the subsequent state.
Interestingly enough, that "fallback behavior" shows better with a few labels and `goto`:

```cpp
template<std::movable T, std::output_iterator Iterator>
void move_to(node<T>* root, Iterator out)
{
    node<T>* current = root;
    node<T>* previous = nullptr;

    while (current) {
        if (previous == current->parent) {
            goto from_parent;
        } else if (previous == current->left) {
            goto from_left;
        } else if (previous == current->right) {
            goto from_right;
        }
        
        from_parent:
            if (current->left) {
                previous = std::exchange(current, current->left);
                continue;
            }
        from_left:
            *out++ = std::move(current->value);
            if (current->right) {
                previous = std::exchange(current, current->right);
                continue;
            }
        from_right:
            previous = std::exchange(current, current->parent);
    }
}
```

For a tree with $n$ nodes, this algorithm's main loop considers is executed $2n$ times:
* Every node is considered once in the initial "going down" phase, which leads to $n$ loops.
* When "going up" after visitation, every node picks its parent as the next node, which gives another $n$ loops.

This number of loops is independent of the data in the tree, and of whether the tree is balanced or not.
This actually reflects what happens in the recursive implementation,
where every function call has control when first reached, then again after the recursive calls return to it.
And that no surprise: the labelled sections in this sequential implementation correspond to where control would resume in the recursive implementation after a recursive call.

The question is now: can we do better without introducing additional pointers, recursion, or stack space?

## Grandma's delicious `goto` soup

This article is already going places it was never supposed to, so I'm just gonna double down on the `goto` soup and have fun trying to iteratively rewrite and prune parts of it.
Let's start right away with a few observations:
1. The first `previous == current->parent` is redundant: if the two following checks fail, then we naturally reach `from_parent:`.
2. The first very first loop satisfies the `from_parent` criterion, we can jump there directly.
3. When visiting a left child, the first thing we want to do is to recursively find another left child. We can skip a few conditions by introducing a tight loop.
4. When visiting a right child, we know that we will come from the parent node in the following loop, we can jump there directly. 

Putting it all together, we get the following modified version of the algorithm:


```cpp
template<std::movable T, std::output_iterator Iterator>
void move_to(node<T>* root, Iterator out)
{
    node<T>* current = root;
    node<T>* previous = nullptr;

    goto from_parent; // (2)
    while (current) {
        // (1) removed (previous == current->parent) condition
        if (previous == current->left) {
            goto from_left;
        } else if (previous == current->right) {
            goto from_right;
        }
        
        from_parent:
            while (current->left) { // (3)
                previous = std::exchange(current, current->left);
            }
        from_left:
            *out++ = std::move(current->value);
            if (current->right) {
                previous = std::exchange(current, current->right);
                goto from_parent; // (4)
            }
        from_right:
            previous = std::exchange(current, current->parent);
    }
}
```

All that tinkering changes nothing to the number of nodes that have to be considered at any given moment by the algorithm, which remains $2n$.
However it effectively reuses knowledge about the algorithm flow to reduce the number of conditions perform during a traversal.
Amazingly enough, experimental data shows that the number of conditions seems independent of data, with $6n$ conditions for the previous version, and $4n$ for the new one.

TODO: numbers of conditions
TODO: benchmark

## Destructive iterative traversal

As you can guess, I didn't start a blog post just to present someone else's code, as good as it may be.


TODO: We don't need the tree after the traversal, so we can afford to alter it
present idea: rewrite nodes YOLO

more CODE

some analysis, comparison to existing threading?

boite à moustache, comparisons of iterations


  [cpp-sort]: 
  [inorder-impl-stackoverflow]: https://stackoverflow.com/a/10380373/1364752
  [inorder-impl-wikipedia]: https://en.wikipedia.org/wiki/Tree_traversal#In-order_implementation
  [inorder-traversal]: https://en.wikipedia.org/wiki/Tree_traversal#Reverse_in-order,_RNL
  [self-balancing-tree]: https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree
  [splay-tree]: https://en.wikipedia.org/wiki/Splay_tree
  [splaysort]: https://en.wikipedia.org/wiki/Splaysort
  [threaded-tree]: https://en.wikipedia.org/wiki/Threaded_binary_tree
  [tree-sort]: https://en.wikipedia.org/wiki/Tree_sort
