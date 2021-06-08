import asyncio
import csv
from pathlib import Path

from aiohttp import ClientSession
import pandas as pd

from parsing_conferences.get_affiliation import get_affiliations_async
from parsing_conferences.get_papers import get_neurips_papers_batched

OUT_FILE = 'async_affiliations_neurips_{year}.csv'

async def write_affiliations(session, out_filename, neurips_art, art_link, pdf_path='tmp.pdf'):
    affiliations = await get_affiliations_async(pdf_path, session)
    for affiliation in affiliations:
        affiliation_data = {
            'affiliation': affiliation,
            'article_link': art_link,
            'paper_title': neurips_art,
        }
        outfile_exists = Path(out_filename).is_file()
        with open(out_filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(affiliation_data.keys()))
            if not outfile_exists:
                writer.writeheader()
            writer.writerow(affiliation_data)

async def bulk_get_affil_and_write(df_affiliations, batch_id=0, batch_size=10, year=2020):
    async with ClientSession() as session:
        tasks = []
        neurips_generator = get_neurips_papers_batched(year, batch_size, batch_id)
        for neurips_art, art_link, pdf_name in neurips_generator:
            if df_affiliations is not None and art_link in df_affiliations['article_link'].unique():
                continue
            tasks.append(
                write_affiliations(
                    out_filename=OUT_FILE.format(year=year),
                    neurips_art=neurips_art,
                    art_link=art_link,
                    session=session,
                    pdf_path=pdf_name,
                )
            )
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    year = 2020
    try:
        df_affiliations = pd.read_csv(OUT_FILE.format(year=year), index_col=0)
    except FileNotFoundError:
        df_affiliations = None
    batch_size = 10
    batch_id = 0
    max_batch = 10000
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
