############ GETTING TOP EXCHANGES HIGH VOLUME COIN PAIR TRADES INFORMATION
# python 2.* ===> install beautifulsoup package (you might need some changes in the code), python 3.* ===> install bs4 package
# Output of the function get_top50exchanges_info() is a dictionary containing:
# {EXCHANGE RANKING in the last 24 hours,
# EXCHANGE NAME,
# TOTAL TRADE VOLUME IN THE LAST 24 hours,
# HIGH VOLUME PRODUCTS IN THE EXCHANGES THAT IS A DICT CONTAINING KEYS: {'rank', 'currency', 'pair', 'volume (24h)',
# 'price', 'volume (%)'}
#### Used url is "https://coinmarketcap.com/exchanges/volume/24-hour/"
# The function also saves the output dictionary in a pickle file
# Name of the output file contains the date and current time hour and minute
############
import urllib.request
from bs4 import BeautifulSoup
import pickle
import datetime

def get_top50exchanges_info():
    top50_exchanges = {}

    ######
    url = 'https://coinmarketcap.com/exchanges/volume/24-hour/'
    page = urllib.request.urlopen(url)
    mybytes = page.read()
    HTML = mybytes.decode("utf8")
    page.close()
    soup = BeautifulSoup(HTML, 'html.parser')

    Ex_tags = soup.findAll('h3', attrs={"class": "volume-header"})[0:50]
    for h_tag in Ex_tags:
        Ex_rank = int(h_tag.text.split('.')[0])
        Ex_name = h_tag.text.split('.')[1]
        table_headers = h_tag.find_next('tr')
        Ex_trade_info = dict()
        table_entries = table_headers.find_next('tr')
        total_volume = 'nan'
        for i in range(11):
            tds = table_entries.findAll('td')
            try:
                temp = int(tds[0].text)
                Ex_trade_info.update({ i+1:{
                    'rank': int(tds[0].text),
                    'Currency' : tds[1].text,
                    'Pair': tds[2].text,
                    'Volume (24h)': tds[3].text,
                    'Price': tds[4].text,
                    'Volume (%)': tds[5].text
                }})
                table_entries = table_entries.find_next('tr')
            except:
                if tds[0].text == 'Total':
                    total_volume = tds[1].text
                    break
                elif tds[0].text == 'View More':
                    table_entries = table_entries.find_next('tr')
                    tds = table_entries.findAll('td')
                    if tds[0].text == 'Total':
                        total_volume = tds[1].text
                    else:
                        total_volume = 'nan'
                    break
                else:
                    total_volume = 'nan'
                    break
        top50_exchanges.update({Ex_rank: {
            'rank': Ex_rank,
            'name': Ex_name,
            'total_volume': total_volume,
            'high_vol_products': Ex_trade_info
        }})
    now = datetime.datetime.now()
    now_time = str(now.year)+'-'+ str(now.month)+'-'+str(now.day)+'-'+str(now.hour)+str(now.minute)
    #pickle_out = open("top_exchanges-"+ now_time, "wb")  ### IF YOU WOULD SAVE THE INFORMATION, UNCOMMENT THESE TWO LINES
    #pickle.dump(top50_exchanges, pickle_out)           ###
    return top50_exchanges
print(get_top50exchanges_info())


#### TO LOAD THE EXCHANGE INFO YOU CAN USE THE FOLLOWING TWO LINES: ####

#pickle_in = open("file.pickle","rb")
#top_exchanges_info = pickle.load(pickle_in)

#### ####