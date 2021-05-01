import requests
from bs4 import BeautifulSoup
import pandas as pd

website_brgy_pop = requests.get('https://en.wikipedia.org/wiki/Barangays_of_Cebu_City#:~:text=As%20of%202015%2C%2058%20barangays,7.21%25%20of%20the%20total%20population.').text
soup = BeautifulSoup(website_brgy_pop, 'lxml')
tbl = soup.find('table', {'class': 'wikitable sortable'})
lst = tbl.find_all('tr')


df_list = []
for _span in lst[3:-2]:
    df_list.append(
        [i for i in _span.text.split('\n') if i != '']
    )
column_names = ['barangay', 'geog_district', 'legislative_district', 'brgy_cap', 'pop_2015', 'pop_2010','chg', 'code', 'urban_or_rural']
_dict = {k: [] for k in column_names}
for dt in df_list:
    for col, i in zip(column_names, dt):
        _dict[col].append(i)
fnl = pd.DataFrame(_dict)
# change Kamputhaw (Camputhaw) to just Kamputhaw
fnl.loc[fnl.barangay == 'Kamputhaw (Camputhaw)', 'barangay'] = 'Kamputhaw'
# change pop data as float
fnl['pop_2010'] = fnl.pop_2010.str.replace(',', '').astype('float64')
fnl.to_csv('data/demographics.txt', index= False)