---
layout: post
title: "Symmetry of Amp"
date: 2025-10-18
categories: presortedness
---

In [a previous article]({% link _posts/2025-06-15-TSB001-amp-a-new-measure-of-presortedness.md %}), I introduced a new [measure of disorder][measures-of-disorder] that I called $$\mathit{Amp}$$ and attempted to determine whether it is a measure of presortedness (it is not).
In this short note, I am going to demonstrate another property of $$\mathit{Amp}$$: its symmetry over the input sequence. That is:

$$\mathit{Amp}(\mathit{Reversed}(X)) = \mathit{Amp}(X)$$

In this article, we are using the following definition for $$\mathit{Amp}$$, which takes into account elements that compare equal (see previous article for what the individual terms mean):

$$\mathit{Amp}(X) = \lvert X \rvert - \mathit{PTP}(X) - N_{\mathit{eq}}(X) - 1$$

We already saw in the previous article that $$\mathit{Amp}(X) = 0$$ when $$X$$ is a sorted sequence, but also when $$X$$ it is a reverse-sorted sequence, which is a special case of that property.
We can as easily find examples with much more random sequences, let's take one from the original article:

$$X = \langle 4, 6, 6, 6, 7, 8, 6, 4, 3, 2, 5, 6, 1, 2, 7, 7, 5, 6, 8, 11, 11, 11, 9, 7, 8, 6 \rangle$$

* ‎$$\mathit{Amp}(X) = \lvert X \rvert - \mathit{PTP}(X) - N_{\mathit{eq}}(X) - 1 = 26 - 5 - 5 - 1 = 15$$
* ‎$$\mathit{Amp}(\mathit{Reversed}(X)) = \lvert \mathit{Reversed}(X) \rvert - \mathit{PTP}(\mathit{Reversed}(X)) - N_{\mathit{eq}}(\mathit{Reversed}(X)) - 1 = 26 - 5 - 5 - 1 = 15$$

![Line graph of a sequence of integers and its shadow, with the peak-to-peak amplitude illustrated]({{ site.baseurl }}/assets/images/TSB005/amp-random-sequence.png){:.centered}
![Same as above, with the same sequence of integers reversed]({{ site.baseurl }}/assets/images/TSB005/amp-random-sequence-reversed.png){:.centered}

The first striking observation is the sheer amount of symmetry in the different elements that contribute to $$\mathit{Amp}$$:
* ‎$$\lvert \mathit{Reversed}(X) \rvert = \lvert X \rvert$$
* ‎$$\mathit{PTP}(\mathit{Reversed}(X)) = \mathit{PTP}(X)$$
* ‎$$N_{\mathit{eq}}(\mathit{Reversed}(X)) = N_{\mathit{eq}}(X)$$

The size of a reversed sequence being equal to the size of the original sequence is trivially true,
and it makes sense that the number of elements that compare equivalent is the same, no matter the direction in which we traverse a sequence.
I don't think those need to be demonstrated  any further, which leaves one thing to prove: the symmetry of $$\mathit{PTP}(\mathit{Reversed}(X)) = \mathit{PTP}(X)$$.

The line graph above gives an intuitive explanation: the peak-to-peak amplitude of the shadow of the reversed sequence is the same as that of the sequence
because the shadow of the reversed sequence is a reversal of the shadow of the sequence, shifted along the vertical axis by some constant value.
More formally, we need to prove the following conjecture (assuming 1-based indexing):

$$\mathit{Shadow}_i(\mathit{Reversed}(X)) = \mathit{Shadow}_{\lvert X \rvert - i + 1}(X) + V$$

Where $$V = -\mathit{Shadow}_{\lvert X \rvert}(X)$$ is the aforementioned shift along the vertical axis (also conjectured from the line graph).

We start by restating the definition of $$\mathit{Shadow}(X)$$: it is the [prefix sum][prefix-sum] of the *pairwise order* of the elements of $$X$$ (called $$\mathit{Order}(X)$$ below),
which is itself a sequence of $$\lvert X \rvert$$ elements taking the values $$-1$$, $$0$$ or $$1$$ (always prefixed with a single $$0$$).

![Pairwise order shadow of a sequence of elements: sequence 3, 4, 6, 6, 6, 7, 8, 6, 4 and the pairwise order shadow 1, 2, 2, 2, 3, 3, 2, 1]({{ site.baseurl }}/assets/images/TSB001/pairwise-order-shadow.png){:.centered}

By definition, the ith element of $$\mathit{Shadow}(X)$$ is the sum of elements $$1$$ to $$i$$ (inclusive) of the *pairwise order* of $$X$$:

$$\mathit{Shadow}_i(X) = \sum_{k=1}^i \mathit{Order}_k(X)$$

We prove the conjecture with the following reasoning:

$$\begin{aligned}
\mathit{Shadow}_i(\mathit{Reversed}(X)) & = \sum_{k=1}^i \mathit{Order}_k(\mathit{Reversed}(X))\\
                                        & = \sum_{k=\lvert X \rvert-i+2}^n -1 * \mathit{Order}_k(X) & \text{ (1) }\\
                                        & = -1 * \sum_{k=\lvert X \rvert-i+2}^n \mathit{Order}_k(X)\\
                                        & = -1 * (\sum_{k=1}^{\lvert X \rvert} \mathit{Order}_k(X) - \sum_{k=1}^{\lvert X \rvert-i+1} \mathit{Order}_k(X)) & \text{ (2) }\\
                                        & = \sum_{k=1}^{\lvert X \rvert-i+1} \mathit{Order}_k(X) - \sum_{k=1}^{\lvert X \rvert} \mathit{Order}_k(X)\\
                                        & = \mathit{Shadow}_{\lvert X \rvert-i+1}(X) - \mathit{Shadow}_{\lvert X \rvert}(X)
\end{aligned}
$$

$$(1)$$ follows from the definition of the *pairwise order*: it is a collection made of a single $$0$$ element followed by the pairwise comparison pairs of adjacent elements according to the following comparison function:

$$
\mathit{comp}(x, y)=
\begin{cases}
1 & \text{ if } x \lt y\\
-1 & \text{ if } x \gt y\\
0 & \text{otherwise}
\end{cases}
$$

When traversing the collection in reverse order, we end up performing the same comparisons starting from the end of the sequence, with the order of its parameters flipped.
It is trivial to see that $$\mathit{comp}(y, x) = -\mathit{comp}(x, y)$$,
which gives us that the first $$n$$ elements of the *pairwise order* of a reversed sequence correspond to $$0$$ followed by the last $$n-1$$ elements of the *pairwise order* of the original sequence, reversed and negated:

Example, with arbitrary emphasis on the first three elements of a sequence, and the corresponding pairwise order:

| Index |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |
| :---- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| $$X$$ | **3** | **4** | **6** | 6 | 6 | 7 | 8 | 6 | 4 |
| $$\mathit{Order}(X)$$ | 0 | **1** | **1** | 0 | 0 | 1 | 1 | -1 | -1 |
| $$\mathit{Reversed}(X)$$ | 4 | 6 | 8 | 7 | 6 | 6 | **6** | **4** | **3** |
| $$\mathit{Order}(\mathit{Reversed}(X))$$ | 0 | 1 | 1 | -1 | -1 | 0 | 0 | **-1** | **-1** | 

$$(2)$$ is the simple observation that the sum of a subsequence equals the sum of the whole sequence minus the sum of the rest of the sequence.

Q.E.D.

Back to our original conjecture, we can conclude as follows:

$$\begin{aligned}
\mathit{PTP}(\mathit{Reversed}(X)) & = \max \mathit{Shadow}(\mathit{Reversed}(X)) - \min \mathit{Shadow}(\mathit{Reversed}(X))\\
                                   & = \max (\mathit{Shadow}(X) + V) - \min (\mathit{Shadow}(X) + V)\\
                                   & = \max \mathit{Shadow}(X) - \min \mathit{Shadow}(X)\\
                                   & = \mathit{PTP}(X)
\end{aligned}
$$

And that's it, that's enough to show that $$\mathit{Amp}(\mathit{Reversed}(X)) = \mathit{Amp}(X)$$.


  [measures-of-disorder]: https://github.com/Morwenn/cpp-sort/wiki/Measures-of-disorder
  [prefix-sum]: https://en.wikipedia.org/wiki/Prefix_sum
