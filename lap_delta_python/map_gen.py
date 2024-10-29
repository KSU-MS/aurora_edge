import csv
import sys
import math

# Open the CSV
map_file = open(sys.argv[1])
output_file = sys.argv[1].removesuffix(".CSV") + ".hpp"
reader = csv.reader(map_file)

# Some holders
lat = []
lon = []
progress = []
pos = []


# Get each cord pair
for line in reader:
    # Ignore the not locked positions
    if line[29] != 0 and line[30] != 0:
        lat.append(int(line[29]))
        lon.append(int(line[30]))

# Combine both lists
cords = zip(lat, lon)

length = 0.0  # length of the track
is_first = True

# Determine the length of the track
for point in cords:
    if is_first:
        is_first = False
        progress.append(0.0)
        last_point = point

    else:
        length += math.sqrt(sum((x - y) ** 2 for x, y in zip(last_point, point)))
        progress.append(length)

        last_point = point

# Now normalize the position value based on the distance from start as 0 - 65535
for i, distance in enumerate(progress):
    pos.append((lat[i], lon[i], (int(round((distance / length) * 65535)))))


# Start the header file output
with open((output_file), "w") as f:
    f.write("#ifndef " + output_file + "\n")
    f.write("#define " + output_file + "\n\n")

    f.write("// Generated list of points\n")
    f.write(f"const int num_points = {len(pos)};\n")
    f.write(
        "const struct Point {\n"
        + "    int32 lat;\n"
        + "    int32 lon;\n"
        + "    uint16 prg;\n"
        + "} points[] = {\n"
    )

    for lat, lon, prg in pos:
        f.write(f"    {{{lat}, {lon}, {prg}}},\n")

    f.write("};\n\n")
    f.write("#endif //" + output_file)
