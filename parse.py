import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import re

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

reboots = ["2025/01/20 23:01:00", "2025/01/27 23:01:00", "2025/02/03 23:01:00", "2025/02/10 23:01:00", "2025/02/14 13:39:00", "2025/02/14 13:43:00", "2025/02/17 23:01:00"]
markers= [pd.Timestamp(x) for x in reboots]
series = pd.Series(series_data, series_index).sort_index()

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