from pdfminer.high_level import extract_pages
from pdfminer.layout import (LTTextContainer, 
                             LTRect, 
                             LTChar)
import sys
import csv
import requests


def add_text_to_cell(table: list, 
                     element: LTChar) -> None:
    """Finds the cell the text should be added to."""
    for cell in [cell for row in table for cell in row]:
        if (element.x0 >= cell['x0']
            and element.x1 <= cell['x1']
            and element.y0 >= cell['y0']
                and element.y1 <= cell['y1']):
            cell['text'] += element.get_text()

# Download 2023 table
url = ("""https://www.mass.gov/doc/"""
       """data-breach-report-2023/download""")
res = requests.get(
    url=url,
    timeout=(10, 5)
)
with open("2023.pdf", "wb") as f:
    f.write(res.content)

# Output table
table = []
# Iterate through every page
for page_layout in extract_pages("2023.pdf"):
    
    # Find the top of the table on the page
    top_of_table = sys.maxsize
    text_markers = [
        "Data Breach Notification Report", 
        "The total number of breaches affecting"]
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            if any(marker in element.get_text() 
                   for marker in text_markers): 
                if element.y0 < top_of_table:
                    top_of_table = element.y0

    # Find table bounding x and y values
    x_values = []
    y_values = []
    for element in page_layout:
        if element.y0 > top_of_table:
            continue
        if isinstance(element, LTRect):
            if element.width < 1:
                x_values.append((element.x0 + element.x1)/2)
                y_values.append(element.y0)
                y_values.append(element.y1)
            elif element.height < 1:
                x_values.append(element.x0)
                x_values.append(element.x1)
                y_values.append((element.y0 + element.y1)/2)
            else:
                x_values.append(element.x0)
                x_values.append(element.x1)
                y_values.append(element.y0)
                y_values.append(element.y1)
    x_values = sorted(list({2*round(x/2) for x in x_values}))
    y_values = sorted(list({2*round(x/2) for x in y_values}),
                      reverse=True)

    # Initialize page table
    page_table = []
    for row_no in range(len(y_values) - 1):
        row = []
        for column_no in range(len(x_values) - 1):
            row.append({'x0': x_values[column_no] - 2,
                        'x1': x_values[column_no + 1] + 2,
                        'y0': y_values[row_no + 1] - 2,
                        'y1': y_values[row_no] + 2,
                        'text': ''})
        page_table.append(row)

    # Assign text content to page table cells
    for element in page_layout:
        if element.y0 > top_of_table:
            continue
        if isinstance(element, LTTextContainer):
            for text_line in element:
                for character in text_line:
                    if isinstance(character, LTChar):            
                        add_text_to_cell(page_table, 
                                         character)

    # Build output table
    if not table:
        for row in page_table:
            table.append([cell['text'] for cell in row])
    else:
        for row in page_table[1:]:
            table.append([cell['text'] for cell in row])

# Save results to disk
with open("2023.csv",
          'wt') as year_csv:
    csv_file = csv.writer(year_csv)
    csv_file.writerow(table[0])
    for row in table[1:]:
        csv_file.writerow(row)
