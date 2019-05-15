import sqlite3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

#Create & Connect to DB
conn =sqlite3.connect('wikidb.sqlite')
cur = conn.cursor()
#DB Set up
cur.executescript('''
    DROP TABLE IF EXISTS urls;
    CREATE TABLE IF NOT EXISTS urls (ID INTEGER PRIMARY KEY, title TEXT, url TEXT, html TEXT
);
''')
def getLinks(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        new_link = (link.get('href'))
        try:
            if re.match("^/w", new_link):
                cur.execute('''INSERT INTO urls (url) VALUES (?)''', (new_link,))
        except: continue
    conn.commit()


getLinks('https://en.wikipedia.org/wiki/Neural_engineering')



cur.execute('SELECT  url FROM urls')
count =0

while count <5:
    for extension in cur.fetchall():
        url = extension[0]
        try:
            getLinks('https://en.wikipedia.org/wiki/'+url)
        except:continue
        count +=1

print('done')
