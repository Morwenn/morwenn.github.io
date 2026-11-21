---
layout: post
title: "Matrices, determinants, disorder"
date: 202?-??-??
categories: presortedness
---

TODO: A few weeks ago, mountain, friend mentioned *The Manga Guide to Linear Algebra* by Shin Takahashi and Iroha Inoue

TODO: thought it was a joke, got surprised, and acquired a copy to read it

TODO: nice book, helped me brush up linear algebra, which I hadn't seen since engineering school more than a decade ago

TODO: brings us to the topic of this article: determinants

## Determinants

TODO: define determinants, invertible square matrices

TODO: examples of computing 2x2 and 3x3 matrices, give the tricks to remember them

## Scaling to bigger matrices

TODO: the formula to compute the determinant of a 4x4 matrix is as follows, there's no simple trick

TODO:  4x4 matrix

$$TODO: 24 terms$$

TODO: if you count the numbers of added/subtracted terms (2, 6, 24), you might start to notice a pattern: factorials, and you would be right

TODO: to understand why let's look at the method given by MC to compute it

TODO: first subscript term is always 1, 2, 3, 4, second subscript term is always a permutation of 1, 2, 3, 4
TODO: the formula uses all the permutations of 1234, which explains the factorial term

TODO: one issue remains, which is what should be added and what should subtracted
TODO: MC gives a complicated explanation which boils down to "count inversions, use MC's words"

TODO: table

TODO: my brain did not need the exact name to recognize it: that's inversions

# Disorder

TODO: I lied, this article is not about linear algebra, it's about disorder again

TODO: describe Inv

TODO: I never thought of analyzing the parity of measures before
TODO: RapidCheck

TODO: found a single _one_ for which it worked, conjecture that Exc=Inv(mod 2)

TODO: define Exc

# Improving the determinant algorithm

TODO: conveniently for this blog post, it means that we can use Exc instead of Inv to compute the determinant of a matrix

TODO: to understand why it matters, we have to look at complexity of computing Inv
TODO: naive method is quadratic, improved method based on mergesort is O(n log n), some other method has a better complexity

TODO: we compute inversions for all permutations, algorithm to compute determinant is therefore O(n! * n log n) or a bit better

TODO: let's look at Exc, it can be computed by sorting the permutation, then reordering cycles which is O(n)
TODO: cpp-sort says it's n log n because it's based on comparisons, and sorting with comp is n log n (see previous article)
TODO: but we're sorting integers, which can be done in O(n + k) with radix sort, and here k=n so O(n)
TODO: therefore Exc here is linear-computable and determinant can be computed in O(n! * n)

TODO: does it matter? no, the manga mentions that real world performs Gauss elimination and whatnot (TODO) to repeatedly simplify the problem space, which is much faster

## Conclusion

TODO: manga was a surprisingly fun way to relearn

TODO: bridges between disciplines are poggers, allow to look at things under a new angle

## Notes

  [^1]: TODO


  [cpp-sort]: TODO:<codeberg>
  [cpp-sort-exc]: TODO:<codeberg>
  [determinant]: https://en.wikipedia.org/wiki/Determinant
  [measures-of-disorder]: :<codeberg>
