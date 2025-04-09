#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 18:38:46 2017

@author: mikewoodward
"""

from glob import glob
import json
from os.path import join

# Dictionary to hold SSID names
ssids = {}
# Get all the names of the user files
user_files = folders = glob(
  join('./UbiqLog4UCI',
        '[0-9]*',
        '*.txt'),
  recursive=True)
# Step through every user file
for user_file in user_files:
  # Open the file, using unicode_escape
  with open(user_file,
            encoding="unicode_escape") as json_file:
    # Step through each line in the file
    for line in json_file:
      try:
        # Decode the JSON data
        data = json.loads(line)
        # Does the JSON contain WiFI and SSID?
        if ('WiFi' in data.keys() and
            'SSID' in data['WiFi'].keys()):
          ssid_value = data['WiFi']['SSID']
          # Increment the counter or 
          # add a new counter
          if ssid_value not in ssids.keys():
            ssids[ssid_value] = 1
          else:
            ssids[ssid_value] += 1
          # Note exceptions and continue
      except ValueError as error:
        print("""ValueError in file """
              f"""{user_file}""")
        continue
      except AttributeError as error:
        print("""AttributeError in file """ 
              f"""{user_file}""")
        continue
# Sort the dictionary in descending order
ssids_descend = sorted(ssids.items(),
                       key=lambda x: x[1],
                       reverse=True)
# Print out the top 10
print("Top 10 SSID names are:")
print("Name       |      count")
for i in ssids_descend[0:10]:
  print(f"{i[0].ljust(10)} | {i[1]:10}")
