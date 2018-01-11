import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import cv2
import numpy as np


def find_boxes(page, pagenum):
    par_threshold = 128
    horizontal_scale = 20
    min_area = 100000
    max_area = 700000
    min_height = 70
    original = cv2.imread(page,0)



if __name__ == '__main__':
    cl_arguments = sys.argv
    if len(cl_arguments) < 3:
        raise ValueError("not enough arguments")
    page = cl_arguments[1]
    pagenum = cl_arguments[2]
    find_boxes(page=page, pagenum=pagenum)