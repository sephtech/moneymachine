import requests
import mysql.connector
from datetime import datetime


def collect():

    r =  requests.get('https://api.coinbase.com/v2/exchange-rates') 
    exchangeRatesJson = r.json()['data']['rates']

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="moneymachine"
        )

    now = datetime.now().utcnow()
    print(now)


    columns = '`timestamp`'
    values = '"{}"'.format(now)

    for coin in exchangeRatesJson:
        columns = ''.join((columns, ', `{}`'.format(coin)))
        values = ''.join((values, ', "{}"'.format(exchangeRatesJson[coin])))
    
    sql = 'INSERT INTO data ({}) VALUES ({})'.format(columns, values)
    #print(sql)
    cursor = mydb.cursor()

    cursor.execute(sql)
    mydb.commit()

    # Detaillierte Info ueber die letzten 24h
    # https://api.crex24.com/v2/public/tickers?instrument=LTC-BTC

    # Alle letzten Trades
    # https://api.crex24.com/v2/public/recentTrades?instrument=LTC-BTC
#     cursor = mydb.cursor()


#     for coin in coins:
#         cursor.execute('SELECT id, price, volume, side, MAX(timestamp) FROM {}'.format(coins[coin]))
#         last_date_item = cursor.fetchall()[0]
#         last_date = last_date_item[4]
#         r= requests.get('https://api.crex24.com/v2/public/recentTrades?instrument={}'.format(coin))
#         recentTrades_json = r.json()
#         for i in enumerate(reversed(recentTrades_json)):
#             date = datetime.strptime(i[1]['timestamp'], '%Y-%m-%dT%H:%M:%SZ')

#             if last_date == None or last_date < date:
#                 print('Neuer Eintrag in', coin)
#                 print('Preis: {}, Volume: {}, Side: {}, Datum: {}'.format(i[1]['price'], i[1]['volume'], i[1]['side'], date))
#                 sql = "INSERT INTO {} (price, volume, side, timestamp) VALUES (%s, %s, %s, %s)".format(coins[coin])
#                 val = (i[1]['price'], i[1]['volume'], i[1]['side'], date)
                
#                 cursor.execute(sql, val)

#                 mydb.commit()
        
# collect()
