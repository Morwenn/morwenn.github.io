import itertools
import numpy
from matplotlib import pyplot


pyplot.subplots(figsize=(6, 3))

sequence = [4, 5, 6, 7, 8, 6, 3, 4, 6, 9, 9, 6, 5, 4, 8, 8, 12, 11, 9, 7, 8, 6]
sequence = [val - 2 for val in sequence]
pyplot.plot(sequence, color="aquamarine", ls="--")

runs = sum(
    1 for left, right in itertools.pairwise(sequence)
    if right < left
)

begin = 0
for idx, (left, right) in enumerate(itertools.pairwise(sequence)):
    if left <= right and idx != len(sequence):
        continue

    if idx == begin:
        pyplot.scatter([idx], [sequence[idx]], color="tab:blue", marker="o")
        pyplot.annotate("",
            xy=(begin-0.7, 11),
            xytext=(idx+0.7, 11),
            arrowprops={
                "arrowstyle": "<->",
                "ls": "--"
            }
        )
    elif idx == begin + 1:
        pyplot.plot(list(range(begin, idx+1)), sequence[begin:idx+1], color="tab:blue")
        pyplot.annotate("",
            xy=(begin-0.2, 11),
            xytext=(idx+0.2, 11),
            arrowprops={
                "arrowstyle": "<->",
                "ls": "--"
            }
        )
    else:
        pyplot.plot(list(range(begin, idx+1)), sequence[begin:idx+1], color="tab:blue")
        pyplot.annotate("",
            xy=(begin, 11),
            xytext=(idx, 11),
            arrowprops={
                "arrowstyle": "<->",
                "ls": "--"
            }
        )

    begin = idx + 1

# Last dot, whatever
pyplot.scatter([len(sequence) - 1], [4], color="tab:blue", marker="o")
pyplot.annotate("",
    xy=(len(sequence)-1-0.7, 11),
    xytext=(len(sequence)-1+0.7, 11),
    arrowprops={
        "arrowstyle": "<->",
        "ls": "--"
    }
)

pyplot.xlabel(f"Runs(X) = {runs+1}")

pyplot.xlim(xmin=0, xmax=len(sequence))
pyplot.ylim(ymin=0, ymax=12)
pyplot.subplots_adjust(bottom=0.2)

axes = pyplot.gca()
axes.xaxis.get_major_locator().set_params(integer=True)
axes.yaxis.get_major_locator().set_params(integer=True)


pyplot.show()    

