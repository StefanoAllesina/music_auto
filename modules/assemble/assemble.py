import sys
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import csv

def convert_page(ff):
    os.system("convert " + ff + " " + ff[:-4] + ".pdf")
    return ff[:-4] + '.pdf'

def assemble(pageOrderFile, outName):
    with open(pageOrderFile) as f:
        reader = csv.DictReader(f)
        writer = PdfFileWriter()
        output = open(outName, mode='wb')
        for row in reader:
            file = os.path.dirname(pageOrderFile) + "/" + row['filename']
            page = convert_page(file)
            pdfr = PdfFileReader(page)
            writer.addPage(pdfr.pages[0])
            pdfr = None
            os.system("rm " + page)
        writer.write(output)
        output.close()
if __name__ == '__main__':
    cl_arguments = sys.argv
    if len(cl_arguments) < 3:
        raise ValueError("not enough arguments")
    pageOrderFile = cl_arguments[1]
    outName = cl_arguments[2]
    assemble(pageOrderFile, outName)
