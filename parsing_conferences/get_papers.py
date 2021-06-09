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

def get_neurips_papers(year):
    response = requests.get(PROCEEDINGS['neurips'][year])
    soup = BeautifulSoup(response.content)
    list_items = soup.find_all('li')
    articles_items = [li for li in list_items if is_li_article(li)]
    for article_item in articles_items:
        article_title = article_item.contents[0].contents[0]
        article_link = article_item.contents[0].attrs['href']
        art_response = requests.get(PROCEEDINGS['neurips']['prefix'] + article_link)
        soup_art = BeautifulSoup(art_response.content)
        meta_art_page = soup_art.find_all('meta')
        art_pdf_links = [m for m in meta_art_page if m.get('name') == 'citation_pdf_url']
        if len(art_pdf_links) > 1:
            raise ValueError()
        article_link = art_pdf_links[0]['content']
        pdf_response = requests.get(article_link)
        with open('tmp.pdf', 'wb') as f:
            f.write(pdf_response.content)
        yield article_title, article_link

def get_neurips_papers_batched(year, batch_size=10, batch_id=0):
    response = requests.get(PROCEEDINGS['neurips'][year])
    soup = BeautifulSoup(response.content)
    list_items = soup.find_all('li')
    articles_items = [li for li in list_items if is_li_article(li)]
    if batch_id*batch_size > len(articles_items) - 1:
        raise ValueError('No more elements')
    articles_items_batched = articles_items[batch_id*batch_size:(batch_id+1)*batch_size]
    for i_art, article_item in enumerate(articles_items_batched):
        article_title = article_item.contents[0].contents[0]
        article_link = article_item.contents[0].attrs['href']
        art_response = requests.get(PROCEEDINGS['neurips']['prefix'] + article_link)
        soup_art = BeautifulSoup(art_response.content)
        meta_art_page = soup_art.find_all('meta')
        art_pdf_links = [m for m in meta_art_page if m.get('name') == 'citation_pdf_url']
        if len(art_pdf_links) > 1:
            raise ValueError()
        article_link = art_pdf_links[0]['content']
        pdf_response = requests.get(article_link)
        pdf_filename = f'tmp_{i_art}.pdf'
        with open(pdf_filename, 'wb') as f:
            f.write(pdf_response.content)
        yield article_title, article_link, pdf_filename

async def get_neurips_papers_batched_async(session, year=2020, batch_size=10, batch_id=0):
    async with session.get(PROCEEDINGS['neurips'][year]) as response:
        soup = BeautifulSoup(await response.text())
    list_items = soup.find_all('li')
    articles_items = [li for li in list_items if is_li_article(li)]
    if batch_id*batch_size > len(articles_items) - 1:
        raise ValueError('No more elements')
    articles_items_batched = articles_items[batch_id*batch_size:(batch_id+1)*batch_size]
    for i_art, article_item in enumerate(articles_items_batched):
        article_title = article_item.contents[0].contents[0]
        article_link = article_item.contents[0].attrs['href']
        art_response = requests.get(PROCEEDINGS['neurips']['prefix'] + article_link)
        soup_art = BeautifulSoup(art_response.content)
        meta_art_page = soup_art.find_all('meta')
        art_pdf_links = [m for m in meta_art_page if m.get('name') == 'citation_pdf_url']
        if len(art_pdf_links) > 1:
            raise ValueError()
        article_link = art_pdf_links[0]['content']
        pdf_response = session.get(article_link)
        yield article_title, article_link, pdf_response
