#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 16:19:23 2025

@author: mikewoodward
"""

# %%---------------------------------------------------------------------------
# Module metadata
# -----------------------------------------------------------------------------
__author__ = "mikewoodward"
__license__ = "MIT"
__summary__ = "One line summary"


import requests
import zipfile
import lxml
import lxml.etree

url = ("""https://leidata-preview.gleif.org/"""
       """storage/golden-copy-files/2025/03/07/"""
       """1051171/20250307-1600-gleif-goldencopy"""
       """-lei2-golden-copy.xml.zip#""")

# Download the file
res = requests.get(
  url=url,
  timeout=10)
with open('population.zip',
          'wb') as xml_file:
  xml_file.write(res.content)
# Unzip the XML
with zipfile.ZipFile('population.zip', 'r') as zf:
  zip_file_names = zf.namelist()
  zf.extractall()

file_path = zip_file_names[0]

search_term = "Amazon"

namespace = {"lei":
             "http://www.gleif.org/data"
             "/schema/leidata/2016"}

# Stream through the file, looking for 
# LEIRecord elements
document = lxml.etree.iterparse(
  file_path,
  events=("end",),
  tag=("{http://www.gleif.org/data/schema/"
       "leidata/2016}LEIRecord")
)

# Loop through every element in the tree
for event, elem in document:

  # Extract LEI
  lei_elem = elem.find("lei:LEI",
                       namespaces=namespace)
  lei = (lei_elem.text if lei_elem is not None
         else None)

  # Extract Legal Name
  legal_name_elem = elem.find(
    "lei:Entity/lei:LegalName",
    namespaces=namespace
  )
  legal_name = (legal_name_elem.text
                if legal_name_elem is not None
                else None)

  # If we've got a legal name and it matches,
  # print out the matches
  if (legal_name and search_term.lower()
      in legal_name.lower()):
    if search_term.lower() in legal_name.lower():
      print(f"LEI: {lei}, Legal Name: {legal_name}")

  # Free memory by clearing processed elements
  elem.clear()
  while elem.getprevious() is not None:
    del elem.getparent()[0]

del document  # Ensure proper cleanup
