#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 21:00:18 2017

@author: mikewoodward
"""
import os
from boto3 import Session
import csv


def get_folders(client, bucket):
    """Gets the full folder structure. Recursive
    function."""
    def recursive(client, bucket, folders, prefix):
        objects = client.list_objects_v2(Bucket=bucket,
                                         Prefix=prefix,
                                         Delimiter='/')
        if 'CommonPrefixes' not in objects.keys():
            return
        for common in objects['CommonPrefixes']:
            prefix = common['Prefix']
            folders.append(prefix)
            recursive(client, bucket, folders, prefix)

    folders = []
    recursive(client, bucket, folders, '')
    print("Folders: {0}".format(folders))


def get1000(client, bucket):
    """Get 1000 keys"""
    with open('the1000.csv', 'w') as file1000:
        the1000 = client.list_objects_v2(Bucket=bucket)
        for content in the1000[u'Contents']:
            file1000.write('{0},{1}\n'.format(content[u'Key'],
                                              content[u'Size']))

    print("By default, list_object_v2 has "\
          "returned {0:,} keys".format(the1000['KeyCount']))


def getmore1000(client, bucket):
    """Get all the keys"""
    # Create a reusable Paginator
    paginator = client.get_paginator('list_objects_v2')
    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate(Bucket=bucket)
    # Iterate through the bucket and write keys to disk
    key_count = 0
    with open('morethan1000.csv', 'w') as filemore:
        for page in page_iterator:
            key_count += page['KeyCount']
            for content in page[u'Contents']:
                filemore.write('{0},{1}\n'.format(
                        content[u'Key'], content[u'Size']))
                
    print("With pagination, list_object_v2 has "\
          "returned {0:,} keys".format(key_count))


def download_samples(client, bucket):
    """Download sample files"""
    events = client.list_objects_v2(Bucket=bucket,
                                    Prefix='v2/events/2016112416')
    s3 = session.resource('s3')
    s3bucket = s3.Bucket(bucket)
    for content in events['Contents']:
        print("File {0} is {1:,} bytes".format(content['Key'],
                                               content['Size']))
        s3bucket.download_file(content['Key'],
                               content['Key'].rsplit('/', 1)[1])


def process_sample():
    """Open one of the files and parse it"""
    actors = set()
    with open('20161124164500.export.csv', 'r') as csvfile:
        events_csv = csv.reader(csvfile, delimiter='\t')
        for row in events_csv:
            desc = {'date': row[1],
                    'actor name': row[16],
                    'location': row[52],
                    'link': row[60]}
            actors.add(row[16])
    print("Actors mentioned.")
    print(sorted(actors))

ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
BUCKET = "gdelt-open-data"

session = Session(aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)
client = session.client('s3')

# Get all the folders in the bucket
get_folders(client, BUCKET)
print('--------------------')

# Get contents without pagination
get1000(client, BUCKET)
print('--------------------')

# Get all contents with pagination
getmore1000(client, BUCKET)
print('--------------------')

# Download example files
download_samples(client, BUCKET)
print('--------------------')

# Process one of the downloaded files
process_sample()
