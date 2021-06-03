import pandas as pd

from parsing_conferences.get_affiliation import get_affiliations
from parsing_conferences.get_papers import get_neurips_papers

if __name__ == '__main__':
    year = 2020
    neurips_generator = get_neurips_papers(year)
    affiliation_data = []
    n_samples = 10
    counter = 0
    for neurips_art in neurips_generator:
        affiliations = get_affiliations('tmp.pdf')
        for affiliation in affiliations:
            affiliation_data.append({
                'affiliation': affiliation,
                'paper_title': neurips_art
            })
        counter += 1
        if counter > n_samples:
            break
    df_affiliations = pd.DataFrame(affiliation_data)
    df_affiliations.to_csv('affiliations_neurips_2020.csv')
    print(df_affiliations)
