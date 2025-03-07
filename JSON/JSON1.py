#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 18:54:04 2017

@author: mikewoodward
"""

import json

with open('ballarat-bbqs.geojson') as json_file:
    data = json.load(json_file)

print(f"Ballarat has {len(data['features'])} BBQs")

for bbq in data['features']:
    print("================")
    print("Site name   : {0}".format(
        bbq[u'properties']['site']))
    print("Number BBQs : {0}".format(
        bbq[u'properties']['number']))
    print("Location    : {0}".format(
        bbq[u'properties']['location']))
