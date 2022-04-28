import os
import PySimpleGUI as sg
from PyPDF2 import PdfFileWriter, PdfFileReader

layout =  [[sg.In() ,
sg.FileBrowse(
    file_types=(("Text Files", "*.txt"),)
    )
    ]]

def select_pdf(message="", initial_folder=""):
    if len(initial_folder):
        path_selected = sg.popup_get_file(
            message,
            initial_folder=initial_folder,
            file_types=(("PDF Files", "*.pdf"),),         
            )  #_tkinter.TclError: bad file type "*.pdf", should be "typeName {extension ?extensions ...?} ?{macType ?macTypes ...?}?"
    else:
        path_selected = sg.popup_get_file(
            message,
            file_types=(("PDF Files", "*.pdf"),)
            )  

    if len(path_selected):
        sg.popup('You selected', path_selected)
        return path_selected
    else:
        sg.popup("Please select valid file")
        return 0

path_odd = select_pdf(message="Select pdf files that store odd pages (1,3,...,N)")
if len(path_odd):
    path_even = select_pdf(
        message="Select pdf files that store odd pages (N+1,..., 4,2)",
        initial_folder=os.path.dirname(path_odd))

pdf_odd = PdfFileReader(path_odd)
pdf_even = PdfFileReader(path_even)        

output = PdfFileWriter()

for t in range(pdf_odd.getNumPages()):
    print(f"page {t+1} of {os.path.basename(path_odd)}")
    output.addPage(pdf_odd.getPage(t))
    output.addPage(pdf_even.getPage(pdf_even.getNumPages()-t-1))

path_merged = path_even[:-4] + f"_merged_{pdf_odd.getNumPages() + pdf_even.getNumPages()}_pages.pdf"

with open(path_merged, "wb") as output_stream:
    output.write(output_stream)

assert os.path.exists(path_merged), print(f"can't save to {path_merged}")
print(f"saved to {path_merged}")

