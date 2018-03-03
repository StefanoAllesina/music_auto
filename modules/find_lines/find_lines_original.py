import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import cv2
import sys
import numpy as np

def find_staves(page, pagenum):
    original = cv2.imread(page)
    print(original[495][1060])
    height = original.shape[0]
    width = original.shape[1]
    par_threshold = 128
    horizontal_scale = 20
    # proportional to 100000 on a 4200 x 3200 image
    min_area = height * width / 134
    # proportional to 700000 on a 4200 x 3200 image
    max_area = height * width / 19
    # proportional to 70 on a 4200 x 3200 image
    min_height = height / 60

    horizontal = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
    (thresh, horizontal) = cv2.threshold(horizontal, par_threshold, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    horizontal = cv2.adaptiveThreshold(cv2.bitwise_not(horizontal), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    horizontalsize = int(width / horizontal_scale) 
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize,1))
    horizontal = cv2.erode(horizontal, horizontalStructure, (-1, 1))
    horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, 1))
    kernel = np.ones((40,40), np.uint8)
    horizontal = cv2.dilate(horizontal, kernel, iterations = 1)
    horizontal = cv2.bitwise_not(horizontal)

    image, contours, hier = cv2.findContours(horizontal, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours.reverse()
    boxes = []
    line_number = 0

    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        my_area = w * h
        if (my_area < max_area) and (my_area > min_area) and (h > min_height):
            line_number += 1
            boxes.append({"x": x, 
                "y": y, 
                "w": w, 
                "h": h, 
                "p": pagenum,
                "l": line_number, 
                "message": "Line " + str(line_number) + " of page " + str(pagenum)
                }) # x,y -> coordinates of top-right corner; w -> width; h -> height
    return boxes


if __name__ == '__main__':
    cl_arguments = sys.argv
    if len(cl_arguments) < 3:
        raise ValueError("not enough arguments")
    page = cl_arguments[1]
    pagenum = cl_arguments[2]
    boxes = find_staves(page, pagenum)
    for box in boxes:
        print(box)