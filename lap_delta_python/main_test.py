import csv
import sys
import math
import plotly.express as px
import pandas as pd
# from scipy.spatial import ConvexHull
# import numpy as np

# Open the CSV
test_file = open("./some_points2.CSV")
reader = csv.reader(test_file)

# Some holders
lat = []
lon = []
pos = []
list_of_gaps = []

is_first = True
lat_offset = 0
lon_offset = 0

# Get each cord pair with offset
for line in reader:
    if is_first:
        lat_offset = int(line[29])
        lon_offset = int(line[30])

        is_first = False

    lat.append(int(line[29]) - lat_offset)
    lon.append(int(line[30]) - lon_offset)

# The previous way that we were calculatiing the "progress" value was a simple
# function that took the current line number and divded by the total number of
# lines, this is flawed as it relies on the points being of consistent spacing
# or certain areas would get "weighted" as having more progress than they were
# actually worth, so now I am using convex hull method (making the smallest
# polygon that can enclose all the points) to get the length of the track and
# seeing where each point is along that length

# for x, y in zip(lat, lon):
#     cords.append([x, y])
#
# poly_guy = ConvexHull(cords)
#
# length = 0.0
#
# for simplex in poly_guy.simplices:
#     # Calculate the distance between each pair of consecutive hull vertices
#     p1, p2 = cords[simplex[0]], cords[simplex[1]]
#     p1, p2 = np.array(p1), np.array(p2)
#     length += np.linalg.norm(p1 - p2)
#
# print("The length of the track is about " + str(length))

# Oldest progress calc

# Calc the progress value of each point
# for line in reader:
#     if reader.line_num == 0:
#         lat_offset = int(line[29])
#         lon_offset = int(line[30])
#
#     lat.append(int(line[29]) - lat_offset)
#     lon.append(int(line[30]) - lon_offset)
#
#     pos.append(reader.line_num / pos_tot)

# Yea turns out that was stupid and over complicated, just going to use the
# same function for finding closest point to find the distance between points
# in the list


# Ok newest method, iterate thru the list and use the distance formula to find
# the length of the track, then assign a progress by divding the distance from
# the start by the total distance
cords = zip(lat, lon)
length = 0.0

for point in cords:
    if not is_first:
        pos.append(0)
        last_point = point
        is_first = True
    else:
        length += math.sqrt(sum((x - y) ** 2 for x, y in zip(last_point, point)))
        list_of_gaps.append(length)
        last_point = point

for gap in list_of_gaps:
    pos.append(gap / length)


# Try to get our progress by finding the closest point and looking at its
# progress value, this could be optimized and should be going forward
# This is an implementation of the Euclidean Distance Calculation with a linear
# search. other things to look at going forward would be k-d trees or ball trees
# to optimize the search part
min_distance = float("inf")
closest_point = None
target_point = [int(sys.argv[1]), int(sys.argv[2])]
points = zip(lat, lon, pos)

for point in points:
    distance = math.sqrt(sum((x - y) ** 2 for x, y in zip(target_point, point)))
    if distance < min_distance:
        min_distance = distance
        closest_point = point

print(closest_point)

#
##
### The rest of this is just for visuals

df = pd.DataFrame({"progress": pos, "lat": lat, "lon": lon})

fig = px.scatter(df, x="lat", y="lon", color="progress")

# Add our test point for visuals
fig.add_scatter(x=[sys.argv[1]], y=[sys.argv[2]])

fig.show()
