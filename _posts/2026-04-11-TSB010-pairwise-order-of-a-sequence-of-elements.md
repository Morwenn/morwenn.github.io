---
layout: post
title: "Pairwise order of a sequence of elements"
date: 2026-04-11
categories: presortedness
---

In the [very first post][TSB001] of this blog, I described a new [measure of disorder][measures-of-disorder] which I called $$\mathit{Amp}$$.
I started its construction process by introducing what I dubbed the *pairwise order* of a sequence as follows:

> A few days ago I went back to one of the simplest possible tools in the domain: a [three-way comparator][three-way-comparison] for two values:
>
> $$
  \mathit{comp}(x, y)=
  \begin{cases}
  1 & \text{ if } x \lt y\\
  -1 & \text{ if } x \gt y\\
  0 & \text{otherwise}
  \end{cases}
  $$
>
> Nothing ground-breaking so far, it's similar to a negation of the [sign function][sign-function] applied to the difference of two real numbers. Let's apply it to all adjacent pairs of elements of a sequence of elements $$X$$:
>
> ![Pairwise order of a sequence of elements: sequence 3, 4, 6, 6, 6, 7, 8, 6, 4 and the pairwise order 1, 1, 0, 0, 1, 1, -1, -1]({{ site.baseurl }}/assets/images/TSB001/pairwise-order.png){:.centered}
>
> Still fairly boring if I'm being honest. We will call that new sequence the *pairwise order* of the sequence for the rest of the article.

Today's article is all about showing that this so-called *pairwise order* is, in fact, maybe not all that boring.

## Definition(s) and properties

The definition above was spot-on when talking about the sign function and three-way comparisons.
The "negation" part however felt a bit confusing upon rereading it: it seems to arbitrarily consider $$x - y$$ instead of $$y - x$$ without being explicit about it.
I would rather describe it again as the sequence made of the sign function applied to the [difference operator][difference-operator] over a sequence of elements:

$$\forall X_i \in \mathbb{R}, \mathit{Order}(X) = \langle \text{sgn } (\Delta X)_i \vert 1 \le i < \lvert X \rvert \rangle$$

That new definition gets rid of the "negation" part, and the direction of the subtraction implicitly follows the definition of the difference operator.

When I showed the article to a friend, she immediately described the pairwise order it as "discrete derivative".
It also accurately matches the intuition of the tool, even though I managed to write the whole thing without ever thinking of derivatives.
After all, the general definition is not about numbers but considers anything satisfying a [strict weak ordering][strict-weak-ordering], as is usual in the realm of [comparison sorts][comparison-sort].

A few obvious properties of the pairwise order immediately emerge from its definition:
* Its size: $$\lvert \mathit{Order}(X) \rvert = \lvert X \rvert - 1$$.
* A sorted sequence produces a pairwise order without any $$-1$$ (and the opposite is true).
* A sequence sorted in reverse order produces a pairwise order without any $$1$$ (the opposite is also true).
* A sequence of distinct elements produces a pairwise order without any $$0$$ (the opposite is not necessarily true).

Let $$\mathit{Reversed}(X)$$ be a function that produces a sequence corresponding to $$X$$ traversed in reversed order.
We showed in [a previous article][TSB005] that $$\mathit{Order}_i(\mathit{Reversed}(X)) = -\mathit{Order}_{\lvert X \rvert - i }(X)$$.

## Pairwise order and measures of disorder

If we have the pairwise order of a sequence $$X$$, we can compute $$\mathit{Amp}(X)$$, we don't need to know more about $$X$$.
That property immediately follows from how it was originally defined.

What's interesting is that _other_ measures of disorder can be redefined in terms of the pairwise order.
Let's take $$\mathit{Runs}$$ for example, for which I already gave a few definitions in [a previous blog post][TSB007]. One of those was:

$$\mathit{Runs}(X) = \lvert \{ i \vert 1 \le i \lt \lvert X \rvert \wedge X_i \gt X_{i+1} \} \rvert$$

It is the number of _steps-down_ in $$X$$, that is, the number of pairs of neighbors where the left element is greater than the right one.
It can trivially be redefined in terms of the pairwise order of $$X$$ as follows:

$$\mathit{Runs}(X) = \lvert \{ i \vert \mathit{Order}_i(X) = -1 \} \rvert$$

Another such measure is $$\mathit{Mono}$$, a measure introduced by H. Zhang, B. Meng and Y. Liang in [*Sort Race*][sort-race]:

> Intuitively, if $$\mathit{Mono}(X) = k$$, then $$X$$ is the concatenation of $$k$$ monotonic lists (either sorted or reversely sorted).

Computing $$\mathit{Mono}(X)$$ is a matter of checking all pairs of neighbors in $$X$$ for ascending run, then descending run, then ascending run, etc. and the result is the number of such runs minus $$1$$.
It is a natural extension of $$\mathit{Runs}$$ that also finds order in descending runs.
Since we only need the order of neighbors to compute it, it is fairly obvious that the pairwise order of a sequence is enough to compute it.

What I'm trying to get at here is that all of those measures of disorder can be _reduced_ to their effect on the pairwise order.
That is, instead of trying to understand how they are affected by changes in the original sequence of values,
we can instead analyze how they behave when adding or removing $$-1$$, $$0$$ or $$1$$ from the pairwise order[^1].
This greatly reduces the scope of the problem.

A corollary is that any measure of disorder that can be defined in terms of the pairwise order alone,
is guaranteed to return the same result for two pairwise-order-isomorphic sequences.

## Equal elements in measures of disorder

One common theme in this blog is the notion of measures of disorder over sequences that contain equal elements.
For context, Mannila's axioms — as well as most of the literature about disorder — only consider sequences of _distinct_ elements when analyzing measures of disorder.
While some real-world subproblems are indeed limited to sequences of distinct elements, I believe that most existing data contains equal elements.
As such, they deserve our attention too.

Measures based on the pairwise order make the distinction trivial:
* Sequences with equal elements produce a pairwise order which can contain $$0$$ elements;
* Sequences of distinct elements produce a pairwise order that only contains $$-1$$ and $$1$$.

We saw earlier that $$\mathit{Runs}(X)$$ can be redefined as the number of $$-1$$ in the pairwise order.
Interestingly this definition is valid regardless of whether the sequence contains equal elements or not:
we want a sequence made exclusively of equal elements to be considered sorted, so we have to consider that any two equal neighbors belong to the same run.

Let $$\mathit{Unique}(X)$$ be a function that associates to the sequence $$X$$ the same sequence with subsequences of equal neighbors reduced to a single element
(similar to the C++ algorithm [`std::unique`][std-unique]). We have:

$$\mathit{Runs}(\mathit{Unique}(X)) = \mathit{Runs}(X)$$

We follow a similar process for $$\mathit{Mono}$$, where any pair of equal elements is considered as belonging to the run that commes before it[^2].
As such, it is equivalent to entirely ignoring $$0$$ elements in the pairwise order, which gives:

$$\mathit{Mono}(\mathit{Unique}(X)) = \mathit{Mono}(X)$$

The same equality is valid for $$\mathit{Amp}$$, whose definition simply considers that $$0$$ elements in the pairwise order do not contribut to disorder.
This means that comparing the values returned by $$\mathit{Runs}$$, $$\mathit{Mono}$$ and $$\mathit{Amp}$$ can be reduced even further to comparing the values returned by those measure over $$\mathit{Unique}(X)$$,
entirely ignoring the $$0$$ elements from the pairwise order.

## Conclusion

Over the course of the previous year, my vision of the pairwise order went from "fairly boring" to "wait, that's actually a pretty cool tool".
The apparent simplicity of the feature remained, yet being able to list some of its properties eventually made it feel like a useful concept in and of itself.

Any two algorithms that are entirely based on the pairwise order of a sequence can be reduced to comparing changes to $$-1$$, $$0$$ and $$1$$, thereby reducing the scope of the analysis.
We saw that redefining measures of disorder in terms of the pairwise order allowed us to benefit from this simpler mental model.

I have been wanting to analyze the relationship between $$\mathit{Mono}$$ and $$\mathit{Amp}$$ for some time,
and to push it further than just $$\mathit{Amp} \not \preceq \mathit{Mono}$$[^3].
I originally wasn't sure how to do it; the current article made me realize that I could reduce the problem to comparing how changes to $$\mathit{Order}(\mathit{Unique}(X))$$ impact both measures.

The full analysis of that comparison, however, is not for today. It will surely be the topic of a subsequent article.

## Notes

  [^1]: This is technically what I did in [*Amp: a new measure of presortedness?*][TSB001] to prove that $$\mathit{Amp}$$ respects Mannila's 3rd axiom for measures of presortedness.
        I used the same approach to prove that $$\mathit{Amp}(X) \le 2 \mathit{Runs}(X)$$ in [*Relationship between Amp and Runs*][TSB007].

  [^2]: The original definition of $$\mathit{Mono}$$ says nothing about elements that compare equal.
        Deciding that any pair of equal neighbors belongs to the same run is a choice I made a long time ago, but other definitions could have been possible.
        For example, stable sorting algorithms often consider that equal neighbors are part of the same ascending run, but cannot be part of a same descending run.
        The reason is practical: those algorithm often blindly reverse descending runs, a process that is not stable if said runs contain equal elements.

  [^3]: See [*Amp and the partial ordering of measures of disorder, part 1*][TSB008].


  [comparison-sort]: https://en.wikipedia.org/wiki/Comparison_sort
  [difference-operator]: https://en.wikipedia.org/wiki/Recurrence_relation#difference_operator
  [measures-of-disorder]: https://github.com/Morwenn/cpp-sort/wiki/Measures-of-disorder
  [sort-race]: https://arxiv.org/ftp/arxiv/papers/1609/1609.04471.pdf
  [three-way-comparison]: https://en.wikipedia.org/wiki/Three-way_comparison
  [TSB001]: {% link _posts/2025-06-15-TSB001-amp-a-new-measure-of-presortedness.md %}
  [TSB005]: {% link _posts/2025-10-18-TSB005-symmetry-of-amp.md %}
  [TSB007]: {% link _posts/2025-11-09-TSB007-relationship-between-amp-and-runs.md %}
  [TSB008]: {% link _posts/2026-02-15-TSB008-amp-and-the-partial-ordering-of-measures-of-disorder-part-1.md %}
  [sign-function]: https://en.wikipedia.org/wiki/Sign_function
  [std-unique]: https://en.cppreference.com/w/cpp/algorithm/unique.html
  [strict-weak-ordering]: https://en.wikipedia.org/wiki/Weak_ordering#Strict_weak_orderings
