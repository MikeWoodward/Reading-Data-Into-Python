from bs4 import BeautifulSoup
import urllib.robotparser
from csv import writer
from re import sub
import requests
import sys

user_agent_string = "Python User Agent"
wikipedia_page = (
  "https://en.wikipedia.org/wiki/List_of_tallest_buildings")

# OK to scrape page?
# ==================
print("Checking robots.txt")
print("-------------------")
r = requests.get(
    "https://en.wikipedia.org/robots.txt",
    headers={"User-Agent": user_agent_string}
)
rp = urllib.robotparser.RobotFileParser()
rp.parse(r.text.splitlines())
scrape_ok = rp.can_fetch(user_agent_string, 
                         wikipedia_page)
if not scrape_ok:
  print("Not allowed to scrape page")
  sys.exit(1)
else:
  print("Allowed to scrape page")


# Getting web page data
# =====================
print("Getting web page")
print("----------------")
try:
    response = requests.get(url=wikipedia_page,
                            headers={'User-Agent': 
                                     user_agent_string},
                            timeout=10)
except requests.ConnectionError as e:
    print('Couldn\'t reach the server.')
    print('Reason: ', e)
    sys.exit(1)
except requests.Timeout as e:
    print('Timeout error.')
    print('Reason: ', e)
    sys.exit(1)
print("Headers:")
print(response.headers)
print("Status code:")
print(response.status_code)
html = response.text

# Parse web data
# ==============
print('Pasing web page')
print('---------------')
soup = BeautifulSoup(html, 'html.parser')
table = soup.find_all('table')[1]
rows = table.find_all('tr')

# Headings
headers = []
for heading in rows[0].find_all("th"):
  # Parse headers that span one column
  if int(heading.get('colspan', 1)) == 1:
    headers.append(sub(r'\[\d+\]', 
                      r'', 
                      heading.text.strip()))
  # Parse headers that span two columns
  elif int(heading.get('colspan', 1)) == 2: 
    # Parse the subheader from the next row
    for sub_head in [h.text.strip() 
                     for h in rows[1].find_all("th")]:
      text = sub(r'\[\d+\]', r'', heading.text.strip())
      headers.append(f"{text} ({sub_head})")
      
# Set up the grid data structure
column_count = len(headers)
row_count = len(rows[1:])
# Pre-allocate grid, note row size
grid = [[None for _ in range(column_count)] 
        for _ in range(row_count)]

# Add header to grid
for col_index, header in enumerate(headers):
  grid[0][col_index] = header
  
# Parse data into grid
# Loop through every data row
for row_index, row in enumerate(rows[2:], start = 1):
  elements = row.find_all('td')
  # Loop through every element in row
  for element_index, element in enumerate(elements):
    element_text = sub(r'\[\d+\]', 
                       r'', 
                       element.text.strip())
    # Insert into first non-None column
    for col_index in range(element_index, column_count):
      if grid[row_index][col_index] is None:
        grid[row_index][col_index] = element_text
        break
    # Row span - paste value into appropriate column
    row_span = int(element.get('rowspan', 1)) 
    if row_span > 1:
       for i in range(1, row_span):
         if row_index + i < row_count: 
           grid[row_index + i][col_index] = element_text

# Output data
# ===========
print('Writing output')
print('--------------')
with open("buildings.csv", 'w') as file_obj:
    csv_file = writer(file_obj)
    for row in grid:
        csv_file.writerow(row)
