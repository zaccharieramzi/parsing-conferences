import pandas as pd
from tqdm import tqdm

from parsing_conferences.get_affiliation import get_affiliations_local
from parsing_conferences.get_papers import get_neurips_papers

if __name__ == '__main__':
    year = 2020
    neurips_generator = get_neurips_papers(year, in_dir=True)
    n_samples = None
    counter = 0
    try:
        df_affiliations = pd.read_csv(f'local_affiliations_neurips_{year}.csv', index_col=0)
    except FileNotFoundError:
        df_affiliations = None
    for neurips_art, art_link in tqdm(neurips_generator):
        if df_affiliations is not None and art_link in df_affiliations['article_link'].unique():
            continue
        affiliation_data = []
        affiliations = get_affiliations_local('pdfs')
        for affiliation in affiliations:
            affiliation_data.append({
                'affiliation': affiliation,
                'article_link': art_link,
                'paper_title': neurips_art
            })
        counter += 1
        if n_samples is not None and counter > n_samples:
            break
        df_affiliations_new = pd.DataFrame(affiliation_data)
        if df_affiliations is not None:
            df_affiliations = df_affiliations.append(df_affiliations_new)
        else:
            df_affiliations = df_affiliations_new
        df_affiliations.to_csv(f'local_affiliations_neurips_{year}.csv')
    print(df_affiliations)
