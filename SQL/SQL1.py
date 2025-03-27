#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 16:41:42 2017

@author: mikewoodward
"""

import requests
import sqlite3
import sys

## Getting Chinook SQL
## ===================
url = 'https://raw.githubusercontent.com/lerocha' \
      '/chinook-database/master/ChinookDatabase' \
      '/DataSources/Chinook_Sqlite.sql'
      
headers = {'User-Agent': 'Python User Agent'}

try:
    response = requests.get(url, headers=headers, timeout=10)
except requests.ConnectionError as e:
    print('Couldn\'t reach the server.')
    print('Reason: ', e)
    sys.exit(1)
except requests.Timeout as e:
    print('Timeout error.')
    print( 'Reason: ', e)
    sys.exit(1)
if response.status_code != 200:
    print('Error status code {0}'.format(response.status_code))
    sys.exit(1)

# Strip off the BOM
build_sql = response.text[1:]

# Save the SQL file
with open('Chinook_Sqlite.sql', 'w') as sql:
    # The first character is a BOM - remove it
    sql.write(build_sql)
   
# Building the database
# =====================
database = "chinook.db"

try:
   conn = sqlite3.connect(database)  
   cursor = conn.cursor()
 
   cursor.executescript(build_sql)
   
   conn.commit()
   conn.close()
except sqlite3.Error as e:
   print("An error occurred:", e.args[0])

# Querying the table
# ==================
with sqlite3.connect(database) as conn:

    cursor = conn.cursor()
    
    print('Tables in database')
    sql = """select name 
             from sqlite_master 
             where type='table' 
             order by name"""
    cursor.execute(sql)
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]
    print(tables)
    print()
    
    print("City and country data")
    sql = """select distinct 
               city, country 
             from 
               Customer 
             order by 
               country, city"""
    cursor.execute(sql)
    print('Columns are {0}'.format([c[0] for c in cursor.description]))
    city_country = cursor.fetchall()
    print(city_country)
    print()
    
    print('Countries who like Black Sabbath')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = """
          select 
            Customer.Country, 
            count(distinct Customer.CustomerId) 
              as cust_count
          from Artist
          join Album
          on Artist.ArtistId = Album.ArtistId
          join Track
          on Track.AlbumId = Album.AlbumId
          join InvoiceLine
          on InvoiceLine.TrackId = Track.TrackId
          join Invoice
          on InvoiceLine.InvoiceId
          join Customer
          on Customer.CustomerId = Invoice.CustomerId
          where Artist.Name='Black Sabbath'
          group by Customer.Country"""
    cursor.execute(sql)
    artistcountry = cursor.fetchall()
    aclist = [dict(ac) for ac in artistcountry]
    print(aclist)
    