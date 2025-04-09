from bs4 import BeautifulSoup
import urllib.robotparser
from csv import writer
from re import sub
import requests
import sys

# OK to scrape page?
# ==================
rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://en.wikipedia.org/robots.txt")
rp.read()
scrape_ok = rp.can_fetch(
    'Python User Agent example',
    "https://en.wikipedia.org/robots.txt")
if scrape_ok:
    print("OK to scrape page")
else:
    sys.exit(0)


# Getting web page data
# =====================
url = 'https://en.wikipedia.org/wiki/' \
      'List_of_tallest_buildings_and_structures'
headers = {'User-Agent': 'Python User Agent example'}
try:
    response = requests.get(url,
                            headers=headers,
                            timeout=10)
except requests.ConnectionError as e:
    print('Couldn\'t reach the server.')
    print('Reason: ', e)
    sys.exit(1)
except requests.Timeout as e:
    print('Timeout error.')
    print('Reason: ', e)
    sys.exit(1)
print(response.headers)
print(response.status_code)
html = response.text

# Parse web data
# ==============
soup = BeautifulSoup(html, 'html.parser')
table = soup.find_all('table')[2]
rows = table.find_all('tr')

buildings = []

# Headings
buildings.append([header.string
                  for header in rows[0].find_all('th')])

# Parse data
for row in rows[1:]:
    items = row.find_all('td')
    line1 = [sub(r'\[\d+\]', r'', item.text.strip())
             for item in items[:-1]]
    loc = items[-1].find('span', {'class': 'geo'})
    loc_text = '' if loc is None else loc.text.strip()

    buildings.append(line1 + [loc_text])

# Output data
# ===========
with open("buildings.csv", 'w') as file_obj:
    csv_file = writer(file_obj)
    for row in buildings:
        row = [s.encode('utf-8') for s in row]
        csv_file.writerow(row)
