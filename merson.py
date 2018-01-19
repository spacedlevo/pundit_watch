from bs4 import BeautifulSoup as bs
import requests
import re
import csv
import sys

merson_url = 'http://www.skysports.com/paul-merson'
week = sys.argv[1]


def get_paul_url():
    r = requests.get(merson_url).text
    soup = bs(r, 'html.parser')
    headlines = soup.find_all('a', class_='news-list__headline-link')
    for head in headlines:
        if head.text.strip().lower() == "merson's predictions":
            print('Got ' + head['href'])
            return head['href']


def paul_fixtures(url):
    fixtures = []
    r = requests.get(url).text
    soup = bs(r, 'html.parser')
    content = soup.find('div', class_='article__body article__body--lead')
    headers = content.find_all('h3', class_=None)
    for headline in headers:
        headline = headline.text.split('(')[0]
        headline = re.sub('Manchester United', 'man utd', headline)
        headline = re.sub('Manchester City', 'man city', headline)
        print(headline)
        fixtures.append(headline.lower().strip().split(' v '))
    return fixtures


def get_scores(url):
    scores = []
    r = requests.get(url).text
    soup = bs(r, 'html.parser')
    content = soup.find('div', class_='article__body article__body--lead')
    paragraphs = content.find_all('p')
    for p in paragraphs:
        if re.search('PAUL PREDICTS:\s\w+', p.text, re.IGNORECASE):
            score = re.search('\d-\d', p.text).group(0).split('-')
            scores.append(score)
    return scores


def format_fixtures(prediction):
    home = prediction[0][0]
    away = prediction[0][1]
    home_score = prediction[1][0]
    away_score = prediction[1][1]
    with open(f'./predictions/merson_{week}.csv', 'a') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([week, 'paul merson', home, away, home_score, away_score])


paul_predictions = []
paul_url = get_paul_url()
teams = paul_fixtures(paul_url)
scores = get_scores(paul_url)
for i in zip(teams, scores):
    paul_predictions.append(format_fixtures(i))
