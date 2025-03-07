#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
import requests

res = requests.get(
    url="""https://zenodo.org/record/6508640"""
    """/files/test_combined_multiclass.csv.gz""",
    timeout=10)

with open('test_combined_multiclass.csv.gz',
          'wb') as zf:
    zf.write(res.content)

with gzip.open('test_combined_multiclass.csv.gz',
                'r') as f:
    file_contents = f.readlines()

print(file_contents[0:10])
