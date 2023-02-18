import datetime
import re
import os
import PyPDF2
import base64

import io

import re
from string import punctuation
from heapq import nlargest

from dash import Dash, dash_table, dcc, html, Output, Input, State

directory = '/home/billel/resume-screening-nlp/data'

class pdfReader:
    def __init__(self, file_path: str) -> str:
        self.file_path = file_path

    def PDF_one_pager(self) -> str:
        """A function that returns a one line string of the
            pdfReader object.

            Parameters:
            file_path(str): The file path to the pdf.

            Returns:
            one_page_pdf (str): A one line string of the pdf.

        """
        content = ""
        p = open(self.file_path, "rb")
        pdf = PyPDF2.PdfReader(p)
        num_pages = len(pdf.pages)
        for i in range(0, num_pages):
            content += pdf.pages[i].extract_text() + "\n"
        content = " ".join(content.replace(u"\xa0", " ").strip().split())
        page_number_removal = r"\d{1,3} of \d{1,3}"
        page_number_removal_pattern = re.compile(page_number_removal, re.IGNORECASE)
        content = re.sub(page_number_removal_pattern, '', content)

        return content

    def pdf_reader(self) -> str:
        """A function that can read .pdf formatted files
            and returns a python readable pdf.

            Returns:
            read_pdf: A python readable .pdf file.
        """
        opener = open(self.file_path, 'rb')
        read_pdf = PyPDF2.PdfReader(opener)

        return read_pdf



def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[0]
    with open(os.path.join(directory, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    save_file(filename, content_string)
    decoded = base64.b64decode(content_string)
    try:
        if 'pdf' in filename:
            pdf = pdfReader(directory + '/' + filename)
            text = pdf.PDF_one_pager()
    except Exception as e:
        print(e)
    return text
