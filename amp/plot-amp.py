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

sequence = [4, 6, 6, 6, 7, 8, 6, 4, 3, 2, 5, 6, 1, 2, 7, 6, 5, 6, 8, 11, 12, 11, 9, 7, 8, 6]
sequence.reverse()
# sequence = [1, 2, 4, 5, 7, 8, 10, 13, 14, 15]
# sequence = [0, 2, 1, 4, 3, 6, 5, 8, 7, 10]
# sequence = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2]
# sequence = [1, 2, 3, 4, 5, 6, 1, 4, 2, 3]
diff = [0] + [comp(lhs, rhs) for lhs, rhs in itertools.pairwise(sequence)]
shadow = numpy.cumsum(diff)
ptp = max(shadow) - min(shadow)

print("Sequence:", sequence)
print("Order:", diff)
print("Shadow:", shadow)
print("PTP:", ptp)
print("Amp:", len(sequence) - ptp - 1)



pyplot.plot(sequence, label="X", color="tab:blue")
pyplot.plot(shadow, label="Original shadow(X)", color="tab:orange")

shadow_range = list(range(len(shadow)))
shadow_range.pop(10)
shadow = list(shadow)
shadow.pop(10)
for i in range(10, len(shadow)):
    shadow[i] -= 1
pyplot.plot(shadow_range, shadow, label="Rectified shadow(X)", color="tab:green")
pyplot.scatter([10, 10], [0, 6], marker="x", color="red", zorder=10)

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
        "color": "green",
        "ls": "--",
    }
)
pyplot.annotate("",
    xy=(0, max(shadow)),
    xytext=(graph_end, max(shadow)),
    arrowprops={
        "arrowstyle": "-",
        "color": "green",
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
pyplot.text(len(sequence), (min(shadow) + max(shadow)) / 2, "$PTP(X) = 6$")

pyplot.xlabel("Scenario 3: removing a $1$ from the pairwise order increases $PTP$")

pyplot.xlim(xmin=0, xmax=graph_end)
pyplot.legend()

pyplot.show()    

