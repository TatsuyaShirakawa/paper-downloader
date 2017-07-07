from __future__ import print_function, division, absolute_import, unicode_literals
import os
from bs4 import BeautifulSoup
import urllib
import click
import arxiv

papers_url = 'https://2017.icml.cc/Conferences/2017/AcceptedPapers'

@click.command()
@click.argument('result_dir')
def main(result_dir):

    html = urllib.request.urlopen('https://2017.icml.cc/Conferences/2017/AcceptedPapers')
    soup = BeautifulSoup(html, "html.parser")

    titles = [x.text for x in soup.find_all('strong')]
    print('{} papers found'.format(len(titles)))

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    num_founds = 0
    num_not_founds = 0
    for title in titles:

        entry = arxiv.search(title)
        if entry is not None:
            print('found    :', title)
            link = entry.find('link', attrs=dict(title='pdf'))
            if link is None:
                num_not_founds += 1
                continue
            paper_url = link['href']
            response = urllib.request.urlopen(paper_url)
            with open(os.path.join(result_dir, paper_url.split('/')[-1]), 'wb') as fout:
                fout.write(response.read())
            num_founds += 1
        else:
            print('not found:', title)
            num_not_founds += 1

    print('founds:', num_founds)
    print('not founds:', num_not_founds)


if __name__ == '__main__':

    main()
