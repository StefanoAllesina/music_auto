import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import cv2
import numpy as np
import sys

def find_boxes(page, pagenum):
    par_threshold = 128
    horizontal_scale = 15
    min_area = 100000
    max_area = 700000
    min_height = 70
    original = cv2.imread(page)
    
    horizontal = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
    linesImg = original.copy()
    (thresh, horizontal) = cv2.threshold(horizontal, par_threshold, 255, cv2.THRESH_BINARY)
    horizontal = cv2.adaptiveThreshold(cv2.bitwise_not(horizontal), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    horizontalSize = int(horizontal.shape[1] /horizontal_scale)
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalSize,1))
    horizontal = cv2.erode(horizontal, horizontalStructure, (-1,1))
    horizontal = cv2.bitwise_not(horizontal)
    edges = cv2.Canny(horizontal,50,150,apertureSize=3)
    print(original.shape[0])
    lines = cv2.HoughLinesP(image=edges, rho=2, theta=np.pi/2, threshold=5, minLineLength=original.shape[0]/42,maxLineGap=original.shape[0]/168)
    array = []
    array.append(0)
    staffLocations = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            array.append(y1)
    array.sort()
    array.append(original.shape[0])
    index = -1
    for i in range(0,len(array)-1):
        if (array[i+1] - array[i]) > original.shape[0]/42:
            if array[i+1] > original.shape[0]/21 and array[i+1] < original.shape[0] - original.shape[0]/21:
                staffLocations.append([])
                staffLocations[index+1].append(array[i+1])
                cv2.line(linesImg, (0,array[i+1]), (original.shape[1], array[i+1]), (0,0,255), 5)
            if index != -1:
                staffLocations[index].append(array[i])
                cv2.line(linesImg, (0,array[i]), (original.shape[1], array[i]), (0,0,255), 5)
            index = index + 1
    print(staffLocations)
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Image', original)
    k = cv2.waitKey(0) & 0xFF
    cv2.imshow('Image', linesImg)
    k = cv2.waitKey(0) & 0xFF

'''     plt.imshow(original, cmap='gray')
    plt.show() '''



if __name__ == '__main__':
    cl_arguments = sys.argv
    if len(cl_arguments) < 3:
        raise ValueError("not enough arguments")
    page = cl_arguments[1]
    pagenum = cl_arguments[2]
    find_boxes(page=page, pagenum=pagenum)