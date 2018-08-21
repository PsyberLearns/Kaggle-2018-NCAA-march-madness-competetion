from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np
import pandas as pd

chrome_path = "/Users/evanlee/Desktop/chromedriver"
driver = webdriver.Chrome(chrome_path)

#Code for webscraping the final season results from 2002-2018 for all the NCAA teams
for date in range(2002, 2019):
    url = "https://kenpom.com/index.php?y={}".format(date)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = []
    for div in soup.findAll('div', {'id': 'data-area'}):
        for tr in div.findAll('tr'):
            for td in tr.findAll('td'):
                if td.string is None:
                    for team in td.findAll('a'):
                        table.append(team.string)
                        continue
                else:
                    table.append(td.string)

    columns = ["Rank","Team","Conf","W-L","AdjEM","AdjO","AdjD","AdjT","Luck","SOC AdjEM","SOC OppO","SOC OppD","NCSOS AdjEM"]
    exec('df_{} = pd.DataFrame(columns=columns)'.format(date))

    i = 1
    j = 0
    new_table = []
    for stat in table:
        if i == 7 or i == 9 or i == 11 or i == 13 or i == 15 or i == 17 or i == 19 or i == 21:
            if i == 21:
                exec('df_{}.loc[j] = new_table'.format(date))
                new_table = []
                i = 0
                j+=1
            i+=1    
            continue
        new_table.append(stat)
        i += 1

    exec('df_{}.set_index(\'Rank\', inplace=True)'.format(date))
    exec('df_{}.to_csv(\'{}_final.csv\')'.format(date, date))
    