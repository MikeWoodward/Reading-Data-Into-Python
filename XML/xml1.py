#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 16:23:52 2025

@author: mikewoodward
"""

# %%---------------------------------------------------------------------------
# Module metadata
# -----------------------------------------------------------------------------
__author__ = "mikewoodward"
__license__ = "MIT"
__summary__ = "One line summary"

# %%---------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import lxml
import requests
import zipfile

url = ("https://api.worldbank.org/v2/en/"""
       """indicator/SP.POP.TOTL"""
       """?downloadformat=xml""")

# Download the file
res = requests.get(
    url=url,
    timeout=10)
with open('population.zip',
          'wb') as xml_file:
    xml_file.write(res.content)
# Unzip the XML
with zipfile.ZipFile('population.zip',
                     'r') as zf:
    zip_file_names = zf.namelist()
    zf.extractall()

# Open the XML file and parse it
tree = lxml.etree.parse(zip_file_names[0])

# Get document information
print('Document information')
print('--------------------')
print("XML version: "
      f"{tree.docinfo.xml_version}")
print("XML encoding: "
      f"{tree.docinfo.encoding}")
print()

# Completely parse the first element
root = tree.getroot()
children = root.getchildren()[0].getchildren()

# Report on elements
print("""There are """
      f"""{len(children)} children.""")
print()
print('11th child')
print('----------')
element = 10
child = children[element].getchildren()
print("""Country code: """
      f"""{child[0].attrib['key']}""")
print(f"""Country name: {child[0].text}""")
print(f"""Year: {child[2].text}""")
print(f"""Population: {child[3].text}""")

# Iterate through entire tree finding all the
# years for which we have data
print('Iterating through tags')
print('----------------------')
years = set()
for element in root.iter():
    if ('name' in element.keys()
            and element.attrib['name']
            == 'Year'):
        years.add(element.text)
print(*sorted(list(years)), sep='\n')
print()

# Use of XPath
french_data = root.xpath(
    """//record[field='France']"""
    """/field[@name='Year' or @name='Value']"""
    """/text()""")
print(french_data)
