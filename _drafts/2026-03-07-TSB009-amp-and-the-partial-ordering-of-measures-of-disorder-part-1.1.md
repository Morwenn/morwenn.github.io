---
layout: post
title: "Amp and the partial ordering of measures of disorder, part 1.1"
date: 2026-03-09
categories: presortedness
---

This post is a short note to complete the work started in the [first of this article][TSB008],
in which we discussed ways to compare [measures of disorder][measures-of-disorder] to construct a partial order.
We then tried to apply that newfound knowledge to narrow down the place of [$$\mathit{Amp}$$][TSB001] in the partial order.

That work remains unfinished as we haven't yet learnt to formally prove that a measure is "better" that another,
but instead analyzed how counter-examples are enough to demonstrate that a measure of disorder is _not_ better than another one.

$$\mathit{Block}(X)$$ is a measure of dirorder introduced by S. Carlsson, C. Levcopoulos and O. Petersson in *Sublinear merging and natural mergesort*.
It is defined as follows ($$\pi$$ is the sorted permutation):

$$\mathit{Block}(X) = \lvert \{ i | 1 \le i \lt \lvert X \rvert \land \pi(i) + 1 \neq \pi(i + 1) \} \rvert + 1$$

In other words, it corresponds to the number of elements in the sequence $$X$$ that don't have the same right neighbor in the sorted permutation.
Intuitively, $$1 \le \mathit{Block}(X) \le \lvert X \rvert$$ for any sequence $$X$$.

Let's now consider the following sequence, obtained by reversing a sorted sequence then swapping its elements pairwise:

$$
X = \langle 0, 1, 3, ..., \frac{\lvert X \rvert}{2} - 1, \lvert X \rvert, \lvert X \rvert - 1, ..., \frac{\lvert X \rvert}{2} \rangle
$$

TODO: ceil or floor?
For such a sequence, we have $$\mathit{Block}(X) = \frac{lvert X \rvert}{2}$$ and $$\mathit{Amp} = \lvert X \rvert - 2$$, which is the maximal value it can take.

![Amp construction for sequence 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]({{ site.baseurl }}/assets/images/TSB009/bad-amp-good-block.png){:.centered}

> There is no constant $$c \in \mathbb{N}$$ such as $$Amp(X) \le c \cdot \mathit{Mono}(X)$$ for every sequence $$X$$.

In other words, $$\mathit{Amp}$$ is not algorithmically finer than $$\mathit{Mono}$$.

### $$\mathit{Amp} \not \preceq \mathit{Max}$$

$$\mathit{Max}$$ is the maximum distance an element of a sequence has to travel to reach its sorted position.

Let's consider the following sequence, obtained by swapping pairs of elements in a sorted permutation:

$$
X = \langle 1, 0, 3, 2, ..., n - 2, n - 3, n, n - 1 \rangle
$$

For such a sequence, we have $$\mathit{Max}(X) = 1$$ and $$\mathit{Amp} = \lvert X \rvert - 2$$, which is the maximal value it can take.

![Amp construction for sequence 1, 0, 3, 2, 5, 4, 7, 6, 9, 8]({{ site.baseurl }}/assets/images/TSB008/max-amp-min-max.png){:.centered}

> There is no constant $$c \in \mathbb{N}$$ such as $$Amp(X) \le c \cdot \mathit{Max}(X)$$ for every sequence $$X$$.

In other words, $$\mathit{Amp}$$ is not algorithmically finer than $$\mathit{Max}$$.

Transitively, this means that $$\mathit{Amp}$$ cannot be algorithmically finer than $$\mathit{Dis}$$, $$\mathit{Enc}$$, $$\mathit{Hist}$$, $$\mathit{Inv}$$, $$\mathit{Loc}$$, $$\mathit{Osc}$$, $$\mathit{Reg}$$, $$\mathit{Spear}$$, $$\mathit{SMS}$$, nor $$\mathit{SUS}$$.

![Amp in partial ordering of measures of disorder, with some hypotheses pruned]({{ site.baseurl }}/assets/images/TSB008/partial-ordering-amp-2.png){:.centered}

## Conclusion

Over the course of this article, we discovered that there's more than meets the eye when it comes to comparing measures of disorders.
A simple comparison of their results simply does not cut it. We need something more.

We could not prove that $$\mathit{Amp}$$ was better than any other measure,
neither could we prove that any other measure was better than $$\mathit{Amp}$$.
We could show however that some measures were _not_ better than $$\mathit{Amp}$$,
and inversely that $$\mathit{Amp}$$ was not better than some measures.
Technically, that's enough to prove the non-equivalence of $$\mathit{Amp}$$ and a bunch of those measures.

I can't finish that article without a conjecture.
My personal feeling is that the following relations hold:
* ‎$$\mathit{Amp} \preceq \mathit{Runs}$$
* ‎$$\mathit{Mono} \preceq \mathit{Amp}$$
* ‎$$\mathit{Osc} \preceq \mathit{Mono}$$[^4]

Which means that the complete graph for the partial ordering would look like this:

![Conjectured complete partial ordering of measures of disorder]({{ site.baseurl }}/assets/images/TSB008/partial-ordering-conjecture.png){:.centered}

In a future article, we will dig further and attempt to understand how to formally prove than a measure of disorder is better than another one.

## Notes

  [^1]: A property that can be directly attributed to [the symmetry of $$\mathit{Amp}$$ over the input sequence][TSB005].

  [^2]: $$\mathit{Runs}$$ counts the number of step-downs in a sequence (pairs of consecutive elements such as $$x_{i+1} > x_i$$).
        In any such pairs, at least one of the two elements cannot be part of the longest increasing subsequence of $$X$$.
        It follows that $$\mathit{Runs} \le \mathit{Rem} + 1$$.

  [^3]: A result proven by Heikki Mannila in *Measures of Presortedness and Optimal Sorting Algorithms*.

  [^4]: The place of $$Mono$$ in the graph is actually also a conjecture.
        I applied similar reasoning that can be found in the [original research][original-research-mono] section of cpp-sort's documentation.
  

  [measures-of-disorder]: https://github.com/Morwenn/cpp-sort/wiki/Measures-of-disorder
  [original-research-mono]: https://codeberg.org/Morwenn/cpp-sort/wiki/Original-research#partial-ordering-of-mono
  [partial-order]: https://en.wikipedia.org/wiki/Partially_ordered_set#Partial_orders
  [partial-ordering]: https://github.com/Morwenn/cpp-sort/wiki/Measures-of-disorder#partial-ordering-of-measures-of-disorder
  [TSB001]: {% link _posts/2025-06-15-TSB001-amp-a-new-measure-of-presortedness.md %}
  [TSB008]: {% link _posts/2026-02-15-TSB008-amp-and-the-partial-ordering-of-measures-of-disorder-part-1.md %}
