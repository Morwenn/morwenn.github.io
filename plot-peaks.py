import itertools
import numpy
from matplotlib import pyplot

def count_drops_from_peak(sequence):
    peaks = 0
    max_i = 0
    for i, elem in enumerate(sequence):
        if elem >= sequence[max_i]:
            peaks += 1
            max_i = i
    return len(sequence) - peaks

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
print("Drops:", count_drops_from_peak(sequence))



pyplot.plot(sequence, label="X", color="tab:blue")

shadow_range = list(range(len(shadow)))
shadow_range.pop(10)
shadow = list(shadow)
shadow.pop(10)
for i in range(10, len(shadow)):
    shadow[i] -= 1
pyplot.scatter([0, 1, 4, 5, 19, 20], [4, 6, 7, 8, 11, 12], marker="o", color="red", zorder=10)
pyplot.scatter([2, 3, 18], [6, 6, 8], marker="o", color="orange", zorder=10)


pyplot.annotate("",
    xy=(len(sequence)-0.5, min(shadow)),
    xytext=(len(sequence)-0.5, max(shadow)),
    arrowprops={
        "arrowstyle": "<->",
        "ls": "--"
    }
)

pyplot.xlabel("Disorder(X) = $|X| - N_{peaks} = 26 - 6 = 20$ (or $26 - 9 = 17$ counting equal elements)")

pyplot.show()    

