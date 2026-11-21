Not even a post, just a draft for post ideas:
- Median theorem vs. Pythagoras, the fun of mathematics
- Exc(X) % 2 = Inv(X) % 2, relation to computing determinants
- Pairwise order, packing?
  -> $$\mathit{Order}(X) = \langle \text{sgn } (\Delta X)_i | 1 \le i < \lvert X \rvert \rangle$$
  -> Composition of the sign function over the difference operator for R
  -> size Order = |X|-1
  -> relationship with Amp, Runs, Mono
  -> show that thanks to order-isomorphism, a MOP based on Order can be reduced to comparing Order
  -> Note about repeated elements, note about ignoring zero and M(Unique(X))=M(X)
- Prove relation between Amp and Mono? relationship between Mono and number of direction flip in the Order?
  -> Mention rêves fiévreux
  -> Mono <= Reve <= 2Mono, donc Rev est équivalent à Mono
  -> Relation entre Reve et Amp, montrer que ça prouve la relation entre Amp et Mono
  -> Reve ne respecte pas l'axiome 4
- Article about Shadow?
  -> Shadow(Shadow(X)) = Shadow(X)
  -> Order-isomorphic to original sequence
  -> As such, Runs(Shadow(X))=Runs(X), etc.
  -> What about other MOPs over the shadow?


## Storing the pairwise order (TODO: do we want this???)

The pairwise order is de facto a collection of elements in base 3

Most of us don't have access to a [Setun][setun] computer nowadays, and have to deal with binary

A natural way to store ternary is -1:0b10, 0:0b00, 1:0b01

Storing one such trit per byte wastes most of it, storing 4 per bytes still wastes 25% of the space since 0b11 is unused

How much can we pack? TODO
