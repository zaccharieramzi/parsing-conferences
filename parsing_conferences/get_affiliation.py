import requests
from bs4 import BeautifulSoup

def get_affiliations(pdf_path):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    response = requests.post(
        'http://cermine.ceon.pl/extract.do',
        headers={'Content-Type': 'application/binary'} ,
        data=data,
    )
    xml_pdf = response.content
    soup = BeautifulSoup(xml_pdf, 'lxml')
    institutions = [i.contents[0] for i in soup.find_all('institution')]
    return institutions

if __name__ == '__main__':
    print(get_affiliations('../mendeley_papers/wang03b.pdf'))
