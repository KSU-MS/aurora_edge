import csv
import sys
import math

# Open the CSV
map_file = open(sys.argv[1])
header_file = open((sys.argv[1] + ".h"), "w+")
reader = csv.reader(map_file)

# Some holders
lat = []
lon = []
pos = []
progress = []

is_first = True
lat_offset = 0
lon_offset = 0

# Get each cord pair with offset
for line in reader:
    # Ignore the not locked positions
    if line[29] != 0 and line[30] != 0:
        if is_first:
            lat_offset = int(line[29])
            lon_offset = int(line[30])

            is_first = False

        lat.append(int(line[29]) - lat_offset)
        lon.append(int(line[30]) - lon_offset)

cords = zip(lat, lon)
length = 0.0

for point in cords:
    if not is_first:
        pos.append(0)
        last_point = point
        is_first = True
    else:
        length += math.sqrt(sum((x - y) ** 2 for x, y in zip(last_point, point)))
        progress.append(length)
        last_point = point

for gap in progress:
    pos.append(gap / length)
