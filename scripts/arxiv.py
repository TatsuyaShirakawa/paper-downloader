from __future__ import print_function, division, absolute_import, unicode_literals

import urllib
import difflib
from bs4 import BeautifulSoup

arxiv_api_url = 'https://export.arxiv.org/api/'

def search(title):
    url = arxiv_api_url + 'query?search_query=all:{}'.format(urllib.parse.quote(title))
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    for entry in soup.find_all('entry'):
        matcher = difflib.SequenceMatcher(a=title, b=entry.find('title').text)
        if matcher.ratio() > 0.9:
            return entry
    return None

if __name__ == '__main__':

    title = 'Algebraic Variety Models for High-Rank Matrix Completion'
    entry = search(title)
    if entry is None:
        print(title, 'not found')
        exit(0)

    print(entry.find_all('link'))
