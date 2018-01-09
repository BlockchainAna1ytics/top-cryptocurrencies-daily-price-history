
import html.parser
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import date, timedelta


###### GET TOP 100 coins
#url = 'https://coinmarketcap.com/all/views/all/'
url = 'https://coinmarketcap.com/historical/20171203/'

page = urllib.request.urlopen(url)

mybytes = page.read()
HTML = mybytes.decode("utf8")

page.close()
soup = BeautifulSoup(HTML, 'html.parser')

coins_url = dict()
for tag in soup.find_all('a', attrs={"class": "currency-name-container"})[0:100]:
    coin_symbol = tag.find_next('td').text
    coins_url.update({coin_symbol:tag['href']})



####### END GET TOP 100 coins

first_day = '20161223'
last_day =  '20171228'
for coin, coin_url in coins_url.items():
    print(coin)
    full_url = 'https://coinmarketcap.com' + coin_url + 'historical-data/?start='+first_day+'&end='+ last_day
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


def get_top100_history(): ### coin_market_cap historical data
    last_day = date(2018,1,7)
    for i in range(105):
        folder = 'top coins price history2/' + str(last_day - timedelta(7*i)).replace('-','')

        if not os.path.exists(folder):
            os.makedirs(folder)

        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)



        ###### GET TOP 100 coins
        #url = 'https://coinmarketcap.com/all/views/all/'
        url = 'https://coinmarketcap.com/historical/' + str(last_day - timedelta(7*i)).replace('-','')
        print(url)
        page = urllib.request.urlopen(url)

        mybytes = page.read()
        HTML = mybytes.decode("utf8")

        page.close()
        soup = BeautifulSoup(HTML, 'html.parser')

        coins_url = dict()
        for tag in soup.find_all('a', attrs={"class": "currency-name-container"})[0:100]:
            coin_symbol = tag.find_next('td').text
            coins_url.update({coin_symbol:tag['href']})



        ####### END GET TOP 100 coins
        Days_Before = 400
        first_day = str(date.today() - timedelta(Days_Before)).replace('-', '')
        yesterday = str(date.today() - timedelta(1)).replace('-', '')
        for coin, coin_url in coins_url.items():
            print(coin)
            full_url = 'https://coinmarketcap.com' + coin_url + 'historical-data/?start='+first_day+'&end='+ yesterday
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
            df.to_csv(folder+ '/'+ coin + '.csv', columns=['date', 'open', 'low', 'high', 'close', 'volume', 'market_cap'])


