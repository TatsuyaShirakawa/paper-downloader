from __future__ import print_function, division, absolute_import, unicode_literals
import os
import sys
import re
import urllib
import json
from bs4 import BeautifulSoup
import click

papers_url = 'http://proceedings.mlr.press/v70/'

def url_encode(url):
    p = urllib.parse.urlparse(url)
    url = '{}://{}{}'.format(p.scheme, p.netloc, '/'.join(urllib.parse.quote_plus(x) for x in p.path.split('/')))
    return url

@click.command()
@click.argument('result_dir')
@click.option('--no_html', is_flag=True)
@click.option('--no_json', is_flag=True)
def main(result_dir, no_html, no_json):

    html = urllib.request.urlopen(papers_url)
    soup = BeautifulSoup(html, "html.parser")

    papers = soup.find_all('div', attrs={'class': 'paper'})
    print('{} papers found'.format(len(papers)))

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    papers_detail = []

    for paper_count, paper in enumerate(papers):

        title = paper.find('p', attrs={'class': 'title'}).text
        links = paper.find('p', attrs={'class': 'links'})

        print( '[{}/{}]'.format(paper_count+1, len(papers)), title, '...' )
        paper_dirname = title.replace(' ', '_').lower()
        paper_dirname = re.sub(r'[\"\'\:\;\/“]', '', paper_dirname)
        paper_dir = os.path.join(result_dir, paper_dirname)
        if not os.path.exists(paper_dir):
            os.makedirs(paper_dir)

        detail = {}
        detail['title'] = title
        detail['links'] = {}
        for a in links.find_all('a'):
            if a.text == 'abs':
                # abs
                url = a['href']
                url = url_encode(url)
                try:
                    abs_html = urllib.request.urlopen(url)
                    abs_soup = BeautifulSoup(abs_html, 'html.parser')
                    # abstract
                    detail['abstract'] = abs_soup.find('div', attrs={'class': 'abstract'}).text.strip()
                    authors =  abs_soup.find('div', attrs={'class': 'authors'}).text.strip().strip(';')
                    authors = [author.strip() for author in authors.split(',')]
                    detail['authors'] = ', '.join(authors)
                except urllib.error.HTTPError as err:
                    print('cannot open url', url, file=sys.stderr)
                    print(err, file=sys.stderr)
            elif a.text == 'Download PDF':
                # paper pdf link
                url = a['href']
                url = url_encode(url)
                try:
                    filename = url.split('/')[-1]
                    save_path = os.path.join(paper_dir, filename)
                    if not os.path.exists(save_path):
                        response = urllib.request.urlopen(url)
                        with open(save_path, 'wb') as fout:
                            fout.write(response.read())
                    detail['links']['pdf'] = os.path.join(paper_dirname, filename)
                except urllib.error.HTTPError as err:
                    print('cannot open url', url, file=sys.stderr)
                    print(err, file=sys.stderr)
            elif a.text == 'Supplementary PDF':
                # paper supplementary pdf link
                url = a['href']
                url = url_encode(url)
                try:
                    filename = url.split('/')[-1]
                    save_path = os.path.join(paper_dir, filename)
                    if not os.path.exists(save_path):
                        response = urllib.request.urlopen(url)
                        with open(save_path, 'wb') as fout:
                            fout.write(response.read())
                    detail['links']['supplementary_pdf'] = os.path.join(paper_dirname, filename)
                except urllib.error.HTTPError as err:
                    print('cannot open url', url, file=sys.stderr)
                    print(err, file=sys.stderr)
            elif a.text == 'Supplementary ZIP':
                # paper supplementary ZIP link
                url = a['href']
                url = url_encode(url)
                try:
                    filename = url.split('/')[-1]
                    save_path = os.path.join(paper_dir, filename)
                    if not os.path.exists(save_path):
                        response = urllib.request.urlopen(url)
                        with open(save_path, 'wb') as fout:
                            fout.write(response.read())
                    detail['links']['supplementary_zip'] = os.path.join(paper_dirname, filename)
                except urllib.error.HTTPError as err:
                    print('cannot open url', url, file=sys.stderr)
                    print(err, file=sys.stderr)
            else:
                print( 'unknown link', a.text )
        papers_detail.append(detail)

    if not no_json:
        json.dump(papers_detail, open(os.path.join(result_dir, 'detail.json'), 'w'))

    if not no_html:
        with open(os.path.join(result_dir, 'index.html'), 'w') as fout:
            fout.write('''<!DOCTYPE html>
            <html><head><meta charset="utf-8"><title>{title}</title></head>
            <body>
            '''.format(title='ICML2017'))
            for detail in papers_detail:
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

if __name__ == '__main__':

    main()
