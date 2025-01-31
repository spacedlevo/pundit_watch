from bs4 import BeautifulSoup as bs
import requests
import re
import csv
import sys

merson_url = 'https://www.skysports.com/charlie-nicholas'
week = sys.argv[1]


def get_paul_url():
    r = requests.get(merson_url).text
    soup = bs(r, 'html.parser')
    headlines = soup.find_all('a', class_='news-list__headline-link')
    for head in headlines:
        if head.text.strip().lower() == "charlie's premier league predictions":
            print('Got ' + head['href'])
            return head['href']


def paul_fixtures(url):
    fixtures = []
    r = requests.get(url).text
    soup = bs(r, 'html.parser')
    content = soup.find('div', class_='article__body article__body--lead callfn')
    headers = content.find_all('h3', class_=None)
    for headline in headers:
        headline = headline.text.split('(')[0]
        headline = re.sub('Manchester United', 'man utd', headline)
        headline = re.sub('Manchester City', 'man city', headline)
        fixtures.append(headline.lower().strip().split(' vs '))
    return fixtures


def get_scores(url):
    scores = []
    r = requests.get(url).text
    soup = bs(r, 'html.parser')
    content = soup.find('div', class_='article__body article__body--lead callfn')
    paragraphs = content.find_all('p')
    for p in paragraphs:
        if re.search('\w+\sPredicts:\s\w+', p.text, re.IGNORECASE):
            try:
                score = re.search('\d-\d', p.text).group(0).split('-')
                scores.append(score)
            except AttributeError:
                continue
    return scores


def format_fixtures(prediction):
    try:
        home = prediction[0][0]
        home = home.replace('united', 'utd')
        away = prediction[0][1].split(' - ')[0]
        away = away.replace('united', 'utd')
        home_score = prediction[1][0]
        away_score = prediction[1][1]
        print(f'{home} {home_score} - {away} {away_score}')
        with open(f'../data/pundits/2019_20/charlie_{week}.csv', 'a') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([week, 'charlie nicholas', home, away, home_score, away_score])
    except IndexError:
        print('prediction not complete')

paul_predictions = []
paul_url = get_paul_url()
# paul_url = 'https://www.skysports.com/football/news/12090/11894383/charlie-nicholas-premier-league-predictions-leicester-to-stun-liverpool'
teams = paul_fixtures(paul_url)
scores = get_scores(paul_url)

for i in zip(teams, scores):
    paul_predictions.append(format_fixtures(i))