import itertools
import numpy
from matplotlib import pyplot


_, axis = pyplot.subplots()

sequence = [4, 10, 11, 19, 0, 7, 15, 20, 21, 12, 6, 13, 8, 14, 2, 1, 3, 5, 18, 9, 16, 17]
pyplot.plot(sequence, color="mediumpurple", ls="--")

runs = sum(
    1 for left, right in itertools.pairwise(sequence)
    if right < left
)

cross_target = 9
pyplot.axhline(cross_target, color="tab:green", ls="-.")
yticks = [*axis.get_yticks(), cross_target]
yticklabels = [*axis.get_yticklabels(), rf"$\mathit{{Cross}}(x_{cross_target})$"]
axis.set_yticks(yticks, labels=yticklabels)

begin = 0
cross = 0
in_run = False
for idx, (left, right) in enumerate(itertools.pairwise(sequence)):
    if left <= right:
        pyplot.plot([idx, idx+1], [left, right], color="tab:blue")
        in_run = True
    else:
        if not in_run:
            pyplot.scatter([idx], sequence[idx], color="tab:blue", marker="o")
        in_run = False

    if left < cross_target < right or left > cross_target > right:
        pyplot.scatter(
            [idx], [left],
            facecolors="none",
            edgecolors="tab:green",
            s=120,
            zorder=10,
        )
        cross += 1

pyplot.xlabel(rf"$\mathit{{Runs}}(X) = {runs}, \mathit{{Cross}}(x_{cross_target}) = {cross}$")

pyplot.show()

