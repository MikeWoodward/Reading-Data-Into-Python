#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:54:04 2017

@author: mikewoodward
"""

import json
import requests

# Download the file
res = requests.get(
    url="""https://data.cdc.gov/api/views/ebbj-sh54/"""
        """rows.json?accessType=DOWNLOAD""",
    timeout=10)
with open('CDC.json',
          'wt') as json_file:
    json_file.write(res.text)

# Read the JSON file
with open('CDC.json') as json_file:
    data = json.load(json_file)

# Print out a subset
print("{0:20} | {1}".format(
    data['meta']['view']['columns'][8]['name'],
    data['meta']['view']['columns'][10]['name']))
for state in data['data']:
    print("{0:20} | {1}".format(state[8],
                                state[10]))
