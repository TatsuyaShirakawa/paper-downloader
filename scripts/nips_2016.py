# -*- coding:utf-8 -*-

from __future__ import print_function

import time
import json
import sys
import os
import six
from six.moves import urllib
from bs4 import BeautifulSoup


#papers_page = "http://www.cv-foundation.org/openaccess/CVPR2016.py"
#paper_root = "http://www.cv-foundation.org/openaccess/"
paper_root = "https://nips.cc/Conferences/2016/Schedule"

def get_file_name(file_urf):
    return file_url.split('/')[-1]

def download_file(file_url, file_path):
    response = urllib.request.urlopen(file_url)
    with open(file_path, 'wb') as fout:
        fout.write(response.read())



html = urllib.request.urlopen(papers_page)
soup = BeautifulSoup(html, "html.parser")

field = soup.find('dl')

ptitle_dts = field.find_all('dt', class_='ptitle')
first_dds = field.find_all('dd')[0::2]
pdf_as = [x for x in soup.find_all('a') if x.text == 'pdf']

assert(len(ptitle_dts) == len(first_dds))
assert(len(pdf_as) == len(first_dds))

num_papers = len(ptitle_dts)

papers = []

for i in range(num_papers):
    # title
    title = ptitle_dts[i].find('a').text

    # authors
    authors = []
    for a in first_dds[i].find_all('a'):
        authors.append(a.text)

    # pdf_url
    pdf_url = paper_root + pdf_as[i]['href']

    papers.append({'title': title, 'authors': authors, 'pdf_url': pdf_url})

if not os.path.exists('papers'):
    os.mkdir('papers')

json.dump(papers, open('papers.json', 'w'))

for d in papers:
    print( "processing {} ...".format(d['title']))
    sys.stdout.flush()
    file_url = d['pdf_url']
    file_path = os.path.join('papers', get_file_name(file_url))
    download_file(file_url, file_path)
    time.sleep(1)
