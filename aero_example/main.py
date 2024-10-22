import sys
import csv
import math
import plotly.express as px
import pandas as pd

target_file = open("./.CSV")
reader = csv.reader(target_file)

fl = []
fr = []
rl = []
rr = []

is_first = True
