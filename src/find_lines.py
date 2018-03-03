import os
import sys
import glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import re

def press(event):
    print('press', event.key)
    sys.stdout.flush()
    if event.key=='x':
        visible = xl.get_visible()
        xl.set_visible(not visible)
        fig.canvas.draw()


def show_image(img, lab = 'this is a test', myscale = 0.6, cmap = 'gray'):
    """
    show an image, rescaled so that it fits the screen
    pressing the x button closes the image
    """
    imS = cv2.resize(img, (int(img.shape[1] * myscale), int(img.shape[0] * myscale))) 
    fig, ax = plt.subplots() 
    fig.canvas.mpl_connect('key_press_event', press)
    im = ax.imshow(imS, cmap=cmap)
    plt.show()

def find_boxes(page, par_threshold = 128, 
               horizontal_scale = 20, min_area = 100000, max_area = 700000,
               min_height = 70,
               debug = "save"):
    #################################################
    # Tunable parameters:
    # par_threshold  to determine what is black
    # horizontal_scale note: if I use a value > 30, I capture also some notes;  if much lower, I lose some lines
    # min_area min area in pixels for a staff
    # max_area max area in pixels for a staff
    # min_height min height to have a staff
    #################################################
    # step 1: find approximate location of staffs
    #################################################
    # strategy: 
    # remove vertical things 
    # expand the pixels so that the staff becomes a big rectangle
    original = cv2.imread(page,0)
    horizontal = original.copy()
    (thresh, horizontal) = cv2.threshold(horizontal, par_threshold, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    horizontal = cv2.adaptiveThreshold(cv2.bitwise_not(horizontal), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    horizontalsize = int(horizontal.shape[1] / horizontal_scale) 
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize,1))
    horizontal = cv2.erode(horizontal, horizontalStructure, (-1, 1))
    horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, 1))
    kernel = np.ones((40,40), np.uint8)
    horizontal = cv2.dilate(horizontal, kernel, iterations = 1)
    horizontal = cv2.bitwise_not(horizontal)
    # now the image contains large rectangle-like blobs
    if debug == "show":
        show_image(horizontal)

    # find the enclosing rectangles
    # filter those that are too small (or too large)
    #################################################
    # step 2: find bounding rectangles
    #################################################
    # strategy: 
    # use findContours to find all contours
    # find the bounding rectangle for each contour
    # if the area seems right, keep, otherwise discard
    # find contours
    image, contours, hier = cv2.findContours(horizontal, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # reverse contours so that it starts from the top
    contours.reverse()
    # This is where we store the boxes
    boxes = []
    # find page number
    page_number = int(os.path.basename(page).split("_")[1].split(".")[0])
    line_number = 0

    if debug == "show":
        # store image with contours drawn
        withlines = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR) 
    for i, c in enumerate(contours):
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        my_area = w * h
        if (my_area < max_area) and (my_area > min_area) and (h > min_height):
            line_number = line_number + 1 
            boxes.append({"x": x, 
                          "y": y, 
                          "w": w, 
                          "h": h, 
                          "p": page_number,
                          "l": line_number, 
                          "message": "Line " + str(line_number) + " of page " + str(page_number)
                         }) # x,y -> coordinates of top-right corner; w -> width; h -> height
            if debug == "show":
                print(i, my_area)
                # draw a green rectangle to visualize the bounding rect
                cv2.rectangle(withlines, (x, y), (x+w, y+h), (0, 255, 255), 60)   
    if debug == "show":
        show_image(withlines)
    ##############################################################
    # step 3: adjust boxes height to include what is cut...
    ##############################################################
    # TODO: for now just add a little bit 
    if debug == "show" or debug == "save":
        # store image with contours drawn
        withlines = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR) 
    fudge = 40
    for b in boxes:
        b["y"] = b["y"] - fudge
        b["h"] = b["h"] + 2 * fudge
        if debug == "show" or debug == "save":
            cv2.rectangle(withlines, (b["x"], b["y"]), (b["x"]+b["w"], b["y"]+b["h"]), (255, 0, 0), 4)   
    ##############################################################
    # optional: save results for debugging
    ##############################################################
    if debug == "show":
        show_image(withlines)
    if debug == "save":
        cv2.imwrite(page.replace("_pages", "_debug"), withlines)
    return boxes

if __name__ == '__main__':
    page = "../misc/pg_0008.jpg"
    find_boxes(page, debug = True)
