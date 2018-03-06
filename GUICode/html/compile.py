## making it into pdf
#16:9 aspect ratio landscape

import matplotlib
matplotlib.use('TkAgg')

import os
import sys
import glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import find_lines_original as find_lines
import csv


#combines into one page. 
#Note: we assume that the user is reading the second from the top line
#So for the first page: the top line is empty.
#For the last page: Only the top and second to the top line are there. 
def combine_images_into_one_page(modifiedLines, finalImages, maxHeight, maxWidth, verticalSpaceBuffer, leftSpaceBuffer, number_lines_per_page):

    #for example, if there are 3 lines per page: maxHeight is the maximum height of all the lines. 
    #So to be conservative, the total height is 3 * maxHeight. However, we want white space between each box vertically for ease of reading.
    # If there are three boxes, there will 3 + 1 white spaces vertically added between each box. (top space, space between 1st line and 2nd line, space between 2nd and 3rd line, and space at bottom )
    totalHeight = int(maxHeight * number_lines_per_page /(1 - verticalSpaceBuffer*(number_lines_per_page+ 1)))
    totalWidth = int(maxWidth/(1 - leftSpaceBuffer))


    #the width:height ratio is 16:9
    if totalWidth/totalHeight > 16/9:
        #it's too wide, and needs to be taller to get 16:9 ratio
        totalHeight = int(totalWidth/16*9)
        
    else:
        #it's too tall, and needs to be made wider to get 16:9 ratio
        totalWidth = int(totalHeight/9 *16)

    #how much vertical space is allocated for box + white space buffer in total
    verticalSpace = int(totalHeight * verticalSpaceBuffer + maxHeight)
    leftSpace = int(leftSpaceBuffer * totalWidth)
    channels = modifiedLines[0].shape[2]

    #all the rest of the pages
    for i in range(len(modifiedLines)-1):
        page_image = np.ones((totalHeight, totalWidth, channels), np.uint8) *255
        number_lines = number_lines_per_page
 

        for j in range(number_lines):
            if (i+j) <= len(modifiedLines) -1:
                image = modifiedLines[i + j]
                height, width = image.shape[:2]
                page_image[(verticalSpace*(j+1) - height):verticalSpace*(j+1), leftSpace:width+leftSpace, :channels] = image

        finalImages.append(page_image)

#Images must have the same number of channels (1 for BW or 3 for Color)
def attach_images_horizontally(img0, img1):
    height0 = img0.shape[0]
    height1 = img1.shape[0]
    width0 = img0.shape[1]
    width1 = img1.shape[1]
    totalWidth = width0 + width1
    channels = img0.shape[2]

    #make blank white image big enough to attach two images horizontally
    combined_images = np.ones((max(height0, height1), totalWidth, channels), np.uint8) *255
    combined_images[:height0, :width0, :channels] = img0
    combined_images[:height1, width0:totalWidth, :channels] = img1
    return combined_images

###goes through all the boxes, and concantenate ones that are small to make 1 line
#the code would be a lot simplier if at most, you can concantenate two boxes horizontally
#but it's written so that more could be concantenated. 
def attach_short_lines_horizontally(images):
    total = len(images)
    modifiedImages = list()

    top_line = images[0]
    middle_line = images[1]
    bottom_line = images[2]
    i = 2

    #for the first page, the top line and middle line could be attached horizontally if short.
    #As well as the middle and bottom line. 
    while (i < total):
        if top_line.shape[1] + middle_line.shape[1] <= bottom_line.shape[1]:
            top_line = attach_images_horizontally(top_line, middle_line)
            middle_line = bottom_line
            i = i + 1
            bottom_line = images[i]
        elif middle_line.shape[1] + bottom_line.shape[1] <= top_line.shape[1]:
            middle_line = attach_images_horizontally(middle_line, bottom_line)
            i = i + 1
            bottom_line = images[i]
        else:
            break
    modifiedImages.append(top_line)
    modifiedImages.append(middle_line)
    modifiedImages.append(bottom_line)

    i = i + 1
    #for the second page and onward, the top line and middle line can't change, because
    #they were used in previous pages and are set.
    #however, if the bottom line is short, it can possibly become longer.
    #Again, this code currently allows an unlimited number of boxes to be attached horizontally.
    #it would be a lot simplier if only two could be attached. 
    while (i < total):
        top_line = middle_line
        middle_line = bottom_line
        bottom_line = images[i]


        i = i + 1
        while (i < total):
            if bottom_line.shape[1] + images[i].shape[1] <= max(top_line.shape[1], middle_line.shape[1]):
                bottom_line = attach_images_horizontally(bottom_line, images[i])
                i = i + 1
            else:
                break
        modifiedImages.append(bottom_line)
    return modifiedImages



def compile_flow(path_to_csv, path_to_jpgs, output_path_to_final_pdf, number_lines_per_page):

    boxes_images = []
    maxHeight = 0
    maxWidth = 0

    with open(path_to_csv) as f:
        # csvr = csv.reader(f)
        csvr = csv.DictReader(f)
        for r in csvr:
            x = int(r["x"])
            y = int(r["y"])
            w = int(r["w"])
            h = int(r["h"])
            page = int(r["page"])

            path_to_jpg_page = path_to_jpgs + str(page) + ".jpg"
            img = cv2.imread(path_to_jpg_page)
            img = img[y:(y + h), x:(x + w), :]
            boxes_images.append(img)

            maxHeight = max(maxHeight, h)
            maxWidth = max(maxWidth, w)

    #horizontally attaches lines if they're too small
    modifiedLines = attach_short_lines_horizontally(boxes_images)
    finalImages = []

 
    #give a minimum buffer of %5 white space between each box.
    #Note that there would be 4 white spaces vertically in total for 3 boxes
    #So it would be dumb if (num_lines_per_page + 1)* verticalSpaceBuffer > 1
    verticalSpaceBuffer = .05
    #give a buffer of 10% white space on the left
    leftSpaceBuffer = .1

    # number_lines_of_pages is how many lines per page the user wants.
    # it makes each page. 
    combine_images_into_one_page(modifiedLines, finalImages, maxHeight, maxWidth, verticalSpaceBuffer, leftSpaceBuffer, number_lines_per_page)


    string = ""
    #makes individual jpgs of eah image
    for i in range(len(finalImages)):
      string = string + output_path_to_final_pdf + "final" +str(i) + ".jpg "
      cv2.imwrite(output_path_to_final_pdf + "final" + str(i) + ".jpg", finalImages[i])

    print(string)
    os.system("convert " + string + " " + output_path_to_final_pdf +"pdf_out.pdf")
    string = string.split()

    #deletes all those jpgs
    for i in string:
        os.remove(i)



if __name__ == '__main__':
    cl_arguments = sys.argv

    path_to_csv = cl_arguments[1]
    path_to_jpgs = cl_arguments[2]
    output_path_to_final_pdf = cl_arguments[3]
    number_lines_per_page = int(cl_arguments[4])       

    compile_flow(path_to_csv, path_to_jpgs, output_path_to_final_pdf, number_lines_per_page)
    # compile_flow(filename, imageDirectory, imageName)
    print("Finished compiling!")