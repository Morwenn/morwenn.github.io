
import colorsys
import matplotlib
import numpy
import sys
from matplotlib import pyplot
from pathlib import Path


def adjust_color(color, scale):
    rgb = matplotlib.colors.to_rgb(color)
    # convert rgb to hls
    h, l, s = colorsys.rgb_to_hls(*rgb)
    # manipulate h, l, s values and return as rgb
    return colorsys.hls_to_rgb(h, min(1, l * scale), s = s)


datasets = {}

for file in sys.argv[1:]:
    name = Path(file).stem
    with open(file) as fd:
        data = fd.read().strip()
    datasets[name] = numpy.array(list(map(int, data.split())))


# Colorblind-friendly palette (https://gist.github.com/thriveth/8560036)
palette = ['#377eb8', '#ff7f00', '#4daf4a',
           '#f781bf', '#a65628', '#984ea3',
           '#999999', '#e41a1c', '#dede00']
colour = iter(palette)

for idx, (name, dataset) in enumerate(datasets.items(), 1):
    boxes = pyplot.boxplot(
        [dataset],
        positions=[len(datasets) - idx],
        vert=False,
        widths=[0.3],
        label=[name],
        patch_artist=True,
    )

    col = next(colour)
    for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        pyplot.setp(boxes[item], color=adjust_color(col, 0.7))
    pyplot.setp(boxes["boxes"], facecolor=adjust_color(col, 1.3))
    pyplot.setp(boxes["fliers"], markeredgecolor=adjust_color(col, 1.3))

pyplot.yticks(list(reversed([idx for idx in range(len(datasets))])),
              datasets.keys(), horizontalalignment='right')

pyplot.xlabel("Time [µs] (lower is better)")
pyplot.title("Running move_to on a tree of $50000$ elements")

pyplot.show()
