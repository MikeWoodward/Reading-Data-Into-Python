#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 20:26:26 2017

@author: mikewoodward
"""

import glob
import csv
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import (PDFResourceManager,
                                PDFPageInterpreter)
from pdfminer.layout import (LAParams, LTTextBox,
                             LTTextLine, LTLine)
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import urllib3


def get_pdf_files(year_start, year_stop):
    """Downloads PDF files and returns a list of their names."""

    pdf_list = []

    http = urllib3.PoolManager()

    for year in range(year_start, year_stop + 1):
        # Go through the years and download the reports.

        print("Downloading file for year {0}".format(year))

        # MA changes the download label in 2019
        if year in [2021, 2020, 2019, 2017]:
            url = ("""https://www.mass.gov/doc/"""
                   """data-breach-report-{0}/download""").format(year)
        elif year in [2018, 2016, 2015, 2014, 2013, 2012, 2011,
                      2010, 2009, 2008, 2007]:
            url = ("""https://www.mass.gov/doc/"""
                   """data-breach-report-{0}-0/download""").format(year)
        r = http.request('GET', url, timeout=10)
        if r.status != 200:
            print("""Error code {0} reported downloading """
                  """file for year {1}. Skipping file """
                  """download. """.format(
                      r.status, year
                      ))
            continue
        pdf_name = "{0}.pdf".format(year)
        with open(pdf_name, "wb") as f:
            f.write(r.data)
        pdf_list.append(pdf_name)

    return pdf_list


def extract_text_lines(tree, texts, lines):
    """Gets text and line data from tree. Recursive function."""
    for branch in tree:
        if isinstance(branch, LTLine):
            lines.append(branch)
        elif isinstance(branch, LTTextLine):
            texts.append(branch)
        elif isinstance(branch, LTTextBox):
            extract_text_lines(branch, texts, lines)


def extract(tree):
    """Extracts text and line information from the layout."""
    texts = []
    lines = []

    # Extract all text and lines
    extract_text_lines(tree, texts, lines)

    # Find the upper and lower limits of the table
    top_text = "Data Breach Notification Report"
    top = [text.y0 for text in texts
           if top_text in text.get_text()][0]

    bottom_text = 'Report Ran:'
    bottom = [text.y1 for text in texts
              if bottom_text in text.get_text()]
    bottom = bottom[0] if bottom else 0

    # Filter to get the table contents only
    texts = [text for text in texts
             if text.y1 < top and text.y0 > bottom]
    lines = [line for line in lines
             if line.y1 < top and line.y0 > bottom]

    # Now, synthesize the table coordinates of the lines
    y_min = min(lines, key=lambda t: t.y0).y0
    x_min = min(lines, key=lambda t: t.x0).x0

    # ...xcol and yrow are the x and y coordinates of the cells
    xcol = [line.x0 for line in lines
            if line.x0 == line.x1 and line.y0 == y_min]
    yrow = [line.y0 for line in lines
            if line.y0 == line.y1 and line.x0 == x_min]

    # ...we need to sort the cells for more efficient
    # searching
    xcol.sort()
    yrow.sort(reverse=True)
    # ...the header row behaves differently - we need to
    # insert a dummy row to make the processing simpler
    yrow.insert(1, yrow[1])

    # Sort the text - we need this later for multi-line
    # text
    texts.sort(key=lambda item: (-item.y0, item.x0))

    return texts, xcol, yrow


def transform(content, xcol, yrow):
    """Transforms the text and line data into a table"""

    # Initialize the table with empty strings
    table = [['']*(int(len(xcol)/2))
             for x in range(int(len(yrow)/2))]

    # Loop through every item of text, finding the row
    # and column it's in.
    for item in content:

        # Get the table column index
        for index in range(0, len(xcol), 2):
            if item.x0 > xcol[index] and \
               item.x0 < xcol[index+1]:
                c = int(index/2)
                break

        # Get the table row index
        for index in range(0, len(yrow), 2):
            if item.y0 < yrow[index] and \
               item.y0 > yrow[index+1]:
                r = int(index/2)
                break

        # Add the text to what's already in the table.
        # This only works with multi-line text because
        # of the ordering(sort) done earlier.
        table[r][c] += item.get_text().replace('\n', '')

    return table[1:], table[0]


class PDFProcessor():

    """Class to handle PDFMiner operations"""

    def __init__(self):
        """Sets up the PDFMiner to interpret the PDF files"""
        resource_manager = PDFResourceManager()
        laparams = LAParams()

        self.device = PDFPageAggregator(resource_manager,
                                        laparams=laparams)
        self.interpreter = PDFPageInterpreter(resource_manager,
                                              self.device)

    def doc_init(self, pdf_name):
        """Initialization for each new document"""
        pdf_file = open(pdf_name, "rb")
        pdf_parser = PDFParser(pdf_file)
        self.pdf_doc = PDFDocument(pdf_parser)

        print("\nPDF metadata for {0}".format(pdf_name))
        print(self.pdf_doc.info)

        if not self.pdf_doc.is_extractable:
            return False

        self.pages = PDFPage.create_pages(self.pdf_doc)
        return True

    def get_layout(self, page):
        """Processes each page and returns layout"""
        self.interpreter.process_page(page)
        return self.device.get_result()


if __name__ == "__main__":
    # Copy the PDF files from the website
    brch_files = get_pdf_files(2007, 2021)

    brch_files = sorted(glob.glob("*.pdf"))

    pdf_processor = PDFProcessor()

    # Loop through each of the files
    for brch_file in brch_files:

        # List that contains all the breaches for the year
        breach_year = []

        # If we can't initialize the file, process the
        # next file
        if not pdf_processor.doc_init(brch_file):
            continue

        # Process each page in the PDF
        for page in pdf_processor.pages:
            layout = pdf_processor.get_layout(page)
            content, xcol, yrow = extract(layout)
            breach_page, header = transform(content,
                                            xcol,
                                            yrow)
            breach_year.append(breach_page)

        # Write the results to disk
        with open(brch_file.replace('.pdf', '.csv'), 
                  'wt') as year_csv:
            csv_file = csv.writer(year_csv)
            csv_file.writerow(header)
            for page in breach_year:
                for row in page:
                    csv_file.writerow(row)
