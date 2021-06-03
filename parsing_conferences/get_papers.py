import time

import requests
from bs4 import BeautifulSoup


PROCEEDINGS = {
    'neurips': {2020: 'https://papers.nips.cc/paper/2020', 'prefix': 'https://papers.nips.cc/'}
}

def is_li_article(li):
    length_correct = len(li) == 3
    try:
        abs_in_ref = 'Abstract' in li.contents[0].attrs['href']
    except AttributeError:
        abs_in_ref = False
    return length_correct and abs_in_ref

if __name__ == '__main__':
    start = time.time()
    response = requests.get(PROCEEDINGS['neurips'][2020])
    soup = BeautifulSoup(response.content)
    list_items = soup.find_all('li')
    articles_items = [li for li in list_items if is_li_article(li)]
    for article_item in articles_items:
        article_link = article_item.contents[0].attrs['href']
        art_response = requests.get(PROCEEDINGS['neurips']['prefix'] + article_link)
        soup_art = BeautifulSoup(art_response.content)
        meta_art_page = soup_art.find_all('meta')
        art_pdf_links = [m for m in meta_art_page if m.get('name') == 'citation_pdf_url']
        if len(art_pdf_links) > 1:
            raise ValueError()
        article_link = art_pdf_links[0]['content']
        pdf_response = requests.get(article_link)
        with open('test.pdf', 'wb') as f:
            f.write(pdf_response.content)
        break
    end = time.time()
    print(f'Listing and downloading 1 took {end - start}')
