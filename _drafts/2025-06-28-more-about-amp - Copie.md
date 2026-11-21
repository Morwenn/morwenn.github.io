---
layout: post
title: ""
date: 2025-05-08
categories: algorithms, sorting, presortedness
---

- Amp over different patterns
- Jay remark about random walk
- Whatever Corobo said about groups and whatnot

New article: Amp(VFlip(X)) = Amp(X)

Amp compared to some other MOPs:
- Mono:
  -> Amp(pipe-organ) = |X|/2, mais Mono(pipe-organ) = 1, donc auncun $c$ tel que $c Amp(X) \le Mono(X)$
  -> Mono(X) <= Amp(X)
  -> Amp != SUS: SUS does not find order in reverse sequence, Amp does not find order in 1, 3, 2, 4, 5, 7, 6, 8, etc.
Assume that measures of disorder that do not find order in reversed sequences are not superior to Amp:
* Exc, Ham, Max, Dis, Runs, Rem, Inv, Spear, SUS, Block are not superior to Amp
Assuming that it works, compare with SUS, Osc, Loc, Max/Dis

Computing the below-set seems too complicated, but
* Amp(X)=0 has 2 solutions no matter the number of inputs
* Amp(X)=1 has (|X|-1)*4 solutions (the 4 could correspond to a sequence and its horizontal and vertical flips)
* Amp(X)=|X|-2 follows zigzag numbers

Other ways to look at it:
- PTP can be seen as the number of unique values in the shadow
- Amp is the number of sign change of comp(x) after removing the 0 (TODO: check)
- Corobo: shadow is discrete/integrald derivative?

Prefix monotonicity fail: -1, 0, 0, 0 (TODO: unique?)
Monotonicity fail: 1183232, 2818670, 444292, -2199770, 2908908
-> TODO: generate real inputs

- As such that series of transormations, when confined to the integer domain, has a ρ-shaped orbit with a handle of size $$0$$ or $$1$$, and a cycle of size $$1$$ (Stepanov & McJohns)


In the study of *Amp*, the notion of disorder corresponds to the number of elements of the shadow that do not contribute to $$PTP$$.
If we plot the shadow as follows, we can even manually count the disorder:

TODO: plot of the shadow as thick points, with dashed horizontal lines, the first points are in a colour, the disorder in another color, 0 in a third color

As we can see, all points in that graph either contribute to $$PTP$$ (in blue), or do not contribute to $$PTP$$ (in red).
*Amp* as we defined it actually corresponds to the number of those points that do not contribute to $$PTP$$.

