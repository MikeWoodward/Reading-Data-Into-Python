#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:01:41 2023

@author: mikewoodward
"""

"""
Download this MP3 file from 
https://anzacportal.dva.gov.au/sites/default/files/audio/the-last-post.mp3
to the folder that contains this code.
"""

# Using context manager
with open("the-last-post.mp3", 
          "rb") as lastpost:
  lastpost_mp3 = lastpost.read()
print(lastpost_mp3[0:120])


with open("the-last-post.mp3", 
          "rb") as last:
  print("Moving file position demo.")
  print(f"Start pos: {last.tell()}")
  lastpost_data = last.read(10)
  print('10 bytes of data', lastpost_data)
  print(f"Start pos + 10: {last.tell()}")
  print("Seek demos:")
  print("seek 1000 point in")
  last.seek(1000)
  print(f"seek position: {last.tell()}")
  print("Seek end of file")
  last.seek(0, 2)
  print(f"ending position: {last.tell()}")
  print("Seek end of file minus 56")
  last.seek(-56, 2)
  print(f"seek position: {last.tell()}")
  print("Seek current position plus 56")
  last.seek(56, 1)
  print(f"seek position: {last.tell()}")
