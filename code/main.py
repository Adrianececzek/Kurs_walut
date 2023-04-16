import requests
import psycopg2
import time

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


