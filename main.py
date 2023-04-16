import requests
import datetime
import psycopg2
import time
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    while True:
        response = requests.get('http://api.nbp.pl/api/exchangerates/tables/a/')

        conn = psycopg2.connect(host="195.150.230.208", port=5432, database="2022_ciochon_adrian",
                                user="2022_ciochon_adrian", password="34275")

        cur = conn.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS exchange.kurs (id_waluty SERIAL PRIMARY KEY, currency CHARACTER(50), code CHARACTER(5), mid CHARACTER(10));")

        current = response.json()[0]['rates']
        for i in current:
            sql = "INSERT INTO exchange.kurs (currency, code, mid) VALUES (%s, %s, %s)"
            val = (i['currency'], i['code'], i['mid'])
            cur.execute(sql, val)

        conn.commit()

        conn.close()

        time.sleep(600)
    return 'test applacation'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

while True:
    response = requests.get('http://api.nbp.pl/api/exchangerates/tables/a/')

    conn = psycopg2.connect(host="195.150.230.208", port=5432, database="2022_ciochon_adrian",
                            user="2022_ciochon_adrian", password="34275")

    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS exchange.kurs (id_waluty SERIAL PRIMARY KEY, currency CHARACTER(50), code CHARACTER(5), mid CHARACTER(10));")

    current = response.json()[0]['rates']
    for i in current:
        sql = "INSERT INTO exchange.kurs (currency, code, mid) VALUES (%s, %s, %s)"
        val = (i['currency'], i['code'], i['mid'])
        cur.execute(sql, val)

    # cur.execute("Select * FROM dziekanat.adresy;", )

    # print(cur.fetchall())

    conn.commit()

    conn.close()

    #plik = open("test.txt", "a")  ##  w = plik do zapisu | a = dołączenie do pliku
    #plik.write(str(datetime.datetime.now()))
    #plik.write("\n")
    #currency = response.json()[0]['rates']
    #for i in currency:
    #    print(i['currency'], '-', i['mid'], ' ', i['code'])
    #    plik.write(i['currency'])
    #    plik.write(" ")
    #    plik.write(str(i['mid']))
    #    plik.write(" ")
    #    plik.write(i['code'])
    #    plik.write("\n")

    #plik.close()

    time.sleep(600)


