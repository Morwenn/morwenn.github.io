---
layout: post
title: "TODO: smth runs mono presorting"
date: TODO
categories: presortedness
---

TODO: mention previous article about Mono, and its natural mergesort

## Reversing runs as a presorting algorithm

TODO: mini intro

TODO: paper about presorting average case, see whether it applies at all

TODO: turns a Runs-adaptive algorithm in a Mono-adaptive one, very cool because Mono(X) <= Runs(X)

TODO: mention that Runs(Y) < Mono(X), then the sequence violates axiom 4
      it corresponds to what we saw in article about descending runs

TODO: attempt to compute when it starts being pog (fewer operations)

TODO: the presorter turns any Runs-optimal algorithm Mono-optimal

## Mono in the partial order

TODO: partial order pic

TODO: how to read it

TODO: Mono-optimal is Runs-optimal

TODO: mention that algorithms that read reversing runs are already Mono-adaptive (probably), so no benefit

TODO: interesting use cases are for measures that are:
- better than runs
- not better than mono
- don't find presortedness in descending runs

okay that leaves SUS, potentially Amp, Osc and Loc but I don't believe it

## Concrete example

TODO: scrape paper about SUS and SMS, try to find a SUS-adaptive algorithm? patience sorting maybe?

## Conclusion

Presorting is cool, direct applications of measures of disorder

## Notes

  [^1]: previous article 1


  [measures-of-disorder]: https://github.com/Morwenn/cpp-sort/wiki/Measures-of-disorder
  [probe-mono]: https://codeberg.org/Morwenn/cpp-sort/wiki/Measures-of-disorder#Mono
  [probe-runs]: https://codeberg.org/Morwenn/cpp-sort/wiki/Measures-of-disorder#Runs
  [TSBTODO]: {% link _posts/2026-TODO.md %}
  [zigzag-permutation]: https://en.wikipedia.org/wiki/Alternating_permutation
