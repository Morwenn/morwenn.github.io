---
layout: post
title: "A new measure of presortedness: Amp"
date: 2025-05-08
categories: sorting
---

During the 80s, after decades of trying to find better sorting algorithms, some computer scientists started to formalize the concept of *adaptive sorting*,
that is, sorting algorithms designed to take advantage of the existing order in a sequence of elements. This article is not about adaptive sorting algorithms.

This article is about the underlying notion of presortedness. When asked "what does it mean to have existing order? How can we _measure_ it?", different authors came with different propositions:
* The number of inversions in a sequence.
* The distance between elements and their sorted position.
* The number of groups of pre-sorted subsequences.
* The number of cycles of swaps needed to sort a sequence.
* The size of the longest ascending subsequence.

It felt like a useful starting point, but once again a bit blurry and ad-hoc.
Recognizing that issue, Heikki Mannila decided to formalize that a bit and published *Measures of presortedness and optimal sorting algorithms* in 1985, which brings a formal definition of *measures of presortedness*,
describing the expected properties of functions meant to measure the existing order in a collection of elements—and also a formal definition of what an adaptive sort is, but once again this article isn't about that.
The original description is a bit of a mouthful, fortunately Marcello La Rocca1 and Domenico Cantone provide a more concise definition in [*NeatSort - A practical adaptive algorithm*][neatsort]:

> Given two sequences $$X$$ and $$Y$$ of distinct elements, a measure of disorder $$M$$ is a function that satisfies the following properties:
>
> 1. If $$X$$ is sorted, then $$M(X) = 0$$
> 2. If $$X$$ and $$Y$$ are order isomorphic, then $$M(X) = M(Y)$$
> 3. If $$X$$ is a subsequence of $$Y$$, then $$M(X) \le M(Y)$$
> 4. If every element of $$X$$ is smaller than every element of $$Y$$, then $$M(XY) \le M(X) + M(Y)$$
> 5. $$\forall x \in \mathbb{N} : M(\langle x \rangle X) \le |X| + M(X)$$

We're going to look back at those points more in-depth later, once we have introduced our own potential measure.
Just a side note before moving on: I'm gonna keep using the term *measure of presortedness* for the rest of this article, though as you can see, those functions return 0 when the collection is already sorted,
as such it would be more appropriate to call them *measures of disorder*—and lots of authors do actually call them that!—but old habits die hard, and I'm gonna stick to the words of Mannila.

## Order isomorph, order spectrum? Find a name that isn't taken

I've been toying with sorting-adjacent concepts for more than a decade now, and go on a tangent every now and then, exploring tiny tools under the length of sorting and combinations.
A few days ago I went back to one of the simplest possible tools in the domain: a [three-way comparator][three-way-comparison] for two values:

$$
comp(x, y)=
\begin{cases}
-1 \quad \text{ if} x \lt y\\
1 \quad \text{ if} x \gt y\\
0 \quad \text{otherwise}
\end{cases}
$$

Nothing ground-breaking so far, it's similar to the [sign function][sign-function] applied to to the difference of two real numbers. Let's apply it to all adjacent pairs of elements of a sequence of elements $$X$$:

TODO: illustration

Still fairly boring if I'm being honest. Now let's compute the [prefix sum][prefix-sum] of that new sequence:

TODO: illustration

Now we get a cute result: a sequence of elements where the variations between adjacent elements follow those of the original sequence, except that the magnitude of that variation is always 0 or 1.

TODO: illustration of original collection vs. prefix sum

Okay, the previous statement is not exactly true: the original sequence has a size of $$|X|$$ while the prefix sum above has a size of $$|X| - 1$$.
I constructed the plot above by prepending 0 to the prefix sum, which leads to a sequence of size $$|X|$$ whose variations between pairwise elements match those of the original sequence exactly.
Interestingly, applying the same series of transformations on that 0-pefixed prefix sum yields the same result again.

Remove: As such that series of transormations, when confined to the integer domain, has a ρ-shaped orbit with a handle of size 0 or 1, and a cycle of size 1.

TODO: note at the bottom of the page for Stepanov

The plot above looks a bit like a shadow of the sequence, so I decided to call it the *pairwise order shadow* of the sequence, and will simply call it "shadow" for the rest of the article.

## Amplitude of a shadow

I started exploring that new mathematical object, and quickly wondered how much information about the order of the sequence was encoded into the peak-to-peak amplitude (PTP) of the shadow.
The idea being that it could constitue a basis for a measure of presortedness.

TODO: illustration of PTP amplitude

A few simple observations can be made about the PTP rather intuitively:
* It is maximal when the sequence is strictly ascending or strictly descending.
* It is zero when all elements compare equal.
* It is one when the relative order of neighbours changes at each step.
* It is at least as big as the longest ascending or descending run of the sequence.
* It is direction-agnostic: the relative order of all adjacent elements could be flipped, the PTP would remain the same.

TODO: illustrations

If we ignore the issue of elements that compare equal, there is an intuition that a bigger PTP means "more sorted", and a lower PTP means "less sorted".
Morever the direction-agnostic property is desirable to consider that a strictly descending sequence is somewhat presorted.
However, we can easily see shortcomings of the tool:

TODO: two images: one ascending run followed by a descending run, then one ascending run followed by randommness

The first pattern above is intuitively more ordered than the second one, however PTP considers them both equivalent.

## Amp as a measure of presortedness

TODO: feels kind of intuitive

TODO: Manilla definition

TODO: "prove" properties one by one

## Amp applied to different patterns

TODO: patterns from cpp-sorting

TODO: compare to other MOPs

## Partial ordering of measures of presortedness

TODO: mention paper, repeat graph without the bold, link to cpp-sort doc

TODO: try to analyze the best we can (for example, rapidcheck over Amp <= Run, make a bunch of those, if we find matching results, analyze further)

## Conclusion

TODO


  [neatsort]: https://arxiv.org/pdf/1407.6183
  [prefix-sum]: https://en.wikipedia.org/wiki/Prefix_sum
  [sign-function]: https://en.wikipedia.org/wiki/Sign_function
  [three-way-comparison]: https://en.wikipedia.org/wiki/Three-way_comparison
