import sys
import os
import csv
from PyPDF2 import PdfFileReader, PdfFileWriter

# Function that converts a page from pdf to jpg
def convert_page(ff):
    #print("converting to jpg file " + ff + "...", end = "\r")
    os.system("convert -density 300 " + ff + " " + ff[:-4] + ".jpg")
    # remove the pdf as we don't need it anymore
    os.system("rm " + ff)
    return 0

# Main function of this file

#replaced filename with path_to_pdf

def split_and_convert(path_to_pdf, output_folder, debug = False):
    reader = PdfFileReader(stream=os.path.abspath(path_to_pdf))
    for i in range(0, reader.numPages):
        page = reader.pages[i]
        if debug:
            print('Converting page: ' + str(i))
        writer = PdfFileWriter()
        writer.addPage(page)
        outputPath = os.path.abspath(output_folder)
        outputFile = outputPath + '/' + str(i) + '.pdf'
        f = open(file=outputFile, mode='wb')
        writer.write(f)
        f.close()
        convert_page(outputFile)

    return reader.numPages


#This is  for when the script is imported
def mainFunction(path_to_pdf, output_folder): 
    '''
    arg[0] = pdf that is multiple pages long
    arg[1] = folder that you want to place it in
    '''
    numPages = split_and_convert(filename=path_to_pdf, outputfolder=output_folder, debug=True)
    print("Finished splitting the file!")
    return numPages    

if __name__ == '__main__':
    cl_arguments = sys.argv
    if len(cl_arguments) < 3:
        raise ValueError("not enough arguments")
    else:
        path_to_pdf = cl_arguments[1]
        output_folder = cl_arguments[2]
        split_and_convert(path_to_pdf, output_folder, debug=True)
        print("Finished splitting the file!")

