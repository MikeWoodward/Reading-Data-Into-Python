#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 12:16:44 2017

@author: mikewoodward
"""

import requests
import zipfile

# Get the Brazillian data
res = requests.get(url='http://download.geonames.org'
                   '/export/zip/BR.zip',
                   timeout=10)

# Write to disk
with open('BR.zip', 'wb') as zf:
    zf.write(res.content)

# Open the zip data
with zipfile.ZipFile('BR.zip', 'r') as zf:
    # Get the file names in the zip file
    names = zf.namelist()

    print("What's in the zip file:")
    for name in names:
        info = zf.getinfo(name)
        print(f"File name: {info.filename}, "
              f"file size: {info.file_size}")

    # Read in the entire file
    readme = zf.read('readme.txt')
    print("Start of readme: {0}:".format(readme[0:31]))

    # Open the BR file and read in data by line
    with zf.open('BR.txt') as br:
        br_postal = br.readlines()

    print("Start of Brazilian postal "
          f"code data: {br_postal[0]}")
