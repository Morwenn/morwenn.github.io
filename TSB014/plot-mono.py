import enum
import itertools
import operator

import numpy
from matplotlib import pyplot


class Direction(enum.Enum):
    ASC = enum.auto()
    DESC = enum.auto()

def unique(iterable):
    return [group[0] for group in itertools.groupby(iterable)]

def split_sequence(sequence):
    """
    Split the sequence into two collections:
    - Ascending sections of the sequence
    - Descending sections of the sequence

    The goal is to make it easier to display both parts in different colors.
    """
    ascending = []
    descending = []

    direction = Direction.ASC  # Assume ascending first
    run = []

    for current, next in itertools.pairwise(enumerate(sequence)):
        if current[1] < next[1]:
            if direction == Direction.DESC:
                descending.append(unique(run))
                run = [next]
                direction = None
            else:
                run.extend([current, next])
                direction = Direction.ASC
        elif current[1] > next[1]:
            if direction == Direction.ASC:
                ascending.append(unique(run))
                run = [next]
                direction = None
            else:
                run.extend([current, next])
                direction = Direction.DESC
        else:
            if direction == Direction.ASC:
                run.extend([current, next])
            else:
                run.extend([current, next])

    if run:
        if direction == Direction.ASC:
            ascending.append(unique(run))
        else:
            descending.append(unique(run))

    return ascending, descending


_, axis = pyplot.subplots()

sequence = [4, 10, 11, 19, 0, 7, 15, 20, 21, 12, 6, 13, 8, 14, 2, 1, 3, 5, 18, 9, 16, 17]
pyplot.plot(sequence, color="mediumpurple", ls="--")

# Fake plots to have proper labels
pyplot.plot([], label="Ascending runs", color="tab:blue")
pyplot.plot([], label="Descending runs", color="tab:orange")

# Real plots, no label
ascending_runs, descending_runs = split_sequence(sequence)

for group in ascending_runs:
    pyplot.plot(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="tab:blue"
    )
for group in descending_runs:
    pyplot.plot(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="tab:orange"
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
    if left < cross_target < right or left > cross_target > right:
        pyplot.scatter(
            [idx], [left],
            facecolors="none",
            edgecolors="tab:green",
            s=120,
            zorder=10,
        )
        cross += 1

mono = len(ascending_runs) + len(descending_runs) - 1
pyplot.xlabel(rf"$\mathit{{Mono}}(X) = {mono}, \mathit{{Cross}}(x_{cross_target}) = {cross}$")

pyplot.show()

