# Web Scraper
#
# This script builds a table of image id's associated with the
# related features and information contained within GAPE's portal
#
# Example Code: https://realpython.com/python-web-scraping-practical-introduction/

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import argparse
import requests
# import csv
# import os
# import re
# import sys
# from pathlib import Path
# from requests.packages.urllib3.util.retry import Retry
# from requests.adapters import HTTPAdapter
# import urllib3

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

#-----------------------------------------------------------------
# Code from feature_extractor.py
#-----------------------------------------------------------------

# # CLI accepting user input
# parser = argparse.ArgumentParser(prog='feature_extractor',
#                                  description='Scrape a list of image ids from"\
#                                  " GAPE and extract associated attributes for each image.')
# parser.add_argument('feature_file', action='store', type=str,
#                     help='CSV file of image ids')
# args = parser.parse_args()

# #default image sizes to small
# img_size= 'small'

# # Max number of retries
# total_retries = 5

# # Checking if input file is present
# input_file = os.path.join('.','inputs', args.feature_file)
# file = Path(input_file)
# try:
#     file.resolve()
# except FileNotFoundError:
#     print("*** ERROR: File: " + args.feature_file + " does not exist. ***")
#     print("\nTerminating script.")
#     sys.exit()
# else:
#     new_folder = args.feature_file[:-4]

# if args.with_crosshairs:
#     # Core urls for images with crosshairs
#     url_1 = "https://eol.jsc.nasa.gov/CatalogersAccess/GetRotatedImage"\
#             ".pl?image="
#     url_2 = "&rotation=1&MarkCenter=1"
# else:
#     # Core url for general images
#     url = "https://eol.jsc.nasa.gov/DatabaseImages"

# # Noted ids with _2 extenstion in name
# anomalous_ids = ['ISS002-E-5448', 'ISS002-E-5632', 'ISS002-E-5633',
#                  'ISS002-E-5634']

# # Creating all new directories with full permission in octal
# mode = 0o777

# # Create an outputs folder if one doesn't exist
# outputs_dir = os.path.join('.','outputs')
# if not os.path.isdir(outputs_dir):
#     os.makedirs(outputs_dir, mode=mode)

# # Alerts for folder duplicate
# output_path = os.path.join(outputs_dir, new_folder, "")
# try:
#     os.makedirs(output_path, mode=mode)
# except FileExistsError:
#     print("\n*** ERROR: Cannot create folder with name " + new_folder +
#           " because the folder already exists. ***")
#     print("\nTerminating script.")
#     sys.exit()

# # Finds the number of ids in csv file
# with open(input_file, 'r') as p:
#         total_count = sum(1 for counter1 in p)

# # Intitial output message
# print("\nTotal number of image ids in file: " + str(total_count) + "\n")

# # Counter for progress and success of image downloads
# count_total = 0
# count_success = 0


# url = "https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=STS099&roll=744&frame=38"
# raw_html = simple_get(url)
# html = BeautifulSoup(raw_html, 'html.parser')

# table = html.findALL("table", attrs = {"class": "table-responsive"})
# print table

page = requests.get("https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=STS099&roll=744&frame=38")
# print page.content
soup = BeautifulSoup(page.content, 'html.parser')
# print (soup.prettify())
table = soup.findALL("table", attrs = {"class": "table-responsive"})

print (table)


