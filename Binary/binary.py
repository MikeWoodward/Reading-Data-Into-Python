#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:01:41 2023

@author: mikewoodward
"""

# Using context manager
with open("the-last-post.mp3", "rb") as lastpost:
  lastpost_mp3 = lastpost.read()
print(lastpost_mp3[0:120])


with open("the-last-post.mp3", "rb") as lastpost:
  print("Read function moving file position.")
  print(f"Starting position: {lastpost.tell()}")
  lastpost_data = lastpost.read(10)
  print('10 bytes of data', lastpost_data)
  print(f"Starting position + 10: {lastpost.tell()}")
  print("Seek demos:")
  print("seek 1000 point in")
  lastpost.seek(1000)
  print(f"seek position: {lastpost.tell()}")
  print("Seek end of file")
  lastpost.seek(0, 2)
  print(f"ending position: {lastpost.tell()}")
  print("Seek end of file minus 56")
  lastpost.seek(-56, 2)
  print(f"seek position: {lastpost.tell()}")
  print("Seek current position plus 56")
  lastpost.seek(56, 1)
  print(f"seek position: {lastpost.tell()}")
