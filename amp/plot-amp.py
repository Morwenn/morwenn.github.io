import itertools
import numpy
from matplotlib import pyplot

def comp(lhs: int, rhs: int) -> int:
    if lhs < rhs:
        return 1
    if rhs < lhs:
        return -1
    return 0

def compute_amp(sequence):
    diff = [0] + [comp(lhs, rhs) for lhs, rhs in itertools.pairwise(sequence)]
    shadow = numpy.cumsum(diff)
    ptp = max(shadow) - min(shadow)
    return len(sequence) - ptp - 1

sequence = [4, 6, 6, 6, 7, 8, 6, 4, 3, 2, 5, 6, 1, 2, 7, 7, 5, 6, 8, 11, 11, 11, 9, 7, 8, 6]
sequence.reverse()
# sequence = [4, 6, 6, 6, 7, 8, 6, 4, 3, 2, 5, 6, 1, 2, 7, 6, 5, 6, 8, 11, 12, 11, 9, 7, 8, 6]  # TSB001
# sequence = [1, 2, 4, 5, 7, 8, 10, 13, 14, 15]  # TSB001
# sequence = [0, 2, 1, 4, 3, 6, 5, 8, 7, 10]  # TSB001
# sequence = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2]  # TSB001
# sequence = [1, 2, 3, 4, 5, 6, 1, 4, 2, 3]  # TSB001



diff = [0] + [comp(lhs, rhs) for lhs, rhs in itertools.pairwise(sequence)]
shadow = numpy.cumsum(diff)
neq = len([x for x in diff if x == 0]) - 1
ptp = max(shadow) - min(shadow)
amp = len(sequence) - ptp - neq - 1

print("Sequence:", sequence)
print("Order(X):", diff)
print("Shadow(X):", shadow)
print("len(X):", len(sequence))
print("Neq(X):", neq)
print("PTP(X):", ptp)
print("Amp(X):", amp)



pyplot.plot(sequence, label="X", color="tab:blue")
pyplot.plot(shadow, label="Shadow(X)", color="tab:orange")

# pyplot.scatter([2, 3, 15, 20, 21, 2, 3, 15, 20, 21], [6, 6, 7, 11, 11, 1, 1, 2, 4, 4], marker="x", color="red", zorder=10)
# pyplot.plot(
    # [0] + [idx for idx, (x, y) in enumerate(itertools.pairwise(shadow), start=1) if x != y],
    # [0, *(y for x, y in itertools.pairwise(shadow) if x != y)],
    # label="Rectified shadow(X)",
    # color="tab:green"
# )

graph_end = len(sequence) + 5

pyplot.annotate("",
    xy=(0, min(shadow)),
    xytext=(graph_end, min(shadow)),
    arrowprops={
        "arrowstyle": "-",
        "color": "orange",
        "ls": "--",
    }
)
pyplot.annotate("",
    xy=(0, max(shadow)),
    xytext=(graph_end, max(shadow)),
    arrowprops={
        "arrowstyle": "-",
        "color": "orange",
        "ls": "--",
    }
)

pyplot.annotate("",
    xy=(len(sequence)-0.5, min(shadow)),
    xytext=(len(sequence)-0.5, max(shadow)),
    arrowprops={
        "arrowstyle": "<->",
        "ls": "--"
    }
)
pyplot.text(len(sequence), (min(shadow) + max(shadow)) / 2, f"$PTP(X) = {ptp}$")

pyplot.xlabel(f"Random sequence, Amp(X) = {amp}")

pyplot.xlim(xmin=0, xmax=graph_end)
pyplot.legend()

pyplot.show()    

