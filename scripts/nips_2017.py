from __future__ import print_function

'''
download all NIPS2017 papers and create index.html for them
'''

import time
import json
import sys
import os
import six
from six.moves import urllib
from bs4 import BeautifulSoup



papers_page = "https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017"
paper_root = "https://papers.nips.cc"

def get_file_name(file_url):
    return file_url.split('/')[-1]

def download_file(file_url, file_path):
    response = urllib.request.urlopen(file_url)
    with open(file_path, 'wb') as fout:
        fout.write(response.read())



html = urllib.request.urlopen(papers_page)
soup = BeautifulSoup(html, "html.parser")

papers = list(soup.find_all('ul')[1].find_all('li'))

paper_details = []
for i, paper in enumerate(papers):
    href = paper.find('a')['href']
    name = paper.find('a').text

    print('{}/{}\t{}'.format(i+1, len(papers), name))

    paper_html = urllib.request.urlopen(paper_root + href)
    paper_soup = BeautifulSoup(paper_html, 'html.parser')

    pdf_href = [x['href'] for x in paper_soup.find_all('a') if x.text == '[PDF]']
    pdf_url = paper_root + pdf_href[0]
    authors = paper_soup.find('ul', class_='authors')
    authors = [author.find('a').text for author in authors.find_all('li')]
    supple_pdf_href = [x['href'] for x in paper_soup.find_all('a') if x.text == '[Supplemental]']
    supple_pdf_url = [paper_root + x for x in supple_pdf_href]


    assert(len(pdf_href) == 1)
#    assert(len(authors) >= 1) # some papers have no authors now

    filename = get_file_name(pdf_url)
    file_path = os.path.join('downloaded', 'nips2017', 'papers', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    download_file(pdf_url, file_path)
    paper_details.append(
        dict(title=name,
             abstract=paper_soup.find('p', class_='abstract').text,
             authors=', '.join(authors),
             links=dict(pdf=os.path.join('papers', filename))
             )
    )
    time.sleep(0.5)



with open(os.path.join('downloaded', 'nips2017', 'index.html'), 'w') as fout:
    fout.write('''<!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>{title}</title></head>
    <body>
    '''.format(title='NIPS2017'))
    for detail in paper_details:
        fout.write('<h2>{title}</h2>\n'.format(title=detail['title']))
        fout.write('{authors}\n'.format(authors=detail['authors']))
        fout.write('<br/>')
        fout.write('<h3>Abstract</h3>')
        fout.write('{abstract}'.format(abstract=detail['abstract']))
        fout.write('<br/>')
        fout.write('<h3>Materials</h3>')
        links = detail['links']
        fout.write('<ul>')
        if 'pdf' in links:
            fout.write('<li><a href={href}>pdf</a></li>'.format(href=links['pdf']))
        if 'supplementary_pdf' in links:
            fout.write('<li><a href={href}>supplementary pdf</a></li>'.format(href=links['supplementary_pdf']))
        if 'supplementary_zip' in links:
            fout.write('<li><a href={href}>supplementary zip</a></li>'.format(href=links['supplementary_zip']))
        fout.write('</ul>')
        fout.write('<br/>')
    fout.write('</body></html>')

