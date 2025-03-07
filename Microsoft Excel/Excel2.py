#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 21:08:11 2017

@author: mikewoodward
"""

from openpyxl import load_workbook
from openpyxl.formula import Tokenizer

wb = load_workbook(filename='databreachesineurope-publicdata.xlsx')
year_sheet = wb['Year']

counter = 2
while True:
    year = year_sheet['A{0}'.format(counter)].value

    if year is None or 'TOTAL' == year:
        break

    volume = year_sheet['B{0}'.format(counter)].value

    volume_tokens = Tokenizer(volume)

    print(year)
    print(volume_tokens.items)

    counter += 1
