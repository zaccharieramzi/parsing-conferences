import asyncio
import csv
from pathlib import Path
import time

import aiohttp
from aiohttp import ClientSession
import pandas as pd

from parsing_conferences.get_affiliation import get_affiliations_async
from parsing_conferences.get_papers import get_neurips_papers_batched, get_neurips_papers_batched_async

OUT_FILE = 'async_affiliations_neurips_{year}.csv'

async def write_affiliations(session, out_filename, neurips_art, art_link, pdf_resp=None):
    affiliations = await get_affiliations_async(pdf_resp, session)
    outfile_exists = Path(out_filename).is_file()
    with open(out_filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'affiliation',
            'article_link',
            'paper_title',
        ])
        if not outfile_exists:
            writer.writeheader()
        for affiliation in affiliations:
            affiliation_data = {
                'affiliation': affiliation,
                'article_link': art_link,
                'paper_title': neurips_art,
            }
            writer.writerow(affiliation_data)

async def bulk_get_affil_and_write(df_affiliations, batch_id=0, batch_size=10, year=2020):
    async with ClientSession(raise_for_status=True, timeout=aiohttp.ClientTimeout(batch_size*50)) as session:
        neurips_generator = get_neurips_papers_batched_async(session, year, batch_size, batch_id)
        tasks = []
        async for neurips_art, art_link, pdf_response in neurips_generator:
            if df_affiliations is not None and art_link in df_affiliations['article_link'].unique():
                continue
            tasks.append(
                write_affiliations(
                    out_filename=OUT_FILE.format(year=year),
                    neurips_art=neurips_art,
                    art_link=art_link,
                    session=session,
                    pdf_resp=pdf_response,
                )
            )
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    year = 2020
    try:
        df_affiliations = pd.read_csv(OUT_FILE.format(year=year), index_col=0)
    except FileNotFoundError:
        df_affiliations = None
    batch_size = 5
    batch_id = 0
    max_batch = 2
    while batch_id < max_batch:
        try:
            asyncio.run(bulk_get_affil_and_write(df_affiliations, batch_id, batch_size, year))
        except ValueError:
            break
        else:
            print(f'Batch {batch_id} done')
            df_affiliations = pd.read_csv(OUT_FILE.format(year=year), index_col=0)
            batch_id += 1
    print(df_affiliations)
