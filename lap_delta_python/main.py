import csv
import os
import plotly.express as px
import pandas as pd

if __name__ == "__main__":
    test_file = open("./some_points.CSV")
    reader = csv.reader(test_file)

    lat = []
    lon = []
    pos = []

    pos_tot = 810
    pos_val = 0

    lat_offset = 0
    lon_offset = 0

    # for line in reader:
    #     pos_tot += 1

    for line in reader:
        if pos_val == 0:
            lat_offset = int(line[29])
            lon_offset = int(line[30])

        lat.append(int(line[29]) - lat_offset)
        lon.append(int(line[30]) - lon_offset)

        pos.append(pos_val / pos_tot)
        pos_val += 1

    df = pd.DataFrame({"progress": pos, "lat": lat, "lon": lon})

    fig = px.scatter(df, x="lat", y="lon", color="progress")

    # Add our test point for visuals
    fig.add_scatter(x=[6], y=[5])

    fig.show()
