from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import re

# `sar -r` data into pandas Series for line plot
series_data = []
series_index = []

for file in Path("./data").glob("sar*.txt"):
    with open(file) as log:
        blocks = log.read().split("\n\n")
        date = re.match(r".*(\d+\/\d+\/\d+).*", blocks[0])[1]
        rows = blocks[1].split("\n")[1:-2]
        data = list(map(lambda x: list(filter(lambda y: y != "", x.split(" "))), rows))

        for d in data:
            time = d[0]
            usage = d[4]

            series_data.append(float(usage))
            series_index.append(pd.Timestamp(f"{date} {time}"))

series = pd.Series(series_data, series_index).sort_index()

# `last` system boot data into a pandas Series for scatter plot
year = datetime.now().year # super horrible I know...
reboots = []

with open("./data/reboots.txt") as log:
    lines = log.read().split("\n")
    for line in lines[:-1]:
        parse = list(filter(lambda x: x != "", re.match(r"reboot   system boot  .*-azur .{3} (.{3} [\d ]{1,2} [\d:]{4,5}).*", line)[1].split(" ")))
        date = f"{parse[0]} {parse[1]} {year} {parse[2]}"
        reboots.append(date)

markers = [pd.Timestamp(x) for x in reboots]


# plotting
plt.figure()
fig, ax = plt.subplots()
fig.set_size_inches(12, 6)

series.plot()
plt.scatter(markers, [0 for _ in range(len(markers))], c="red", label="reboots")

plt.title("CSCTCloud %memusage")
plt.legend()
ax.xaxis.set_minor_locator(mdates.DayLocator())
ax.grid(which="both", axis="x")

plt.savefig("output.png")