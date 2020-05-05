import mysql.connector
import json
import requests


r =  requests.get('https://api.coinbase.com/v2/exchange-rates') 
exchangeRatesJson = r.json()['data']
# print(exchangeRatesJson)

columns = ''

for coin in exchangeRatesJson['rates']:
    coinStr = ' `{}` DOUBLE NOT NULL ,'.format(coin)
    columns = ''.join((columns, coinStr))
print(columns)
# print(columns)
#rint('CREATE TABLE `moneymachine`.`data` ( `id` INT NOT NULL AUTO_INCREMENT , `timestamp` DATE NOT NULL , {} PRIMARY KEY (`id`)) ENGINE = InnoDB;'.format(columns))
# CREATE TABLE `moneymachine`.`data` ( `id` INT NOT NULL AUTO_INCREMENT , `timestamp` DATE NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="moneymachine"
)

cursor = mydb.cursor()

cursor.execute('CREATE TABLE `moneymachine`.`data` ( `id` INT NOT NULL AUTO_INCREMENT , `timestamp` DATE NOT NULL , {} PRIMARY KEY (`id`)) ENGINE = InnoDB;'.format(columns))
mydb.commit()