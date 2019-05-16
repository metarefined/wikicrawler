import sqlite3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from collections import Counter

#CREATE AND CONNECT TO DB
conn = sqlite3.connect('wiki.sqlite')
cur = conn.cursor()
cur.executescript('''
    DROP TABLE IF EXISTS wiki;
    CREATE TABLE IF NOT EXISTS wiki (title TEXT, url TEXT, most_used TEXT, id INTEGER PRIMARY KEY)

''')
def getLinkInfo(url):
    '''GETS INFO ABOUT THE LINK (TITLE, MOST USED WORD AND URLS)'''
    url_list = []
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    #GET TITLE
    formatted_title = soup.title.text.split("-")
    #GET LINKS
    for link in soup.find_all('a'):
        pre_link = (link.get('href'))
        try:
            if re.match("^/w", pre_link):
                url_list.append(pre_link)
        except:continue
    #GET MOST FREQUENT WORD WITHIN DOCUMENT
    text = soup.text.split()
    counter = Counter(text)
    most_used = counter.most_common(10)
    return formatted_title[0], url_list, most_used

def CreateDb(urls, title, most_used_words):
    for url in urls[5:10]:
        cur.execute('''INSERT INTO wiki(url, title, most_used) VALUES (?,?,?)''', (url,title,str(most_used_words[5])))
    conn.commit()

def getNewLink():
    cur.execute('''SELECT * FROM wiki ORDER BY url DESC LIMIT 1''')
    try:
        last_link = cur.fetchone()[1]
        return last_link
    except:
        print('oops')

def repeat():
    url = getNewLink()
    formatted_url = 'https://en.wikipedia.org/' + url
    urls = getLinkInfo(formatted_url)[1]
    title = getLinkInfo(formatted_url)[0]
    most_used_words = getLinkInfo(formatted_url)[2]
    CreateDb(urls, title, most_used_words)

first_url = input('Select the url')
hops = input('select how many times to run')

urls = getLinkInfo(first_url)[1]
title = getLinkInfo(first_url)[0]
most_used_words = getLinkInfo(first_url)[2]
CreateDb(urls, title, most_used_words)


for i in range(int(hops)):
    repeat()
