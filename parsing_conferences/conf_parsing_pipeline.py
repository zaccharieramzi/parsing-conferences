import pandas as pd
from tqdm import tqdm

from parsing_conferences.get_affiliation import get_affiliations
from parsing_conferences.get_papers import get_neurips_papers

if __name__ == '__main__':
    year = 2020
    neurips_generator = get_neurips_papers(year)
    affiliation_data = []
    n_samples = 10
    counter = 0
    try:
        df_affiliations = pd.read_csv('affiliations_neurips_2020.csv', index_col=0)
    except FileNotFoundError:
        df_affiliations = None
    for neurips_art, art_link in tqdm(neurips_generator):
        if df_affiliations is not None and art_link in df_affiliations['article_link'].unique():
            continue
        affiliations = get_affiliations('tmp.pdf')
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
    df_affiliations.to_csv('affiliations_neurips_2020.csv')
    print(df_affiliations)
