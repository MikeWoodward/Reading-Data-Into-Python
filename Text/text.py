#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:01:41 2023

@author: mikewoodward
"""

# Simplest example
text = open("artofwar.txt", "r").read()
print(text[0:100])

# Use of readlines
file_object = open("artofwar.txt", "r")
lines = file_object.readlines()
print(lines[10:15])

# Using context manager
with open("artofwar.txt", "rt") as warfile:
    text = warfile.read()
print(text[0:100])

