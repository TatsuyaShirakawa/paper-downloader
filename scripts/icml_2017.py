from __future__ import print_function, division, absolute_import, unicode_literals
import os
from bs4 import BeautifulSoup
import urllib
import click
import arxiv

papers_url = 'http://proceedings.mlr.press/v70/'

def url_encode(url):
    p = urllib.parse.urlparse(url)
    url = '{}://{}{}'.format(p.scheme, p.netloc, '/'.join(urllib.parse.quote_plus(x) for x in p.path.split('/')))
    return url

@click.command()
@click.argument('result_dir')
def main(result_dir):

    html = urllib.request.urlopen(papers_url)
    soup = BeautifulSoup(html, "html.parser")

    papers = soup.find_all('div', attrs={'class': 'paper'})
    print('{} papers found'.format(len(papers)))

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    for paper in papers:

        title = paper.find('p', attrs={'class': 'title'}).text
        links = paper.find('p', attrs={'class': 'links'})

        print( title, '...' )

        paper_dir = os.path.join(result_dir, title.replace(' ', '_').lower())
        if not os.path.exists(paper_dir):
            os.makedirs(paper_dir)

        for a in links.find_all('a'):
            if a.text == 'abs':
                # abs
                pass
            elif a.text == 'Download PDF':
                # paper pdf link
                url = a['href']
                print(url)
                url = url_encode(url)
                save_path = os.path.join(paper_dir, url.split('/')[-1])
                if os.path.exists(save_path):
                    continue
                response = urllib.request.urlopen(url)
                with open(save_path, 'wb') as fout:
                    fout.write(response.read())
            elif a.text == 'Supplementary PDF':
                # paper supplementary pdf link
                url = a['href']
                print(url)
                url = url_encode(url)
                save_path = os.path.join(paper_dir, url.split('/')[-1])
                if os.path.exists(save_path):
                    continue
                response = urllib.request.urlopen(url)
                with open(save_path, 'wb') as fout:
                    fout.write(response.read())
            elif a.text == 'Supplementary ZIP':
                # paper supplementary ZIP link
                url = a['href']
                print(url)
                url = url_encode(url)
                save_path = os.path.join(paper_dir, url.split('/')[-1])
                if os.path.exists(save_path):
                    continue
                response = urllib.request.urlopen(url)
                with open(save_path, 'wb') as fout:
                    fout.write(response.read())
            else:
                print( 'unknown link', a.text )


if __name__ == '__main__':

    main()
