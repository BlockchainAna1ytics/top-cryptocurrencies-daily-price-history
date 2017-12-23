
import html.parser
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


###### GET TOP 100 coins
url = 'https://coinmarketcap.com/all/views/all/'

page = urllib.request.urlopen(url)

mybytes = page.read()
HTML = mybytes.decode("utf8")

page.close()
soup = BeautifulSoup(HTML, 'html.parser')

coins_url = dict()
for tag in soup.find_all('a', attrs={"class": "currency-name-container"})[0:99]:
    coins_url.update({tag.text:tag['href']})

####### END GET TOP 100 coins

for coin, coin_url in coins_url.items():
    print(coin)
    full_url = 'https://coinmarketcap.com' + coin_url + 'historical-data/?start=20161223&end=20171223'
    page = urllib.request.urlopen(full_url)
    mybytes = page.read()
    coin_HTML = mybytes.decode("utf8")
    page.close()

    soup = BeautifulSoup(coin_HTML, 'html.parser')
    table = soup.findAll('table')
    rows = soup.findAll('tr')
    df = pd.DataFrame({'date':[], 'open':[], 'low':[], 'high':[],
                       'close':[], 'volume':[], 'market_cap':[]})
    for row in rows[1:]:
        tds = row.findAll('td')
        try:
            df = df.append(pd.DataFrame({'date':[tds[0].text],
                   'open': [float(tds[1].text.replace(",", ""))],
                   'low': [float(tds[2].text.replace(",", ""))],
                   'high': [float(tds[3].text.replace(",", ""))],
                   'close': [float(tds[4].text.replace(",", ""))],
                   'volume': [float(tds[5].text.replace(",", ""))],
                   'market_cap': float(tds[6].text.replace(",", ""))}))
        except:
            continue
    df.to_csv('top coins price history/'+ coin + '.csv', columns=['date', 'open', 'low', 'high', 'close', 'volume', 'market_cap'])





