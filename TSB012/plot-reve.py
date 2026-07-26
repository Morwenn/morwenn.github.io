import enum
import itertools
import numpy
import operator
from matplotlib import pyplot

class Direction(enum.Enum):
    ASC = enum.auto()
    DESC = enum.auto()

def comp(lhs: int, rhs: int) -> int:
    if lhs < rhs:
        return 1
    if rhs < lhs:
        return -1
    return 0

def pairwise_order(sequence):
    return [comp(lhs, rhs) for lhs, rhs in itertools.pairwise(sequence)]

def unique(iterable):
    return [group[0] for group in itertools.groupby(iterable)]

def compute_reve(sequence):
    return len(unique(pairwise_order(unique(sequence)))) - 1

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
                run = []
            direction = Direction.ASC
            run.extend([current, next])
        elif current[1] > next[1]:
            if direction == Direction.ASC:
                ascending.append(unique(run))
                run = []
            direction = Direction.DESC
            run.extend([current, next])
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


sequence =  [4, 6, 6, 6, 7, 8, 6, 4, 3, 2, 2, 5, 6, 1, 2, 7, 7, 5, 6, 8, 11, 11, 11, 9, 7, 8, 6]

diff = pairwise_order(sequence)
shadow = numpy.cumsum(diff)
neq = len([x for x in diff if x == 0]) - 1
ptp = max(shadow) - min(shadow)
amp = len(sequence) - ptp - neq - 1

reve = compute_reve(sequence)
print("Sequence:", sequence)
print("Unique(X):", unique(sequence))
print("Order(Unique(X)):", pairwise_order(unique(sequence)))
print("Unique(Order(Unique(X))):", unique(pairwise_order(unique(sequence))))
print("Reve(X):", reve)

# Fake plots to have proper labels
pyplot.plot([], label="X (ascending)", color="tab:blue")
pyplot.plot([], label="X (descending)", color="tab:orange")

# Real plots, no label
ascending, descending = split_sequence(sequence)

for group in ascending:
    pyplot.plot(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="tab:blue"
)
for group in descending:
    pyplot.plot(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="tab:orange"
    )

# Points where the direction of the growth changes
inflection_points = sorted(
    section[0] for section in itertools.chain(ascending, descending)
)[1:]

pyplot.scatter(
    list(map(operator.itemgetter(0), inflection_points)),
    list(map(operator.itemgetter(1), inflection_points)),
    facecolors="none",
    edgecolors="red",
    zorder=10,
)

pyplot.xlabel(f"Reve(X) = {reve}")
pyplot.legend()

pyplot.show()    
