import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


CERMINE_URL = 'http://cermine.ceon.pl/extract.do'

def get_affiliations(pdf_path):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    response = requests.post(
        CERMINE_URL,
        headers={'Content-Type': 'application/binary'} ,
        data=data,
    )
    xml_pdf = response.content
    soup = BeautifulSoup(xml_pdf, 'lxml')
    institutions = [i.contents[0] for i in soup.find_all('institution')]
    return institutions

async def get_affiliations_async(pdf_resp, session):
    resp = await pdf_resp
    headers = {
        'Content-Type': 'application/binary',
        'Content-Length': str(resp.content_length),
    }
    async with session.post(CERMINE_URL, data=resp.content, headers=headers) as resp:
        xml_pdf = await resp.text()
    soup = BeautifulSoup(xml_pdf, 'lxml')
    institutions = [i.contents[0] for i in soup.find_all('institution')]
    return institutions

if __name__ == '__main__':
    mendeley_path = Path('../mendeley_papers')
    papers = mendeley_path.glob('NeurIPS-2020*.pdf')
    n_samples = 10
    for paper in list(papers)[:10]:
        start = time.time()
        print(paper.stem, get_affiliations(paper))
        end = time.time()
        print(f'Took {end - start} seconds')
        print('='*20)
