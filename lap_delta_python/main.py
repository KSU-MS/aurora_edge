import csv
import sys
import plotly.express as px
import pandas as pd
import math

if __name__ == "__main__":
    # Open the CSV
    test_file = open("./some_points.CSV")
    reader = csv.reader(test_file)

    # Some holders
    lat = []
    lon = []
    pos = []

    lat_offset = 0
    lon_offset = 0

    # TODO: Need to auto fetch this
    pos_tot = 810
    pos_val = 0

    # for line in reader:
    #     pos_tot += 1

    # Get each cord pair with offset accounted for and calc the progress val
    for line in reader:
        if pos_val == 0:
            lat_offset = int(line[29])
            lon_offset = int(line[30])

        lat.append(int(line[29]) - lat_offset)
        lon.append(int(line[30]) - lon_offset)

        pos.append(pos_val / pos_tot)
        pos_val += 1

    # Try to get our progress by finding the closest point and looking at its
    # progress value, this could be optimized and should be going forward
    # This is an implementation of the Euclidean Distance Calculation with a linear
    # search other things to look at going forward would be k-d trees or ball trees
    # to optimize the search part
    min_distance = float("inf")
    closest_point = None
    points = zip(lat, lon, pos)
    target_point = [int(sys.argv[1]), int(sys.argv[2])]

    for point in points:
        # distance = euclidean_distance(given_point, point)
        distance = math.sqrt(sum((x - y) ** 2 for x, y in zip(target_point, point)))
        if distance < min_distance:
            min_distance = distance
            closest_point = point

    print(closest_point)

    #
    ## The rest of this is just for visuals
    #

    df = pd.DataFrame({"progress": pos, "lat": lat, "lon": lon})

    fig = px.scatter(df, x="lat", y="lon", color="progress")

    # Add our test point for visuals
    fig.add_scatter(x=[sys.argv[1]], y=[sys.argv[2]])

    fig.show()
