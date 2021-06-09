from pathlib import Path
import subprocess
import time

import requests
from bs4 import BeautifulSoup


CERMINE_URL = 'http://cermine.ceon.pl/extract.do'
CERMINE_JAR_FILE = 'cermine-impl-1.13-jar-with-dependencies.jar'
CERMINE_OPTION = 'pl.edu.icm.cermine.ContentExtractor'

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

def get_affiliations_local(pdf_dir):
    subprocess.call(
        ['java', '-cp', CERMINE_JAR_FILE, CERMINE_OPTION, '-path', pdf_dir, '-outputs', 'jats'],
        stdout=subprocess.PIPE,
    )
    pdf_dir = Path(pdf_dir)
    xml_files = list(pdf_dir.glob('*.cermxml'))
    try:
        xml_file = xml_files[0]
    except IndexError:
        return []
    else:
        with open(xml_file, 'rb') as f:
            xml_pdf = f.read()
        soup = BeautifulSoup(xml_pdf, 'lxml')
        institutions = [i.contents[0] for i in soup.find_all('institution')]
        xml_file.unlink()
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
    institutions = get_affiliations_local('pdfs')
    print(institutions)
