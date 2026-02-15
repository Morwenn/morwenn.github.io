import itertools
import numpy
from matplotlib import pyplot

def comp(lhs: int, rhs: int) -> int:
    if lhs < rhs:
        return 1
    if rhs < lhs:
        return -1
    return 0

def pairwise_order(sequence):
    return [0] + [comp(lhs, rhs) for lhs, rhs in itertools.pairwise(sequence)]

def compute_shadow(sequence):
    diff = pairwise_order(sequence)
    return numpy.cumsum(diff)

def compute_amp(sequence):
    diff = pairwise_order(sequence)
    shadow = numpy.cumsum(diff)
    neq = len([x for x in diff if x == 0]) - 1
    ptp = max(shadow) - min(shadow)
    return len(sequence) - ptp - neq - 1

# sequence = [4, 6, 6, 6, 7, 8, 6, 4, 3, 2, 5, 6, 1, 2, 7, 7, 5, 6, 8, 9, 9, 9, 8, 6, 7, 5]
# sequence = [8, 7, 6, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 13, 12, 11]  # TSB007
# sequence = [4, 6, 6, 6, 7, 8, 6, 4, 3, 2, 5, 6, 1, 2, 7, 7, 5, 6, 8, 11, 11, 11, 9, 7, 8, 6]  # TSB001
# sequence = [4, 6, 6, 6, 7, 8, 6, 4, 3, 2, 5, 6, 1, 2, 7, 6, 5, 6, 8, 11, 12, 11, 9, 7, 8, 6]  # TSB001
# sequence = [1, 2, 4, 5, 7, 8, 10, 13, 14, 15]  # TSB001
# sequence = [0, 2, 1, 4, 3, 6, 5, 8, 7, 10]  # TSB001
# sequence = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2]  # TSB001
# sequence = [1, 2, 3, 4, 5, 6, 1, 4, 2, 3]  # TSB001
# sequence = [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 10]  # TSB008
sequence = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]  # TSB008

diff = pairwise_order(sequence)
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

# sequence2 = [8, 7, 6, 5, 6, 7, 8, 9, 8, 11, 12, 13, 14, 13, 12, 11]
# shadow2 = compute_shadow(sequence2)
# ptp2 = max(shadow2) - min(shadow2)

# pyplot.plot(list(range(0, 8)), sequence[:8], dashes=[4, 4], color="tab:blue", gapcolor="tab:purple")
# pyplot.plot(list(range(7, 10)), sequence[7:10], label="X", color="tab:blue")
# pyplot.plot(list(range(7, 10)), sequence2[7:10], label="Y", color="tab:purple")
# pyplot.plot(list(range(9, len(sequence))), sequence[9:], dashes=[4, 4], color="tab:blue", gapcolor="tab:purple")

#pyplot.plot(list(range(0, 8)), shadow[:8], dashes=[4, 4], color="tab:orange", gapcolor="tab:green")
# pyplot.plot(list(range(7, len(shadow2))), shadow[7:], label="Shadow(X)", color="tab:orange")
# pyplot.plot(list(range(7, len(shadow2))), shadow2[7:], label="Shadow(Y)", color="tab:green")

# pyplot.scatter([2, 3, 15, 20, 21, 2, 3, 15, 20, 21], [6, 6, 7, 11, 11, 1, 1, 2, 4, 4], marker="x", color="red", zorder=10)
# pyplot.plot(
    # [0] + [idx for idx, (x, y) in enumerate(itertools.pairwise(shadow), start=1) if x != y],
    # [0, *(y for x, y in itertools.pairwise(shadow) if x != y)],
    # label="Rectified shadow(X)",
    # color="tab:green"
# )

pyplot.plot(sequence, label="X", color="tab:blue")
pyplot.plot(shadow, label="Shadow(X)", color="tab:orange")

graph_end = len(sequence) + 3

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

# pyplot.annotate("",
#     xy=(0, min(shadow2)),
#     xytext=(graph_end, min(shadow2)),
#     arrowprops={
#         "arrowstyle": "-",
#         "color": "green",
#         "ls": "--",
#     }
# )
# pyplot.annotate("",
#     xy=(0, max(shadow2)),
#     xytext=(graph_end, max(shadow2)),
#     arrowprops={
#         "arrowstyle": "-",
#         "color": "green",
#         "ls": "--",
#     }
# )
#
# pyplot.annotate("",
#     xy=(len(sequence), min(shadow2)),
#     xytext=(len(sequence), max(shadow2)),
#     arrowprops={
#         "arrowstyle": "<->",
#         "ls": "--"
#     }
# )
# pyplot.text(len(sequence)+0.5, (min(shadow2) + max(shadow2)) / 2, f"$PTP(Y) = {ptp2}$")

#pyplot.xlabel(f"Amp(X) = {amp}, Amp(Y) = {compute_amp(sequence2)}")

pyplot.xlim(xmin=0, xmax=graph_end)
pyplot.legend()

axes = pyplot.gca()
axes.xaxis.get_major_locator().set_params(integer=True)
axes.yaxis.get_major_locator().set_params(integer=True)

pyplot.show()    
