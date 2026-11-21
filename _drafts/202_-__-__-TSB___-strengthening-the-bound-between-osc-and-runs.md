---
layout: post
title: "Strengthening the inequality between Osc and Runs"
date: TODO
categories: presortedness
---

Furthermore the argument could be made that only runs of two elements or more can contribute two elements to $$\mathit{Cross}(x_i)$$.
While it makes sense, $$\mathit{Runs}(X)$$ doesn't tell us much about the size of the individual runs in $$X$$.

TODO: proper bounds below, floor or ceiling? Compute and come back

The best we can do is consider whenever a sequence contains more than $$\frac{\lvert X \rvert}{2}$$ runs,
then at least $$\mathit{Runs}(X) - \frac{\lvert X \rvert}{2}$$ of those contain a single element.
That leads to the following inequality:

TODO: another way is to look from the opposite side: Runs(X) = |X|-1 means that all sequences are 1
|X|-2 = all sequences are 2
TODO: compare to what the other definition says

TODO: how to combine them? Is there prior literature?

TODO: probably shit, get it right

$$
\mathit{Osc}(X) \le
\begin{cases}
2 \cdot \frac{\lvert X \rvert}{2} \cdot \mathit{Runs}(X) + \lvert X \rvert \cdot (\mathit{Runs}(X) - \frac{\lvert X \rvert}{2}) \text{ if } \mathit{Runs}(X) > \frac{\lvert X \rvert}{2}\\
2 \cdot \lvert X \rvert \cdot \mathit{Runs}(X) \text{ otherwise}
\end{cases}
$$
