import os
import sys
import glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import find_lines
import csv

flowfile = "../test/Beethoven5_pages/flow.csv"

# extract name of directory
dirname = os.path.dirname(flowfile)

# boxes file
boxesfile = flowfile.replace("flow.csv", "boxes.csv")

# read the flow in a list
flow = []
with open(flowfile) as f:
    csvr = csv.reader(f)
    next(csvr, None) # skip header
    for r in csvr:
        flow.append(r)
# read boxes and make them into a dictonary of dictionaries
boxes = {}
with open(boxesfile) as f:
    csvr = csv.reader(f)
    next(csvr, None) # skip header
    for r in csvr:
        boxes[r[0]] = {"page": int(r[2]),
                       "line": int(r[1]),
                       "x": int(r[3]),
                       "y": int(r[4]),
                       "w": int(r[5]),
                       "h": int(r[6])
                        }

# number of lines per page
n = 3
# step
step = 2

lines = []
for f in flow:
    if f[1] != 'NA':
        my_box = boxes[f[1]]
        print(f, my_box)
        # extract image
        my_page = my_box['page']
        pagefile = dirname + "/pg_" + ("0000" + str(my_page))[-4:] + ".jpg"
        img = cv2.imread(pagefile)
        x = my_box['x']
        y = my_box['y']
        w = my_box['w']
        h = my_box['h']
        linename = "line_" + str(len(lines) + 1) 
        lines.append(linename + ".pdf")
        img = img[y:(y + h), x:(x + w), :]
        cv2.imwrite(linename + ".jpg", img)
        os.system("convert " + linename + ".jpg " + linename + ".pdf")
        os.system("rm " + linename + ".jpg")
    else:
        print(f[0])
