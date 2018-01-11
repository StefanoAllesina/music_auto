import sys
import os
from PyPDF2 import PdfFileReader, PdfFileWriter


def convert_page(ff):
    #print("converting to jpg file " + ff + "...", end = "\r")
    os.system("convert -density 300 " + ff + " " + ff[:-4] + ".jpg")
    # remove the pdf as we don't need it anymore
    os.system("rm " + ff)
    return 0

def split_and_convert(filename, outputfolder, debug = False):
    reader = PdfFileReader(stream=os.path.abspath(filename))
    for i in range(0, reader.numPages):
        page = reader.pages[i]
        if debug:
            print('Converting page: ' + str(i))
        writer = PdfFileWriter()
        writer.addPage(page)
        outputPath = os.path.abspath(outputfolder)
        outputFile = outputPath + '/' + os.path.basename(filename)[:-4] + '_' + str(i) + '.pdf'
        f = open(file=outputFile, mode='wb')
        writer.write(f)
        f.close()
        convert_page(outputFile)

if __name__ == '__main__':
    cl_arguments = sys.argv
    if len(cl_arguments) < 2:
        raise ValueError("not enough arguments")
    else:
        filename = cl_arguments[1]
        outputfolder = cl_arguments[2]
        split_and_convert(filename=filename, outputfolder=outputfolder, debug=True)
        print("Finished splitting the file!")



