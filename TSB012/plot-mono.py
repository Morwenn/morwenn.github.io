import enum
import itertools
import numpy
import operator
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


pyplot.subplots(figsize=(6, 3))

sequence = [4, 5, 6, 5, 7, 8, 6, 3, 3, 4, 6, 9, 9, 6, 5, 4, 8, 8, 12, 11, 9, 7, 8, 6]
sequence = [val - 2 for val in sequence]

# Fake plots to have proper labels
pyplot.plot([], label="Ascending runs", color="tab:blue")
pyplot.plot([], label="Descending runs", color="tab:orange")

# Real plots, no label
ascending, descending = split_sequence(sequence)

for group in ascending:
    pyplot.scatter(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="tab:blue"
    )
    pyplot.plot(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="tab:blue"
    )
for group in descending:
    pyplot.scatter(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="tab:orange"
    )
    pyplot.plot(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="tab:orange"
    )

for section in itertools.chain(ascending, descending):
    begin = section[0][0]
    end = section[-1][0] + 1
    pyplot.annotate("",
        xy=(max(0, begin - 0.1), 11),
        xytext=(end + 0.1, 11),
        arrowprops={
            "arrowstyle": "<->",
            "ls": "--"
        }
    )

pyplot.xlabel(f"Mono(X) = {len(ascending)+len(descending)-1}")

pyplot.xlim(xmin=0, xmax=len(sequence))
pyplot.ylim(ymin=0, ymax=12)
pyplot.subplots_adjust(bottom=0.2)

axes = pyplot.gca()
axes.xaxis.get_major_locator().set_params(integer=True)
axes.yaxis.get_major_locator().set_params(integer=True)


pyplot.show()    

