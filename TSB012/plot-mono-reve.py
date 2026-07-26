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

def split_sequence_mono(sequence):
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

def split_sequence_reve(sequence):
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


sequence = [1, 5, 2, 8, 7, 5, 3, 6, 2, 6, 8, 9, 4, 5, 1, 7, 5, 2, 8, 0]

diff = pairwise_order(sequence)
shadow = numpy.cumsum(diff)
neq = len([x for x in diff if x == 0]) - 1
ptp = max(shadow) - min(shadow)
amp = len(sequence) - ptp - neq - 1

reve = compute_reve(sequence)

# Fake plots to have proper labels
pyplot.plot([], label="Ascending runs", color="tab:blue")
pyplot.plot([], label="Descending runs", color="tab:orange")

# Real plots (Mono)
ascending_runs, descending_runs = split_sequence_mono(sequence)

for group in ascending_runs:
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
for group in descending_runs:
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

for section in itertools.chain(ascending_runs, descending_runs):
    begin = section[0][0] - 0.5
    end = section[-1][0] + 0.5
    pyplot.annotate("",
        xy=(begin - 0.1, 10),
        xytext=(end + 0.1, 10),
        arrowprops={
            "arrowstyle": "<->",
            "ls": "--"
        }
    )

# Real plots (Reve)
ascending_sections, descending_sections = split_sequence_reve(sequence)

for group in ascending_sections:
    pyplot.plot(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="skyblue", ls="--",
        zorder=-1,
)
for group in descending_sections:
    pyplot.plot(
        list(map(operator.itemgetter(0), group)),
        list(map(operator.itemgetter(1), group)),
        color="bisque", ls="--",
        zorder=-1,
    )

# Points where the direction of the growth changes
inflection_points = sorted(
    section[0] for section in itertools.chain(ascending_sections, descending_sections)
)[1:]

pyplot.scatter(
    list(map(operator.itemgetter(0), inflection_points)),
    list(map(operator.itemgetter(1), inflection_points)),
    facecolors="none",
    edgecolors="red",
    s=120,
    zorder=10,
)

pyplot.xlabel(f"Mono(X) = {len(ascending_runs)+len(descending_runs)-1}, Reve(X) = {reve}")
pyplot.legend()

pyplot.xlim(xmin=-1, xmax=len(sequence))
pyplot.ylim(ymin=-2, ymax=11)
pyplot.subplots_adjust(bottom=0.2)

axes = pyplot.gca()
axes.xaxis.get_major_locator().set_params(integer=True)
axes.yaxis.get_major_locator().set_params(integer=True)

pyplot.show()    
