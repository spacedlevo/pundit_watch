import sys
from bs4 import BeautifulSoup as bs
import requests
import csv

url = sys.argv[1]
week = sys.argv[2]


def get_lawro_table(url):
    r = requests.get(url).text
    soup = bs(r, 'html.parser')
    table = soup.find('table', class_='sp-story-body__table')
    return table.find_all('tr')


def scrape_result(row):
    elements = row.find_all('td')
    teams = elements[0].text.lower().split(' v ')
    lawro_predict = elements[2].text.split('-')
    try:
        return [week, 'mark lawrenson', teams[0], teams[1], lawro_predict[0], lawro_predict[1]]
    except IndexError:
        pass


def print_results(predictions):
    home = predictions[2]
    away = predictions[3]
    home_score = predictions[4]
    away_score = predictions[5]
    print(f'{home.title()} {home_score} - {away_score} {away.title()}')


def mark_lawrenson():
    predictions = []
    table = get_lawro_table(url)
    table = table[3:]
    for row in table:
        predict = scrape_result(row)
        if predict is not None:
            predictions.append(predict)

    for i in predictions:
        print_results(i)

    with open(f'./predictions/lawro_{week}.csv', 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(predictions)


mark_lawrenson()
