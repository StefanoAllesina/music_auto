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
def split_and_convert(filename, outputfolder, debug = False):
    reader = PdfFileReader(stream=os.path.abspath(filename))
    fileN = outputfolder + '/' + 'order_of_pages.csv'
    
    with open(fileN, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for i in range(0, reader.numPages):
            

            page = reader.pages[i]
            if debug:
                print('Converting page: ' + str(i))
            writer = PdfFileWriter()
            writer.addPage(page)
            outputPath = os.path.abspath(outputfolder)
            # outputFile = outputPath + '/' + os.path.basename(filename)[:-4] + '_' + str(i) + '.pdf'
            # wr.writerow([i, os.path.basename(filename)[:-4] + '_' + str(i) + '.jpg'])
            outputFile = outputPath + '/' + 'page'+ '_' + str(i) + '.pdf'
            wr.writerow([i, 'page' + '_' + str(i) + '.jpg'])

            f = open(file=outputFile, mode='wb')
            writer.write(f)
            f.close()
            convert_page(outputFile)

    return reader.numPages


#This is  for when the script is imported
def mainFunction(multiplePagesPDF, folder): 
    '''
    arg[0] = pdf that is multiple pages long
    arg[1] = folder that you want to place it in
    '''
    filename = multiplePagesPDF
    outputfolder = folder
    numPages = split_and_convert(filename=filename, outputfolder=outputfolder, debug=True)
    print("Finished splitting the file!")
    return numPages    

if __name__ == '__main__':
    cl_arguments = sys.argv
    if len(cl_arguments) < 3:
        raise ValueError("not enough arguments")
    else:
        filename = cl_arguments[1]
        outputfolder = cl_arguments[2]
        split_and_convert(filename=filename, outputfolder=outputfolder, debug=True)
        print("Finished splitting the file!")

