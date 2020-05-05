import matplotlib.pyplot as plt
import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="moneymachine"
        )

cursor = mydb.cursor()

cursor.execute('SHOW COLUMNS FROM data;') # SELECT * FROM data')
columns = cursor.fetchall()

data = {}

for column in columns:
    if column[0] != 'id' and column[0] != 'timestamp':
        cursor.execute('SELECT `{}` FROM data;'.format(column[0]))
        data[column[0]] = cursor.fetchall()

x = list(range(len(data['AED'])))

for coin in data:
    price = data[coin]
    pN = price[0][0]
    priceNormal = [p[0] / pN for p in price]
    plt.plot(x, priceNormal)
plt.show()
